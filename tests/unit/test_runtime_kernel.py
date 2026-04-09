import asyncio
import pytest
from hyperflow.language.command_builder import build_command
from hyperflow.runtime_kernel import run
from hyperflow.schemas.command_schema import CommandObject


def test_runtime_kernel_end_to_end(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("🧠🔥🌈 analyze global architecture")
    result = asyncio.run(run(cmd))
    assert result.intent
    assert result.summary
    assert result.run_id
    assert result.observer_status
    assert result.edde_contract["schema"] == "hyperflow/edde-contract/v1"


def test_runtime_kernel_rejects_non_command_object() -> None:
    with pytest.raises(ValueError, match="CommandObject"):
        asyncio.run(run("not a command object"))  # type: ignore[arg-type]


def test_runtime_kernel_returns_llm_source(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("analyze the kernel LLM source field")
    result = asyncio.run(run(cmd))
    assert hasattr(result, "llm_source")
    assert result.llm_source in ("llm", "stub")
