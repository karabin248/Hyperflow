from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from hyperflow.runtime_paths import get_checkpoint_dir


def _safe_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []



def _derive_checkpoint_id(item: dict[str, Any]) -> str:
    explicit = str(item.get("checkpoint_id", "") or "").strip()
    if explicit:
        return explicit
    file_name = str(item.get("_file_name", "") or "").strip()
    if file_name:
        return Path(file_name).stem
    return ""



def _derive_run_id(item: dict[str, Any]) -> str:
    for key in ("run_id", "trace_id"):
        value = str(item.get(key, "") or "").strip()
        if value:
            return value
    return ""



def _load_checkpoint(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["_file_name"] = path.name
    data["_file_path"] = str(path)
    if not data.get("checkpoint_id"):
        data["checkpoint_id"] = path.stem
    if not data.get("run_id") and data.get("trace_id"):
        data["run_id"] = data["trace_id"]
    return data



def _sort_key(item: dict[str, Any]) -> str:
    return str(item.get("generated_at", ""))



def _simplify_checkpoint(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "checkpoint_id": _derive_checkpoint_id(item),
        "run_id": _derive_run_id(item),
        "file_name": item.get("_file_name", ""),
        "file_path": item.get("_file_path", ""),
        "generated_at": item.get("generated_at", ""),
        "version": item.get("version", ""),
        "status": item.get("status", ""),
        "development_phase": item.get("development_phase", item.get("phase", "")),
        "dominant_work_style": item.get("dominant_work_style", ""),
        "dominant_intent": item.get("dominant_intent", ""),
        "dominant_mode": item.get("dominant_mode", ""),
        "core_operating_kernel": _safe_list(item.get("core_operating_kernel")),
        "satellite_modes": _safe_list(item.get("satellite_modes")),
    }



def _compare_checkpoints(latest: dict[str, Any], previous: dict[str, Any]) -> list[str]:
    findings: list[str] = []

    if latest.get("status") != previous.get("status"):
        findings.append(
            f"Status changed: {previous.get('status', 'unknown')} -> {latest.get('status', 'unknown')}"
        )

    if latest.get("development_phase") != previous.get("development_phase"):
        findings.append(
            "Development phase changed: "
            f"{previous.get('development_phase', 'unknown')} -> {latest.get('development_phase', 'unknown')}"
        )

    if latest.get("dominant_work_style") != previous.get("dominant_work_style"):
        findings.append(
            "Dominant work style changed: "
            f"{previous.get('dominant_work_style', 'unknown')} -> {latest.get('dominant_work_style', 'unknown')}"
        )

    if latest.get("dominant_intent") != previous.get("dominant_intent"):
        findings.append(
            f"Dominant intent changed: {previous.get('dominant_intent', 'unknown')} -> {latest.get('dominant_intent', 'unknown')}"
        )

    if latest.get("dominant_mode") != previous.get("dominant_mode"):
        findings.append(
            f"Dominant mode changed: {previous.get('dominant_mode', 'unknown')} -> {latest.get('dominant_mode', 'unknown')}"
        )

    latest_core = set(_safe_list(latest.get("core_operating_kernel")))
    previous_core = set(_safe_list(previous.get("core_operating_kernel")))

    added_core = sorted(latest_core - previous_core)
    removed_core = sorted(previous_core - latest_core)

    if added_core:
        findings.append(f"Core kernel expanded: {', '.join(added_core)}")
    if removed_core:
        findings.append(f"Core kernel reduced: {', '.join(removed_core)}")

    latest_sat = set(_safe_list(latest.get("satellite_modes")))
    previous_sat = set(_safe_list(previous.get("satellite_modes")))

    added_sat = sorted(latest_sat - previous_sat)
    removed_sat = sorted(previous_sat - latest_sat)

    if added_sat:
        findings.append(f"New satellite modes: {', '.join(added_sat)}")
    if removed_sat:
        findings.append(f"Removed satellite modes: {', '.join(removed_sat)}")

    if not findings:
        findings.append("No major architectural changes detected between the two latest checkpoints.")

    return findings



def _load_all_checkpoints() -> list[dict[str, Any]]:
    checkpoint_dir = get_checkpoint_dir()
    if not checkpoint_dir.exists():
        files: list[Path] = []
    else:
        files = sorted(checkpoint_dir.glob("*.json"))
    raw_items = [_load_checkpoint(path) for path in files]
    raw_items.sort(key=_sort_key, reverse=True)
    return raw_items



def build_checkpoint_history(limit: int = 10) -> dict[str, Any]:
    raw_items = _load_all_checkpoints()

    if limit > 0:
        raw_items = raw_items[:limit]

    timeline = [_simplify_checkpoint(item) for item in raw_items]

    latest = timeline[0] if timeline else None
    previous = timeline[1] if len(timeline) > 1 else None

    if latest and previous:
        evolution = _compare_checkpoints(latest, previous)
    elif latest:
        evolution = ["Only one checkpoint available. Add another checkpoint to enable comparison."]
    else:
        evolution = ["No checkpoints found."]

    return {
        "count": len(timeline),
        "latest": latest,
        "previous": previous,
        "timeline": timeline,
        "evolution": evolution,
    }



def load_checkpoint_by_identity(checkpoint_ref: str) -> dict[str, Any] | None:
    normalized = checkpoint_ref.strip()
    if not normalized:
        return None

    candidates = {normalized}
    if normalized.endswith('.json'):
        candidates.add(Path(normalized).stem)
    else:
        candidates.add(f"{normalized}.json")

    for item in _load_all_checkpoints():
        file_name = str(item.get("_file_name", "") or "")
        file_stem = Path(file_name).stem if file_name else ""
        checkpoint_id = _derive_checkpoint_id(item)
        run_id = _derive_run_id(item)
        identities = {value for value in (file_name, file_stem, checkpoint_id, run_id) if value}
        if identities & candidates:
            return item
    return None
