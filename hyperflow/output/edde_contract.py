from __future__ import annotations

from typing import Any

from hyperflow.config import get_pipeline_stage_aliases
from hyperflow.contracts.version_policy import CONTRACT_VERSION
from hyperflow.control.mps_profiles import MPS_PROFILES
from hyperflow.schemas.command_schema import CommandObject
from hyperflow.schemas.runtime_state_schema import RuntimeState


def _normalize_next_step(value: Any) -> str:
    lower = str(value or "").strip().lower()
    if lower in {"", "done", "end", "final", "finish"}:
        return "END"
    if lower in {"expand", "decide", "retry", "clarify_or_continue", "continue_with_warning", "return_to_core"}:
        return "DECIDE"
    return "DECIDE"


def _default_constraints(command: CommandObject) -> dict[str, bool]:
    return {
        "safe": "safe_mode" in command.constraints,
        "sandboxed": True,
        "llm_no_direct_ffi": True,
    }


def _phase_frame(
    phase: str,
    trace_id: str,
    *,
    input_payload: dict[str, Any] | None = None,
    plan: list[Any] | None = None,
    results: dict[str, Any] | None = None,
    assessment: dict[str, Any] | None = None,
    next_step: str = "DECIDE",
    constraints: dict[str, bool] | None = None,
) -> dict[str, Any]:
    return {
        "phase": phase,
        "trace_id": trace_id,
        "input": input_payload or {},
        "plan": list(plan or []),
        "results": dict(results or {}),
        "assessment": dict(assessment or {}),
        "constraints": constraints or {
            "safe": True,
            "sandboxed": True,
            "llm_no_direct_ffi": True,
        },
        "next_step": next_step,
    }


def build_edde_contract(
    command: CommandObject,
    state: RuntimeState,
    final_bundle: dict[str, Any],
    result: Any,
    observer_status: str,
    *,
    observer_contract: dict[str, Any] | None = None,
    graph_snapshot: dict[str, Any] | None = None,
    graph_analytics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    partials = list(state.partial_results)
    extract_bundle = dict(partials[0]) if len(partials) > 0 else {}
    discover_bundle = dict(partials[1]) if len(partials) > 1 else {}
    do_bundle = dict(partials[2]) if len(partials) > 2 else {}
    output_bundle = dict(final_bundle)
    constraints = _default_constraints(command)
    pipeline_stage_map = get_pipeline_stage_aliases()
    mps_profile = dict(MPS_PROFILES.get(state.mps_level, MPS_PROFILES[2]))

    decide_input = {
        "task_core": extract_bundle.get("task_core", command.cleaned_text or command.raw_input),
        "tokens": extract_bundle.get("tokens", command.tokens),
        "constraints": extract_bundle.get("constraints", command.constraints),
        "scope": extract_bundle.get("scope", "local"),
    }
    decide_plan = list(state.plan)
    if not decide_plan and discover_bundle.get("selected_path"):
        decide_plan = [str(discover_bundle.get("selected_path"))]
    decide_assessment = {
        "strategy": discover_bundle.get("strategy", f"{command.intent}:{command.mode}"),
        "reasoning_depth": discover_bundle.get("reasoning_depth", "medium"),
        "selected_path": discover_bundle.get("selected_path", command.intent),
        "resolved_edde_phase_hints": list(command.parser_trace.get("resolved_edde_phase", [])),
    }
    do_results = {
        "draft_result": do_bundle.get("draft_result", ""),
        "partial_insights": list(do_bundle.get("partial_insights", [])),
        "actions": list(do_bundle.get("actions", [])),
        "coverage_status": do_bundle.get("coverage_status", "ok"),
        "action_execution": list(output_bundle.get("action_execution", [])),
    }
    output_assessment = {
        "summary": output_bundle.get("summary", getattr(result, "summary", "")),
        "final_insights": list(output_bundle.get("final_insights", getattr(result, "insights", []))),
        "confidence": output_bundle.get("confidence", getattr(result, "confidence", command.confidence)),
        "observer_status": observer_status,
        "observer_contract": observer_contract or {},
    }

    timeline = [
        _phase_frame(
            "DECIDE",
            state.run_id,
            input_payload=decide_input,
            plan=decide_plan,
            assessment=decide_assessment,
            next_step="DO",
            constraints=constraints,
        ),
        _phase_frame(
            "DO",
            state.run_id,
            results=do_results,
            assessment={
                "executed_operations": list(command.operations),
                "active_target": state.active_target,
            },
            next_step="OUTPUT",
            constraints=constraints,
        ),
        _phase_frame(
            "OUTPUT",
            state.run_id,
            results={
                "observer_status": observer_status,
                "actions": list(output_bundle.get("actions", getattr(result, "actions", []))),
            },
            assessment=output_assessment,
            next_step=_normalize_next_step(output_bundle.get("next_step")),
            constraints=constraints,
        ),
    ]

    return {
        "schema": "hyperflow/edde-contract/v1",
        "contract_version": CONTRACT_VERSION,
        "trace_id": state.run_id,
        "status": "fallback" if observer_status == "FALLBACK" else "ok",
        "input": {
            "raw_prompt": command.raw_input,
            "emoji_run": "".join(command.tokens),
            "core_text": command.cleaned_text or command.raw_input,
        },
        "parser": dict(command.parser_trace),
        "timeline": timeline,
        "runtime": {
            "flow": ["DECIDE", "DO", "OUTPUT"],
            "pipeline_path": list(output_bundle.get("pipeline_path", [])),
            "pipeline_stage_map": output_bundle.get("pipeline_stage_map", pipeline_stage_map),
            "mps": {
                "level": state.mps_level,
                "risk_level": state.risk_level,
                "profile": mps_profile,
            },
            "observer": observer_contract or {},
            "graph": {
                "summary": graph_snapshot or {},
                "analytics": graph_analytics or {},
            },
        },
        "output": {
            "kind": getattr(result, "kind", command.output_type),
            "payload": result.to_dict(include_contract=False),
        },
        "errors": [str(item) for item in output_bundle.get("errors", [])],
    }
