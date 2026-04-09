from __future__ import annotations

from pathlib import Path

from hyperflow.engine.replay import replay_trace
from tests._runtime_freeze import build_runtime_snapshot


def test_trace_replay_roundtrip(monkeypatch, tmp_path: Path) -> None:
    snapshot = build_runtime_snapshot(monkeypatch, tmp_path)
    replayed = replay_trace(snapshot['trace'])
    assert replayed == snapshot['result']
