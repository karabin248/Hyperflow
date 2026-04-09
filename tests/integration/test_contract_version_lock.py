import asyncio
from hyperflow.language.command_builder import build_command
from hyperflow.runtime_kernel import run

EXPECTED_SCHEMA = "hyperflow/edde-contract/v1"


def test_runtime_contract_version_is_emitted_across_output_and_contract(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("🧠🔥 contract version lock test")
    result = asyncio.run(run(cmd))
    assert result.edde_contract["schema"] == EXPECTED_SCHEMA
    assert result.contract_version == result.edde_contract["contract_version"]


def test_contract_version_drift_requires_explicit_bump(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("contract drift check")
    result = asyncio.run(run(cmd))
    assert result.edde_contract["schema"] == EXPECTED_SCHEMA
