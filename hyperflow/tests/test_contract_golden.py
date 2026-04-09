from __future__ import annotations

from hyperflow.engine.runtime_kernel import run
from hyperflow.language.command_builder import build_command


def test_edde_contract_golden_shape() -> None:
    command = build_command("🌈💎🔥🧠🔀⚡ Task: prepare an MVP rollout plan")
    result = run(command)
    contract = result.edde_contract

    snapshot = {
        "schema": contract["schema"],
        "status": contract["status"],
        "emoji_run": contract["input"]["emoji_run"],
        "timeline": [
            {
                "phase": step["phase"],
                "next_step": step["next_step"],
                "constraint_keys": sorted(step["constraints"].keys()),
            }
            for step in contract["timeline"]
        ],
        "runtime": {
            "pipeline_path": contract["runtime"]["pipeline_path"],
            "pipeline_stage_keys": sorted(contract["runtime"]["pipeline_stage_map"].keys()),
            "mps_level": contract["runtime"]["mps"]["level"],
            "output_kind": contract["output"]["kind"],
            "output_payload_has_contract": "edde_contract" in contract["output"]["payload"],
        },
    }

    assert snapshot == {
        "schema": "hyperflow/edde-contract/v1",
        "status": "ok",
        "emoji_run": "🌈💎🔥🧠🔀⚡",
        "timeline": [
            {"phase": "DECIDE", "next_step": "DO", "constraint_keys": ["llm_no_direct_ffi", "safe", "sandboxed"]},
            {"phase": "DO", "next_step": "OUTPUT", "constraint_keys": ["llm_no_direct_ffi", "safe", "sandboxed"]},
            {"phase": "OUTPUT", "next_step": "DECIDE", "constraint_keys": ["llm_no_direct_ffi", "safe", "sandboxed"]},
        ],
        "runtime": {
            "pipeline_path": ["scan", "extract", "cluster", "interpret", "orchestrate", "remix", "output"],
            "pipeline_stage_keys": ["discover", "do", "evaluate", "extract"],
            "mps_level": 6,
            "output_kind": "plan",
            "output_payload_has_contract": False,
        },
    }
