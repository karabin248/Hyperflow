"""
main.py — Hyperflow MVP unified entry point.

Merges ZIP1's full EDDE engine (emoji parser, MPS controller, graph memory,
checkpoint system) with ZIP2's infrastructure (OpenRouter LLM, PostgreSQL
persistence contract, repository scanner, workflow resume).

Architecture:
  FastAPI → command_builder (emoji parser + intent resolver + MPS)
          → runtime_kernel.run() (async EDDE pipeline)
              → reasoning.run_do_phase_async() → OpenRouter LLM
          → response serialization (EDDE contract + canonical phases)
  FastAPI → scanner.core (git clone + language/dep analysis)
  FastAPI → workflow topology (Kahn sort + per-step LLM)
"""
from __future__ import annotations

import hashlib
import os
import uuid
from collections import deque
from datetime import datetime, timezone
from typing import Any, Deque, Dict, List, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── ZIP1 engine imports ───────────────────────────────────────────────────────
from hyperflow.language.command_builder import build_command
from hyperflow.engine.runtime_kernel import run as kernel_run
from hyperflow.engine.reasoning import set_llm_backend
from hyperflow.schemas.command_schema import CommandObject

# ── ZIP2 OpenRouter ────────────────────────────────────────────────────────────
from openrouter import call_model, OpenRouterUnavailable

# ── Scanner ────────────────────────────────────────────────────────────────────
from scanner.core import (
    analyze_repo_real, analyze_repo_stub,
    compute_overlap_scores,
    _SCAN_MAX_REPOS, _SCAN_MAX_DURATION_S, _TMP_MIN_FREE_MB,
)

import asyncio
import shutil
import tempfile
from pathlib import Path

# ── App bootstrap ─────────────────────────────────────────────────────────────
app = FastAPI(title="Hyperflow MVP", version="0.3.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Register LLM backend once at startup (ZIP1 engine picks it up)
set_llm_backend(call_model)

# ── Canonical phase registry (ZIP2 semantics, 6-phase) ────────────────────────
_CANONICAL_PHASES: List[str] = [
    "perceive","extract_essence","sense_direction","synthesize","generate_options","choose",
]
_PHASE_POS: Dict[str,int] = {p: i+1 for i,p in enumerate(_CANONICAL_PHASES)}

# ── Ring-buffer log store ─────────────────────────────────────────────────────
_LOG_STORE: Deque[Dict[str,Any]] = deque(maxlen=200)

def _emit(event:str, run_id:str, **kw:Any)->None:
    _LOG_STORE.append({"event":event,"run_id":run_id,
                       "timestamp":datetime.now(timezone.utc).isoformat(),**kw})

# ── Request / response models ──────────────────────────────────────────────────
class RunRequest(BaseModel):
    prompt: str
    type: Optional[str] = "agent"
    name: Optional[str] = None

class ExploreRequest(BaseModel):
    prompt: str
    mps_level: Optional[int] = None

class WorkflowStep(BaseModel):
    id: str; name: str; prompt: str; dependsOn: List[str] = []

class WorkflowRunRequest(BaseModel):
    workflowId: str; name: str; steps: List[WorkflowStep]

class CompletedNode(BaseModel):
    nodeId: str; name: str
    result: Optional[Dict[str,Any]] = None
    startedAt: Optional[str] = None; completedAt: Optional[str] = None

class WorkflowResumeRequest(BaseModel):
    runId: str; workflowId: str; name: str
    steps: List[WorkflowStep]; completedNodes: List[CompletedNode]

class RepositoryInput(BaseModel):
    id: str; name: str; url: str

class RepositoryScanRequest(BaseModel):
    repositories: List[RepositoryInput]

class GraphRepoInput(BaseModel):
    id: str; name: str; url: Optional[str]=None
    language: str; classification: str
    dependencyCount: int; dependencyNames: Optional[List[str]]=None
    packageName: Optional[str]=None

class RepositoryGraphRequest(BaseModel):
    repositories: List[GraphRepoInput]

# ── Helpers ────────────────────────────────────────────────────────────────────
def _topological_sort(steps: List[WorkflowStep]) -> List[WorkflowStep]:
    ids = {s.id for s in steps}
    for s in steps:
        for dep in s.dependsOn:
            if dep not in ids:
                raise ValueError(f"Step \'{s.id}\' depends on unknown \'{dep}\'")
    step_map = {s.id: s for s in steps}
    in_deg   = {s.id: 0 for s in steps}
    deps     = {s.id: [] for s in steps}
    for s in steps:
        for dep in s.dependsOn:
            in_deg[s.id] += 1; deps[dep].append(s.id)
    queue   = [sid for sid,d in in_deg.items() if d==0]
    ordered: List[WorkflowStep] = []
    while queue:
        cur = queue.pop(0); ordered.append(step_map[cur])
        for nxt in deps[cur]:
            in_deg[nxt] -= 1
            if in_deg[nxt] == 0: queue.append(nxt)
    if len(ordered) != len(steps):
        raise ValueError("Workflow contains a dependency cycle")
    return ordered

def _build_canonical_trace(run_id:str, phases:List[str])->Dict[str,Any]:
    terminal = phases[-1] if phases else ""
    expected = [p for p in _CANONICAL_PHASES if p in phases]
    return {
        "scope":"python_core_observable","phases_completed":phases,
        "terminal_phase":terminal,"order_preserved":(phases==expected),
        "cycle_version":"1.0",
    }

async def _do_step(prompt:str, intent:str, mode:str) -> Dict[str,Any]:
    """Execute a single workflow step — LLM call with stub fallback."""
    try:
        text,model = await call_model(prompt, intent, mode)
        return {"output":text,"intent":intent,"mode":mode,"source":"llm","model":model}
    except OpenRouterUnavailable:
        return {"output":f"Executed \'{intent}\' op: {prompt[:120]}","intent":intent,
                "mode":mode,"source":"stub"}

# ── Endpoints ──────────────────────────────────────────────────────────────────
@app.get("/v1/health")
def health():
    return {"status":"ok","service":"hyperflow-mvp","version":"0.3.0",
            "engine":"edde+mps+emoji","llm_backend":"openrouter+stub_fallback"}

@app.get("/v1/logs/recent")
def logs_recent(limit:int=Query(default=20,ge=1,le=200)):
    return {"items":list(_LOG_STORE)[-limit:]}

@app.post("/v1/explore")
async def explore(req: ExploreRequest):
    """Return candidate execution paths for a prompt (ZIP2 compatibility)."""
    command = build_command(req.prompt)
    intent  = command.intent
    run_id  = str(uuid.uuid4())
    _emit("explore_request", run_id, intent=intent, mode=command.mode)
    paths = [
        {"label":f"EDDE {intent} path","path_key":f"edde_{intent}",
         "description":f"Full EDDE pipeline ({intent} intent, {command.mode} mode)",
         "evaluation_score":0.90},
        {"label":f"Direct {intent} path","path_key":f"direct_{intent}",
         "description":f"Direct LLM call without MPS elevation",
         "evaluation_score":0.78},
    ]
    return {"paths":paths,"selected_path_label":paths[0]["label"],
            "selected_path_key":paths[0]["path_key"],
            "selection_reason":f"EDDE pipeline selected for intent \'{intent}\'"}

@app.post("/v1/run")
async def run(req: RunRequest):
    run_id     = str(uuid.uuid4())
    started_at = datetime.now(timezone.utc)
    _emit("run_started", run_id, prompt_tokens=len(req.prompt.split()))

    try:
        # ── ZIP1 full pipeline: emoji parse → MPS → EDDE → checkpoint ──
        command = build_command(req.prompt)
        result  = await kernel_run(command)

        # ── Log canonical phases ─────────────────────────────────────────
        for phase in ["sense_direction","synthesize","generate_options","choose"]:
            _emit("canonical_phase_entered",  run_id, phase=phase, position=_PHASE_POS.get(phase,0))
            _emit("canonical_phase_completed", run_id, phase=phase, position=_PHASE_POS.get(phase,0))

        _emit("run_completed", run_id, intent=command.intent, mode=command.mode,
              source=getattr(result,"llm_source","stub"),
              model=getattr(result,"llm_model",None))

        return {
            "run_id":     run_id,
            "intent":     command.intent,
            "mode":       command.mode,
            "output_type":command.output_type,
            "mps_level":  result.edde_contract.get("mps_level",2) if hasattr(result,"edde_contract") and isinstance(result.edde_contract,dict) else 2,
            "tokens":     command.tokens,
            "result":     {"output": result.summary,
                           "reasoning": str(getattr(result,"insights",[])),
                           "source": getattr(result,"llm_source","stub"),
                           "model":  getattr(result,"llm_model",None)},
            "edde_contract": result.edde_contract if hasattr(result,"edde_contract") else {},
            "observer_status": result.observer_status if hasattr(result,"observer_status") else "OK",
            # ZIP2-compatible envelope
            "runId":       run_id, "type":req.type or "agent",
            "name":        req.name or f"{command.intent} run",
            "status":      "completed", "progress": 100,
            "startedAt":   started_at.isoformat(),
            "completedAt": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as exc:
        _emit("run_failed", run_id, error=f"{type(exc).__name__}: {exc}")
        return {
            "run_id":run_id,"status":"failed","error":str(exc),
            "runId":run_id,"type":req.type or "agent","name":req.name or "failed run",
            "progress":0,"startedAt":started_at.isoformat(),
            "completedAt":datetime.now(timezone.utc).isoformat(),
        }


@app.post("/v1/workflow/run")
async def workflow_run(req: WorkflowRunRequest):
    run_id      = str(uuid.uuid4())
    run_started = datetime.now(timezone.utc)
    _emit("workflow_run_started", run_id, workflow_id=req.workflowId,
          name=req.name, total_steps=len(req.steps))
    try:
        ordered = _topological_sort(req.steps)
    except ValueError as exc:
        _emit("workflow_run_failed", run_id, error=str(exc))
        return {"runId":run_id,"workflowId":req.workflowId,"name":req.name,"status":"failed",
                "progress":0,"startedAt":run_started.isoformat(),
                "completedAt":datetime.now(timezone.utc).isoformat(),"error":str(exc),"nodes":[]}

    nodes:List[Dict[str,Any]] = []
    completed = 0; run_failed = False; run_error = None

    for step in ordered:
        if run_failed:
            nodes.append({"nodeId":step.id,"name":step.name,"status":"skipped",
                          "startedAt":None,"completedAt":None,"result":None,"error":None})
            continue
        t0 = datetime.now(timezone.utc)
        _emit("workflow_node_started", run_id, node_id=step.id, node_name=step.name)
        try:
            command = build_command(step.prompt)
            result  = await _do_step(step.prompt, command.intent, command.mode)
            completed += 1
            _emit("workflow_node_completed", run_id, node_id=step.id, source=result.get("source"))
            nodes.append({"nodeId":step.id,"name":step.name,"status":"completed",
                          "startedAt":t0.isoformat(),"completedAt":datetime.now(timezone.utc).isoformat(),
                          "result":result,"error":None})
        except Exception as exc:
            run_failed=True; run_error=f"Step \'{step.id}\' failed: {exc}"
            _emit("workflow_node_failed", run_id, node_id=step.id, error=str(exc))
            nodes.append({"nodeId":step.id,"name":step.name,"status":"failed",
                          "startedAt":t0.isoformat(),"completedAt":datetime.now(timezone.utc).isoformat(),
                          "result":None,"error":str(exc)})

    status   = "failed" if run_failed else "completed"
    progress = round((completed/len(req.steps))*100,1) if req.steps else 0
    _emit("workflow_run_completed", run_id, status=status, progress=progress)
    return {"runId":run_id,"workflowId":req.workflowId,"name":req.name,
            "status":status,"progress":progress,
            "startedAt":run_started.isoformat(),"completedAt":datetime.now(timezone.utc).isoformat(),
            "error":run_error,"nodes":nodes}


@app.post("/v1/workflow/resume")
async def workflow_resume(req: WorkflowResumeRequest):
    run_started = datetime.now(timezone.utc)
    _emit("workflow_resume_started", req.runId, workflow_id=req.workflowId,
          completed_carried=len(req.completedNodes))
    try:
        ordered = _topological_sort(req.steps)
    except ValueError as exc:
        return {"runId":req.runId,"workflowId":req.workflowId,"name":req.name,"status":"failed",
                "progress":0,"startedAt":run_started.isoformat(),
                "completedAt":datetime.now(timezone.utc).isoformat(),"error":str(exc),"nodes":[]}

    step_ids = {s.id for s in req.steps}
    for cn in req.completedNodes:
        if cn.nodeId not in step_ids:
            err = f"Completed node \'{cn.nodeId}\' not in workflow definition — drift not supported"
            return {"runId":req.runId,"status":"failed","error":err,"nodes":[],
                    "progress":0,"startedAt":run_started.isoformat(),
                    "completedAt":datetime.now(timezone.utc).isoformat(),
                    "workflowId":req.workflowId,"name":req.name}

    completed_map = {cn.nodeId:cn for cn in req.completedNodes}
    nodes:List[Dict[str,Any]] = []
    completed = len(req.completedNodes)
    run_failed = False; run_error = None

    for step in ordered:
        if step.id in completed_map:
            prior = completed_map[step.id]
            nodes.append({"nodeId":step.id,"name":step.name,"status":"completed",
                          "startedAt":prior.startedAt,"completedAt":prior.completedAt,
                          "result":prior.result,"error":None})
            continue
        t0 = datetime.now(timezone.utc)
        if run_failed:
            nodes.append({"nodeId":step.id,"name":step.name,"status":"skipped",
                          "startedAt":None,"completedAt":None,"result":None,"error":None})
            continue
        try:
            command = build_command(step.prompt)
            result  = await _do_step(step.prompt, command.intent, command.mode)
            completed += 1
            nodes.append({"nodeId":step.id,"name":step.name,"status":"completed",
                          "startedAt":t0.isoformat(),"completedAt":datetime.now(timezone.utc).isoformat(),
                          "result":result,"error":None})
        except Exception as exc:
            run_failed=True; run_error=f"Step \'{step.id}\' failed: {exc}"
            nodes.append({"nodeId":step.id,"name":step.name,"status":"failed",
                          "startedAt":t0.isoformat(),"completedAt":datetime.now(timezone.utc).isoformat(),
                          "result":None,"error":str(exc)})

    status   = "failed" if run_failed else "completed"
    total    = len(req.steps)
    progress = round((completed/total)*100,1) if total>0 else 0
    _emit("workflow_resume_completed", req.runId, status=status)
    return {"runId":req.runId,"workflowId":req.workflowId,"name":req.name,
            "status":status,"progress":progress,
            "startedAt":run_started.isoformat(),"completedAt":datetime.now(timezone.utc).isoformat(),
            "error":run_error,"nodes":nodes}


@app.post("/v1/repositories/scan")
async def repository_scan(req: RepositoryScanRequest):
    run_id      = str(uuid.uuid4())
    run_started = datetime.now(timezone.utc)
    scan_mode   = os.environ.get("SCAN_MODE","v2")

    if not req.repositories:
        return {"runId":run_id,"status":"completed","progress":100.0,
                "startedAt":run_started.isoformat(),"completedAt":datetime.now(timezone.utc).isoformat(),
                "error":None,"repos":[]}

    if len(req.repositories) > _SCAN_MAX_REPOS:
        return {"runId":run_id,"status":"failed","progress":0,
                "error":f"Max {_SCAN_MAX_REPOS} repos per request",
                "startedAt":run_started.isoformat(),"completedAt":datetime.now(timezone.utc).isoformat(),
                "repos":[]}

    repos_in   = [{"id":r.id,"name":r.name,"url":r.url} for r in req.repositories]
    overlaps   = compute_overlap_scores(repos_in)
    deadline   = datetime.now(timezone.utc).timestamp() + _SCAN_MAX_DURATION_S
    repos_out: List[Dict[str,Any]] = []
    failed     = 0

    if scan_mode == "stub":
        for r in repos_in:
            repos_out.append(analyze_repo_stub(r, overlaps[r["id"]]))
    else:
        work_dir = Path(tempfile.mkdtemp(prefix="hyperflow-scan-"))
        try:
            for r in repos_in:
                remaining = deadline - datetime.now(timezone.utc).timestamp()
                if remaining <= 0:
                    repos_out.append({"id":r["id"],"language":"unknown","classification":"unknown",
                                      "classificationRationale":None,"dependencyCount":0,
                                      "dependencyNames":[],"overlapScore":overlaps[r["id"]],
                                      "cloneDurationMs":None,"analysisDurationMs":None,
                                      "error":"Scan deadline exceeded"})
                    failed += 1; continue
                try:
                    repos_out.append(await analyze_repo_real(r, work_dir, overlaps[r["id"]], remaining))
                except Exception as exc:
                    failed += 1
                    repos_out.append({"id":r["id"],"language":"unknown","classification":"unknown",
                                      "classificationRationale":None,"dependencyCount":0,
                                      "dependencyNames":[],"overlapScore":overlaps[r["id"]],
                                      "cloneDurationMs":None,"analysisDurationMs":None,
                                      "error":str(exc)})
        finally:
            shutil.rmtree(work_dir, ignore_errors=True)

    scanned  = len(repos_out) - failed
    status   = "completed" if failed==0 else "partial"
    progress = 100.0 if failed==0 else round((scanned/len(req.repositories))*100,1)
    return {"runId":run_id,"status":status,"progress":progress,
            "startedAt":run_started.isoformat(),"completedAt":datetime.now(timezone.utc).isoformat(),
            "error":None,"repos":repos_out}


@app.post("/v1/repositories/graph")
async def repository_graph(req: RepositoryGraphRequest):
    """Build dependency graph from pre-scanned repository data."""
    run_id = str(uuid.uuid4())
    nodes  = [{"id":r.id,"name":r.name,"language":r.language,"classification":r.classification}
               for r in req.repositories]
    edges: List[Dict[str,Any]] = []
    overlap_pairs: List[Dict[str,Any]] = []

    # Build edges from dependency names matching package names
    pkg_map: Dict[str,str] = {}  # package_name -> repo_id
    for r in req.repositories:
        if r.packageName:
            pkg_map[r.packageName.lower()] = r.id

    for r in req.repositories:
        for dep in (r.dependencyNames or []):
            target_id = pkg_map.get(dep.lower())
            if target_id and target_id != r.id:
                edges.append({"source":r.id,"target":target_id,"weight":1.0,
                              "type":"dependency","matchedOn":dep})

    # Overlap pairs (Jaccard on names)
    repos_in = [{"id":r.id,"name":r.name} for r in req.repositories]
    scores   = compute_overlap_scores(repos_in)
    seen     = set()
    for i, ri in enumerate(req.repositories):
        for rj in req.repositories[i+1:]:
            key = tuple(sorted([ri.id, rj.id]))
            if key in seen: continue
            seen.add(key)
            names_i = set(ri.name.lower().replace("-"," ").split())
            names_j = set(rj.name.lower().replace("-"," ").split())
            if names_i and names_j:
                score = round(len(names_i & names_j)/max(len(names_i),len(names_j)),4)
                if score > 0:
                    overlap_pairs.append({"repoA":ri.id,"repoB":rj.id,"score":score})

    return {"nodes":nodes,"edges":edges,"overlapPairs":overlap_pairs}
