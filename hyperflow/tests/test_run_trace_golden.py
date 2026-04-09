from __future__ import annotations

import json
from pathlib import Path
from datetime import UTC, datetime

from hyperflow.runtime_kernel import run
from hyperflow.language.command_builder import build_command
from hyperflow.memory import traces as traces_module
from hyperflow.engine import runtime_state as runtime_state_module
from hyperflow.memory.traces import load_recent_traces


class _FrozenDateTime:
    @classmethod
    def now(cls, tz=None):
        return datetime(2026, 3, 29, 0, 0, 0, tzinfo=UTC)


def test_run_trace_golden_freeze(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv('HYPERFLOW_STORAGE_DIR', str(tmp_path / 'storage'))
    monkeypatch.setattr(runtime_state_module, 'uuid4', lambda: 'run-trace-freeze-001')
    monkeypatch.setattr(traces_module, 'datetime', _FrozenDateTime)

    prompt = '🌈💎🔥🧠🔀⚡ Task: prepare an MVP rollout plan'
    command = build_command(prompt)
    result = run(command)

    traces = load_recent_traces(limit=5)
    trace = next((t for t in traces if t.get('run_id') == result.run_id), None)
    assert trace is not None, 'runtime must persist a trace record for the run_id'

    expected = json.loads((Path(__file__).resolve().parents[2] / 'tests' / 'golden' / 'run_trace_freeze.json').read_text(encoding='utf-8'))
    assert trace == expected
