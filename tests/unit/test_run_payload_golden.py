import asyncio
import json
import pytest
from pathlib import Path
from hyperflow.language.command_builder import build_command
from hyperflow.runtime_kernel import run
from hyperflow.output.run_payload import serialize_run_payload

GOLDEN_KEYS_COMMAND = {"intent", "mode", "output_type", "intensity", "tokens", "operations", "raw_input"}
GOLDEN_KEYS_RESULT = {"run_id", "summary", "confidence", "observer_status", "next_step", "plan", "insights", "actions"}


def test_run_payload_golden_shape(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("🧠🔥🌈 golden payload shape check")
    result = asyncio.run(run(cmd))
    payload = serialize_run_payload(cmd, result)
    assert GOLDEN_KEYS_COMMAND.issubset(payload["command"].keys())
    assert GOLDEN_KEYS_RESULT.issubset(payload["result"].keys())


def test_run_payload_is_json_serializable(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("json serialization check")
    result = asyncio.run(run(cmd))
    payload = serialize_run_payload(cmd, result)
    serialized = json.dumps(payload)
    assert len(serialized) > 10


def test_run_payload_contract_section_present(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("contract section check")
    result = asyncio.run(run(cmd))
    payload = serialize_run_payload(cmd, result)
    assert "contract" in payload
    assert payload["contract"]["schema"] == "hyperflow/edde-contract/v1"
