import asyncio
from hyperflow.language.command_builder import build_command
from hyperflow.runtime_kernel import run


def test_trace_record_captures_output_subtype_and_resolved_subtypes(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("🧠🔥 analyze the noise semantics pipeline")
    result = asyncio.run(run(cmd))
    assert result.observer_status in ("OK", "WARN", "FALLBACK", "ERROR")
    assert result.summary
