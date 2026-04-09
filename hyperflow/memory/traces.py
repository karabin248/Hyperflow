from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from hyperflow.config import get_config_versions
from hyperflow.contracts.version_policy import CONTRACT_VERSION
from hyperflow.runtime_paths import get_trace_file


def _extract_contract_trace_fields(contract: Any) -> tuple[str, str]:
    if not isinstance(contract, dict):
        return "", ""

    if contract.get("schema") == "hyperflow/edde-contract/v1":
        timeline = contract.get("timeline")
        if isinstance(timeline, list) and timeline:
            last_step = timeline[-1] if isinstance(timeline[-1], dict) else {}
            phase = str(last_step.get("phase", "") or "")
            next_step = str(last_step.get("next_step", "") or "")
            return phase, next_step
        return "", ""

    phase = contract.get("phase")
    next_step = contract.get("next_step")
    return str(phase or ""), str(next_step or "")


def build_trace_record(
    run_id: str,
    command: Any,
    result: Any,
) -> dict:
    parser_trace = getattr(command, "parser_trace", {}) or {}
    edde_phase, edde_next_step = _extract_contract_trace_fields(getattr(result, "edde_contract", {}))
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "contract_version": CONTRACT_VERSION,
        "run_id": run_id,
        "raw_input": command.raw_input,
        "intent": command.intent,
        "mode": command.mode,
        "output_type": command.output_type,
        "output_subtype": getattr(command, "output_subtype", ""),
        "intensity": command.intensity,
        "observer_status": result.observer_status,
        "threshold_status": getattr(result, "observer_contract", {}).get("status", "OK"),
        "confidence": result.confidence,
        "summary": result.summary,
        "next_step": result.next_step,
        "matched_combo": parser_trace.get("matched_combo"),
        "matched_preset": parser_trace.get("matched_preset"),
        "resolved_mps_mode": parser_trace.get("resolved_mps_mode"),
        "resolved_edde_phase": parser_trace.get("resolved_edde_phase", []),
        "resolved_output_types": parser_trace.get("resolved_output_types", []),
        "resolved_output_subtypes": parser_trace.get("resolved_output_subtypes", []),
        "resolution_policy": parser_trace.get("resolution_policy"),
        "parser_decisions": parser_trace.get("parser_decisions", []),
        "primary_status": parser_trace.get("primary_status"),
        "action_route_ids": [item.get("action_id") for item in parser_trace.get("action_routes", [])],
        "action_route_errors": parser_trace.get("action_route_errors", []),
        "edde_phase": edde_phase,
        "edde_next_step": edde_next_step,
        "config_versions": get_config_versions(),
        "replay_contract_version": CONTRACT_VERSION,
        "replay_output": result.to_dict(),
    }


def append_trace(trace: dict, file_path: Path | None = None) -> Path:
    target = file_path or get_trace_file()
    target.parent.mkdir(parents=True, exist_ok=True)

    with target.open("a", encoding="utf-8") as f:
        f.write(json.dumps(trace, ensure_ascii=False) + "\n")

    return target


def load_recent_traces(limit: int = 5, file_path: Path | None = None) -> list[dict]:
    target = file_path or get_trace_file()

    if not target.exists():
        return []

    lines = target.read_text(encoding="utf-8").splitlines()
    parsed = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            parsed.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    return parsed[-limit:][::-1]
