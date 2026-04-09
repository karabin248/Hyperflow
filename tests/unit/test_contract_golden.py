import asyncio
import pytest
from hyperflow.language.command_builder import build_command
from hyperflow.runtime_kernel import run

GOLDEN_CONTRACT_KEYS = {
    "schema", "run_id", "intent", "mode", "output_type",
    "mps_level", "mps_state", "observer_status", "timeline",
    "graph_snapshot", "safe_constraint",
}


def test_edde_contract_golden_shape(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("🧠🔥🌈💎 contract golden shape")
    result = asyncio.run(run(cmd))
    contract = result.edde_contract
    missing = GOLDEN_CONTRACT_KEYS - set(contract.keys())
    assert not missing, f"Contract missing keys: {missing}"


def test_edde_contract_timeline_has_output_phase(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("contract timeline test")
    result = asyncio.run(run(cmd))
    timeline_phases = [t["phase"] for t in result.edde_contract["timeline"]]
    assert "OUTPUT" in timeline_phases
