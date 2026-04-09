from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

import hyperflow.engine.runtime_state as runtime_state_module
import hyperflow.memory.traces as traces_module
from hyperflow.language.command_builder import build_command
from hyperflow.memory.traces import load_recent_traces
from hyperflow.runtime_kernel import run

FROZEN_RUN_ID = 'run-full-freeze-001'
FROZEN_TRACE_RUN_ID = 'run-trace-freeze-001'
FROZEN_TIMESTAMP = datetime(2026, 3, 29, 0, 0, 0, tzinfo=UTC)
DEFAULT_PROMPT = '🌈💎🔥🧠🔀⚡ Task: prepare an MVP rollout plan'


class FrozenDateTime:
    @classmethod
    def now(cls, tz=None):
        return FROZEN_TIMESTAMP


def build_runtime_snapshot(monkeypatch, tmp_path: Path, *, prompt: str = DEFAULT_PROMPT, run_id: str = FROZEN_RUN_ID) -> dict:
    monkeypatch.setenv('HYPERFLOW_STORAGE_DIR', str(tmp_path / 'storage'))
    monkeypatch.setattr(runtime_state_module, 'uuid4', lambda: run_id)
    monkeypatch.setattr(traces_module, 'datetime', FrozenDateTime)

    command = build_command(prompt)
    result = run(command)
    traces = load_recent_traces(limit=5)
    trace = next((item for item in traces if item.get('run_id') == result.run_id), None)
    assert trace is not None, 'runtime must persist a replayable trace record'

    return {
        'command': asdict(command),
        'result': result.to_dict(),
        'trace': trace,
    }
