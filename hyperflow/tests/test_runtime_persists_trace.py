from pathlib import Path

from hyperflow.engine.runtime_kernel import run
from hyperflow.language.command_builder import build_command
from hyperflow.memory.traces import load_recent_traces


def test_runtime_creates_persistent_trace():
    raw = (
        "🌈💎🔥🧠🔀⚡ "
        "Task: create a Hyperflow MVP build plan "
        "Goal: extract module order "
        "Format: sections + priorities"
    )

    command = build_command(raw)
    result = run(command)

    recent = load_recent_traces(limit=1)

    assert result.intent == "planning"
    assert len(recent) >= 1
    assert recent[0]["intent"] == "planning"