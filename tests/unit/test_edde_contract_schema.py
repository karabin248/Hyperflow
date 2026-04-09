import asyncio
import pytest
from hyperflow.language.command_builder import build_command
from hyperflow.runtime_kernel import run


def test_runtime_attaches_valid_edde_contract(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("🧠🔥 edde contract schema test")
    result = asyncio.run(run(cmd))
    contract = result.edde_contract
    assert contract["schema"] == "hyperflow/edde-contract/v1"
    assert contract.get("run_id")
    assert contract.get("intent")
    assert contract.get("timeline")


def test_runtime_contract_includes_mps_and_graph_context(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("💎🧠 mps and graph context check")
    result = asyncio.run(run(cmd))
    contract = result.edde_contract
    assert contract.get("mps_level") is not None
    assert contract.get("graph_snapshot") is not None


def test_runtime_contract_safe_constraint_tracks_safe_mode_flag(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("safe mode contract check")
    result = asyncio.run(run(cmd))
    contract = result.edde_contract
    assert "safe_constraint" in contract
