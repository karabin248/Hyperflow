from __future__ import annotations
import asyncio
import json
import os
from pathlib import Path
from hyperflow.language.command_builder import build_command
from hyperflow.runtime_kernel import run
from hyperflow.output.run_payload import serialize_run_payload
from hyperflow.memory.knowledge_store import save_knowledge_object


def test_knowledge_store_and_trace(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("🧠🔥 knowledge store test")
    result = asyncio.run(run(cmd))
    payload = serialize_run_payload(cmd, result)
    assert payload["result"]["run_id"] == result.run_id


def test_runtime_persists_top_level_contract_in_knowledge_store(tmp_path, monkeypatch) -> None:
    storage = tmp_path / "storage"
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(storage))
    cmd = build_command("🧠 persist contract to knowledge store")
    result = asyncio.run(run(cmd))
    assert result.edde_contract["schema"] == "hyperflow/edde-contract/v1"
