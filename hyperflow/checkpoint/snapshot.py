from datetime import datetime, UTC
from pathlib import Path
import json

from hyperflow.memory.status_report import build_status_report
from hyperflow.memory.self_profile import build_self_profile
from hyperflow.memory.graph_reasoning import reason_over_graph
from hyperflow.memory.traces import load_recent_traces


def _list_python_modules(root: Path) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {}

    for section in ["engine", "memory", "output", "interface", "language", "control", "schemas"]:
        section_path = root / section
        if not section_path.exists():
            continue

        items = []
        for file in sorted(section_path.glob("*.py")):
            if file.name == "__init__.py":
                continue
            items.append(file.stem)

        buckets[section] = items

    return buckets



def _infer_recent_run_context(limit_runs: int = 10) -> dict[str, str]:
    traces = load_recent_traces(limit=limit_runs)
    if not traces:
        return {}
    latest = traces[0]
    payload: dict[str, str] = {}
    run_id = str(latest.get("run_id", "") or "").strip()
    timestamp = str(latest.get("timestamp", "") or "").strip()
    if run_id:
        payload["run_id"] = run_id
    if timestamp:
        payload["trace_timestamp"] = timestamp
    return payload



def build_architecture_snapshot(limit_runs: int = 10) -> dict:
    package_root = Path(__file__).resolve().parents[1]

    status = build_status_report(limit_runs=limit_runs)
    profile = build_self_profile(limit_runs=limit_runs)
    reasoning = reason_over_graph(limit_runs=limit_runs)

    snapshot = {
        "system_name": "Hyperflow",
        "version": status.get("version") or "",
        "generated_at": datetime.now(UTC).isoformat(),
        "development_phase": status.get("development_phase") or "",
        "status": status.get("status") or "",
        "dominant_work_style": profile.get("dominant_work_style") or "",
        "dominant_intent": status.get("dominant_intent") or "",
        "dominant_mode": status.get("dominant_mode") or "",
        "core_operating_kernel": profile.get("core_operating_kernel") or [],
        "satellite_modes": profile.get("satellite_modes") or [],
        "reasoning_findings": reasoning.get("findings") or [],
        "modules": _list_python_modules(package_root),
        "capabilities": [
            "command parsing",
            "planning",
            "analysis",
            "persistent traces",
            "graph memory",
            "graph analytics",
            "graph reasoning",
            "self profile",
            "status report",
            "pretty cli output",
        ],
        "narrative_summary": profile["narrative_summary"],
    }
    snapshot.update(_infer_recent_run_context(limit_runs=limit_runs))

    return snapshot



def save_architecture_snapshot(output_path: str, limit_runs: int = 10) -> dict:
    snapshot = build_architecture_snapshot(limit_runs=limit_runs)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    snapshot.setdefault("checkpoint_id", path.stem)
    path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    return snapshot
