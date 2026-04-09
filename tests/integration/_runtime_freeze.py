import asyncio
from hyperflow.language.command_builder import build_command
from hyperflow.runtime_kernel import run
from hyperflow.output.run_payload import serialize_run_payload


def build_runtime_snapshot(prompt: str, tmp_path, monkeypatch) -> dict:
    """Helper: run the full pipeline and return a serialized payload snapshot."""
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command(prompt)
    result = asyncio.run(run(cmd))
    return serialize_run_payload(cmd, result)
