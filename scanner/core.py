"""scanner/core.py — Repository analysis module (from ZIP2).

FIX #7: Added explicit _validate_repo_url() helper for defense-in-depth
URL validation before git clone. Prevents SSRF via file://, ssh://, etc.
The existing _ALLOWED_URL_SCHEMES check in _clone_repo is preserved.
"""
from __future__ import annotations
import asyncio, hashlib, json as _json_mod, logging, os, re, shutil, tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

_SCAN_MAX_REPOS=20; _SCAN_MAX_DURATION_S=300; _CLONE_TIMEOUT_S=60
_CLONE_MAX_SIZE_MB=500; _TREE_WALK_MAX_FILES=50_000; _TMP_MIN_FREE_MB=512
_ALLOWED_URL_SCHEMES=("http://","https://")

_EXT_LANG:Dict[str,str]={
    ".py":"python",".pyw":"python",".pyi":"python",
    ".ts":"typescript",".tsx":"typescript",
    ".js":"javascript",".jsx":"javascript",".mjs":"javascript",
    ".go":"go",".rs":"rust",".java":"java",".kt":"kotlin",
    ".rb":"ruby",".php":"php",".cs":"csharp",".cpp":"cpp",".c":"c",
    ".swift":"swift",".scala":"scala",".ex":"elixir",".exs":"elixir",
    ".hs":"haskell",".lua":"lua",".r":"r",".sh":"shell",".dart":"dart",
}
_EXT_WEIGHTS:Dict[str,float]={
    "python":1.0,"typescript":1.2,"javascript":0.8,"go":1.0,"rust":1.0,
    "java":1.0,"kotlin":1.0,"ruby":1.0,"csharp":1.0,"cpp":0.9,"c":0.7,
    "swift":1.0,"scala":1.0,"elixir":1.0,"shell":0.3,"dart":1.0,
}
_SKIP_DIRS={".git","node_modules","__pycache__",".tox",".mypy_cache",
            ".pytest_cache","venv",".venv","env","dist","build","target",
            "vendor",".next",".nuxt"}


def _validate_repo_url(url: str) -> None:
    """FIX #7: Explicit URL validation — raises ValueError on disallowed schemes.

    Prevents SSRF vectors such as file://, ssh://, git://, ftp://.
    Defense-in-depth: _clone_repo also checks _ALLOWED_URL_SCHEMES.
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(
            f"Repository URL scheme {parsed.scheme!r} is not allowed. "
            f"Only http:// and https:// are permitted."
        )
    if not parsed.netloc:
        raise ValueError(f"Repository URL has no valid host: {url[:120]!r}")


def compute_overlap_scores(repos:List[Dict[str,str]])->Dict[str,float]:
    if len(repos)<=1: return {r["id"]:0.0 for r in repos}
    names=[r["name"].lower() for r in repos]
    scores:Dict[str,float]={}
    for i,repo in enumerate(repos):
        ti=set(names[i].replace("-"," ").split())
        total=0.0
        for j,other in enumerate(names):
            if i==j: continue
            tj=set(other.replace("-"," ").split())
            if ti and tj: total+=len(ti&tj)/max(len(ti),len(tj))
        scores[repo["id"]]=round(total/(len(repos)-1),4)
    return scores

def detect_language(repo_dir:Path)->str:
    counts:Dict[str,float]={}
    seen=0
    for root,dirs,files in os.walk(repo_dir):
        dirs[:]=[d for d in dirs if d not in _SKIP_DIRS]
        for fname in files:
            seen+=1
            if seen>_TREE_WALK_MAX_FILES: break
            ext=os.path.splitext(fname)[1].lower()
            lang=_EXT_LANG.get(ext)
            if lang: counts[lang]=counts.get(lang,0.0)+_EXT_WEIGHTS.get(lang,1.0)
        if seen>_TREE_WALK_MAX_FILES: break
    return max(counts,key=counts.get) if counts else "unknown"

_SERVER_PATTERNS=[
    ("main.py",r"(uvicorn|gunicorn|flask|fastapi|django|\.run\()"),
    ("app.py",r"(flask|fastapi|\.run\()"),
    ("server.ts",r"(\.listen\s*\(|express\(\)|fastify\(\))"),
    ("index.ts",r"(\.listen\s*\(|express\(\)|fastify\(\))"),
    ("main.go",r"(ListenAndServe|gin\.|echo\.|fiber\.)"),
    ("main.rs",r"(actix|rocket|axum|warp|hyper)"),
]
_INFRA_DIRS={"terraform","helm","k8s","kubernetes","ansible","pulumi"}
_INFRA_MARKERS={"Dockerfile","docker-compose.yml","docker-compose.yaml"}

def detect_classification(repo_dir:Path)->Tuple[str,Dict[str,Any]]:
    infra=[d for d in _INFRA_DIRS if (repo_dir/d).is_dir()]
    infra+=[m for m in _INFRA_MARKERS if (repo_dir/m).exists()]
    if len(infra)>=2 or any((repo_dir/d).is_dir() for d in _INFRA_DIRS):
        return "infrastructure",{"decision":f"infra: {infra}"}
    for ef,pat in _SERVER_PATTERNS:
        p=repo_dir/ef
        if p.exists():
            try:
                if re.search(pat,p.read_text(errors="replace")[:8192]):
                    return "service",{"decision":f"server entry in {ef}"}
            except OSError: pass
    has_lib=any((repo_dir/f).exists() for f in ["setup.py","setup.cfg"])
    if (repo_dir/"pyproject.toml").exists():
        try:
            if "[project]" in (repo_dir/"pyproject.toml").read_text(errors="replace"):
                has_lib=True
        except OSError: pass
    if (repo_dir/"package.json").exists():
        try:
            pkg=_json_mod.loads((repo_dir/"package.json").read_text(errors="replace"))
            if "main" in pkg or "exports" in pkg: has_lib=True
        except Exception: pass
    has_cli=any((repo_dir/d).is_dir() for d in ["bin","cli","cmd"])
    if has_cli and not has_lib: return "tool",{"decision":"CLI entry"}
    if has_lib: return "library",{"decision":"lib manifest"}
    return "unknown",{"decision":"no markers"}

def extract_dependencies(repo_dir:Path)->Tuple[int,List[str]]:
    def norm(n,eco):
        n=re.split(r"[><=!~;@\[]",n.strip())[0].strip()
        return n.replace("-","_").lower() if eco in ("python","rust") else n.lower()
    names:List[str]=[]
    req=repo_dir/"requirements.txt"
    if req.exists():
        for line in req.read_text(errors="replace").splitlines():
            s=line.strip()
            if s and not s.startswith(("#","-")): n=norm(s,"python"); n and names.append(n)
    py=repo_dir/"pyproject.toml"
    if py.exists():
        try:
            import tomllib
            data=tomllib.loads(py.read_text(errors="replace"))
            for dep in data.get("project",{}).get("dependencies",[]):
                n=norm(dep,"python"); n and names.append(n)
        except Exception: pass
    pkg=repo_dir/"package.json"
    if pkg.exists():
        try:
            for k in _json_mod.loads(pkg.read_text(errors="replace")).get("dependencies",{}).keys():
                names.append(k.strip().lower())
        except Exception: pass
    unique=list(dict.fromkeys(names))
    return len(unique),unique

async def _clone_repo(url:str,dest:Path,timeout:int=_CLONE_TIMEOUT_S)->float:
    if not any(url.startswith(s) for s in _ALLOWED_URL_SCHEMES):
        raise ValueError(f"URL scheme not allowed: {url[:80]}")
    proc=await asyncio.create_subprocess_exec(
        "git","clone","--depth","1","--single-branch","--quiet",url,str(dest),
        stdout=asyncio.subprocess.DEVNULL,stderr=asyncio.subprocess.PIPE)
    try: _,stderr=await asyncio.wait_for(proc.communicate(),timeout=timeout)
    except asyncio.TimeoutError:
        proc.kill(); await proc.wait(); shutil.rmtree(dest,ignore_errors=True)
        raise TimeoutError(f"Clone timed out after {timeout}s")
    if proc.returncode!=0:
        err=(stderr or b"").decode(errors="replace").strip()
        shutil.rmtree(dest,ignore_errors=True); raise RuntimeError(f"git clone failed: {err}")
    mb=sum(f.stat().st_size for f in dest.rglob("*") if f.is_file())/(1024*1024)
    if mb>_CLONE_MAX_SIZE_MB: shutil.rmtree(dest,ignore_errors=True); raise RuntimeError(f"Clone {mb:.0f}MB > limit")
    return mb

async def analyze_repo_real(repo:Dict[str,str],work_dir:Path,overlap:float,remaining_s:float)->Dict[str,Any]:
    # FIX #7: Validate URL before attempting clone
    _validate_repo_url(repo["url"])
    safe_id=re.sub(r"[^a-zA-Z0-9_\-]","_",repo["id"])[:64]
    dest=work_dir/safe_id
    timeout=min(_CLONE_TIMEOUT_S,max(int(remaining_s),5))
    t0=datetime.now(timezone.utc)
    await _clone_repo(repo["url"],dest,timeout=timeout)
    clone_ms=int((datetime.now(timezone.utc)-t0).total_seconds()*1000)
    try:
        t1=datetime.now(timezone.utc)
        language=detect_language(dest)
        cls,rationale=detect_classification(dest)
        dep_count,dep_names=extract_dependencies(dest)
        analysis_ms=int((datetime.now(timezone.utc)-t1).total_seconds()*1000)
    finally: shutil.rmtree(dest,ignore_errors=True)
    return {"id":repo["id"],"language":language,"classification":cls,
            "classificationRationale":rationale,"dependencyCount":dep_count,
            "dependencyNames":dep_names,"overlapScore":overlap,
            "cloneDurationMs":clone_ms,"analysisDurationMs":analysis_ms,"error":None}

def analyze_repo_stub(repo:Dict[str,str],overlap:float)->Dict[str,Any]:
    n=repo["name"].lower()
    lang="typescript" if any(x in n for x in ["ts","react","ui","web","frontend"]) else "python"
    cls=("service" if any(x in n for x in ["api","server","core","worker"]) else
         "library" if any(x in n for x in ["sdk","lib","client","common"]) else
         "tool" if any(x in n for x in ["cli","tool","script"]) else "unknown")
    dep_count=int(hashlib.sha256(n.encode()).hexdigest()[:4],16)%20+1
    return {"id":repo["id"],"language":lang,"classification":cls,
            "classificationRationale":{"decision":f"stub:{cls}"},"dependencyCount":dep_count,
            "dependencyNames":[],"overlapScore":overlap,"cloneDurationMs":None,
            "analysisDurationMs":None,"error":None}
