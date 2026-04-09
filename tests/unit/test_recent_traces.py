import json
from pathlib import Path

from hyperflow.memory.traces import append_trace, load_recent_traces


def test_load_recent_traces(tmp_path: Path):
    trace_file = tmp_path / "traces.jsonl"

    append_trace(
        {
            "run_id": "r1",
            "timestamp": "2026-03-14T10:00:00+00:00",
            "intent": "analysis",
            "mode": "standard",
            "observer_status": "OK",
            "confidence": "medium",
            "summary": "first",
        },
        trace_file,
    )

    append_trace(
        {
            "run_id": "r2",
            "timestamp": "2026-03-14T10:01:00+00:00",
            "intent": "planning",
            "mode": "fusion",
            "observer_status": "OK",
            "confidence": "high",
            "summary": "second",
        },
        trace_file,
    )

    recent = load_recent_traces(limit=2, file_path=trace_file)

    assert len(recent) == 2
    assert recent[0]["run_id"] == "r2"
    assert recent[1]["run_id"] == "r1"