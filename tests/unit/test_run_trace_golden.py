import asyncio
import json
import pytest
from pathlib import Path
from hyperflow.language.command_builder import build_command
from hyperflow.runtime_kernel import run
from hyperflow.memory.traces import load_recent_traces


def test_run_trace_golden_freeze(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("🧠🔥🌈 global analysis for trace golden freeze")
    result = asyncio.run(run(cmd))
    traces = load_recent_traces(limit=10)
    run_ids = [t.get("run_id") for t in traces]
    assert result.run_id in run_ids, "runtime must persist a trace record for the run_id"
    trace = next(t for t in traces if t.get("run_id") == result.run_id)
    assert trace.get("intent")
    assert trace.get("summary")
    assert trace.get("observer_status")
