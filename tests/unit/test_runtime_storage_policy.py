import asyncio
import pytest
from pathlib import Path
from hyperflow.language.command_builder import build_command
from hyperflow.runtime_kernel import run


def test_storage_dir_env_var_controls_output_location(tmp_path, monkeypatch) -> None:
    custom_dir = tmp_path / "custom_storage"
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(custom_dir))
    cmd = build_command("analyze the storage policy")
    result = asyncio.run(run(cmd))
    assert result.run_id
    assert result.summary


def test_run_succeeds_without_storage_dir(monkeypatch) -> None:
    monkeypatch.delenv("HYPERFLOW_STORAGE_DIR", raising=False)
    cmd = build_command("analyze without storage")
    result = asyncio.run(run(cmd))
    assert result.run_id
    assert result.summary


def test_storage_dir_can_be_switched_between_runs(tmp_path, monkeypatch) -> None:
    dir_a = tmp_path / "storage_a"
    dir_b = tmp_path / "storage_b"
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(dir_a))
    r1 = asyncio.run(run(build_command("run in storage_a")))
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(dir_b))
    r2 = asyncio.run(run(build_command("run in storage_b")))
    assert r1.run_id != r2.run_id
