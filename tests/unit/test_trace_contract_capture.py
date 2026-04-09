import asyncio
from hyperflow.language.command_builder import build_command
from hyperflow.engine.runtime_state import init_runtime_state
from hyperflow.runtime_kernel import run


def test_trace_record_captures_v1_contract_phase_and_next_step(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("🧠🔥 analyze the pipeline architecture")
    result = asyncio.run(run(cmd))
    contract = result.edde_contract
    assert contract["schema"] == "hyperflow/edde-contract/v1"
    timeline_phases = [t["phase"] for t in contract["timeline"]]
    assert "OUTPUT" in timeline_phases
