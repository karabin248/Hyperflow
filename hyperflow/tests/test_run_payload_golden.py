from __future__ import annotations

from hyperflow.engine.runtime_kernel import run
from hyperflow.language.command_builder import build_command
from hyperflow.output.run_payload import serialize_run_payload


def test_run_payload_golden_shape() -> None:
    command = build_command("🌈💎🔥🧠🔀⚡ Task: prepare an MVP rollout plan")
    result = run(command)
    payload = serialize_run_payload(command, result)

    snapshot = {
        "keys": list(payload.keys()),
        "command": {
            "intent": payload["command"]["intent"],
            "mode": payload["command"]["mode"],
            "output_type": payload["command"]["output_type"],
            "matched_combo": payload["command"]["parser_trace"]["matched_combo"],
            "tokens": payload["command"]["tokens"],
        },
        "result": {
            "kind": payload["result"]["kind"],
            "intent": payload["result"]["intent"],
            "mode": payload["result"]["mode"],
            "confidence": payload["result"]["confidence"],
            "observer_status": payload["result"]["observer_status"],
            "output_subtype": payload["result"]["output_subtype"],
        },
        "contract": {
            "schema": payload["contract"]["schema"],
            "status": payload["contract"]["status"],
        },
        "run_id_matches": payload["run_id"] == payload["result"]["run_id"] == payload["contract"]["trace_id"],
    }

    assert snapshot == {
        "keys": ["command", "intent", "mode", "output_type", "result", "run_id", "contract"],
        "command": {
            "intent": "planning",
            "mode": "fusion",
            "output_type": "plan",
            "matched_combo": "🌈💎🔥🧠🔀⚡",
            "tokens": ["🌈", "💎", "🔥", "🧠", "🔀", "⚡"],
        },
        "result": {
            "kind": "plan",
            "intent": "planning",
            "mode": "fusion",
            "confidence": "high",
            "observer_status": "OK",
            "output_subtype": "plan",
        },
        "contract": {
            "schema": "hyperflow/edde-contract/v1",
            "status": "ok",
        },
        "run_id_matches": True,
    }
