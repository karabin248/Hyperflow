from __future__ import annotations

import json
from pathlib import Path

from tests._runtime_freeze import build_runtime_snapshot


def test_run_deterministic_golden(monkeypatch, tmp_path: Path) -> None:
    expected = json.loads((Path(__file__).resolve().parent / 'golden' / 'run_full_freeze.json').read_text(encoding='utf-8'))
    actual = build_runtime_snapshot(monkeypatch, tmp_path)
    assert actual == expected


def test_run_deterministic_snapshot_is_stable_across_fresh_runs(monkeypatch, tmp_path: Path) -> None:
    first = build_runtime_snapshot(monkeypatch, tmp_path / 'first')
    second = build_runtime_snapshot(monkeypatch, tmp_path / 'second')
    third = build_runtime_snapshot(monkeypatch, tmp_path / 'third')
    assert first == second == third
