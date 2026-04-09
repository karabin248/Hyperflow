import asyncio
from hyperflow.language.command_builder import build_command
from hyperflow.runtime_kernel import run
from hyperflow.memory.traces import load_recent_traces


def test_runtime_persists_trace_after_run(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("🧠🔥 trace persistence check")
    result = asyncio.run(run(cmd))
    traces = load_recent_traces(limit=5)
    run_ids = [t.get("run_id") for t in traces]
    assert result.run_id in run_ids, "runtime must persist a trace record for the run_id"
