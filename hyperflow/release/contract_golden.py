from __future__ import annotations

import json
from importlib import resources
from typing import Any

CONTRACT_GOLDEN_FILE = "runtime_contract_health_check.json"



def _normalize_action_route(route: dict[str, Any]) -> dict[str, Any]:
    return {
        "emoji": route.get("emoji"),
        "action_id": route.get("action_id"),
        "command": route.get("command"),
        "safe_to_execute": route.get("safe_to_execute"),
    }



def normalize_contract_for_golden(contract: dict[str, Any]) -> dict[str, Any]:
    parser = contract.get("parser", {})
    runtime = contract.get("runtime", {})
    output = contract.get("output", {})
    payload = output.get("payload", {})

    return {
        "schema": contract.get("schema"),
        "contract_version": contract.get("contract_version"),
        "status": contract.get("status"),
        "input": {
            "emoji_run": contract.get("input", {}).get("emoji_run"),
            "core_text": contract.get("input", {}).get("core_text"),
        },
        "parser": {
            "matched_combo": parser.get("matched_combo"),
            "primary_name": parser.get("primary_name"),
            "primary_match_type": parser.get("primary_match_type"),
            "primary_status": parser.get("primary_status"),
            "resolved_mps_mode": parser.get("resolved_mps_mode"),
            "resolved_edde_phase": parser.get("resolved_edde_phase", []),
            "resolved_output_types": parser.get("resolved_output_types", []),
            "resolved_output_subtypes": parser.get("resolved_output_subtypes", []),
            "action_routes": [_normalize_action_route(item) for item in parser.get("action_routes", [])],
            "action_route_errors": parser.get("action_route_errors", []),
            "resolution_policy": parser.get("resolution_policy"),
            "parser_decisions": parser.get("parser_decisions", []),
        },
        "timeline": [
            {
                "phase": step.get("phase"),
                "next_step": step.get("next_step"),
                "constraints": {
                    "safe": step.get("constraints", {}).get("safe"),
                    "sandboxed": step.get("constraints", {}).get("sandboxed"),
                    "llm_no_direct_ffi": step.get("constraints", {}).get("llm_no_direct_ffi"),
                },
            }
            for step in contract.get("timeline", [])
        ],
        "runtime": {
            "flow": runtime.get("flow", []),
            "pipeline_path": runtime.get("pipeline_path", []),
            "pipeline_stage_map": runtime.get("pipeline_stage_map", {}),
            "observer": runtime.get("observer", {}),
            "mps": {
                "level": runtime.get("mps", {}).get("level"),
                "risk_level": runtime.get("mps", {}).get("risk_level"),
                "profile": {
                    "name": runtime.get("mps", {}).get("profile", {}).get("name"),
                    "execution_policy": runtime.get("mps", {}).get("profile", {}).get("execution_policy"),
                },
            },
        },
        "output": {
            "kind": output.get("kind"),
            "payload": {
                "intent": payload.get("intent"),
                "mode": payload.get("mode"),
                "observer_status": payload.get("observer_status"),
                "output_subtype": payload.get("output_subtype"),
            },
        },
        "errors": contract.get("errors", []),
    }



def load_contract_golden() -> dict[str, Any]:
    resource = resources.files("hyperflow.resources.contracts").joinpath(CONTRACT_GOLDEN_FILE)
    return json.loads(resource.read_text(encoding="utf-8"))
