from __future__ import annotations

from pathlib import Path

import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from hyperflow.api.edde_api import app
from hyperflow.checkpoint.snapshot import save_architecture_snapshot
from hyperflow.memory.traces import append_trace


def test_checkpoint_lookup_supports_stable_checkpoint_and_run_identity(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)

    append_trace(
        {
            'run_id': 'r-002',
            'timestamp': '2026-03-22T10:10:00+00:00',
            'intent': 'analysis',
            'mode': 'analysis',
            'observer_status': 'OK',
            'confidence': 'high',
            'summary': 'checkpoint identity smoke',
        }
    )
    save_architecture_snapshot('storage/checkpoints/cp-beta.json', limit_runs=1)

    client = TestClient(app)
    listing = client.get('/v1/checkpoints')
    assert listing.status_code == 200
    item = listing.json()['items'][0]
    assert item['checkpoint_id'] == 'cp-beta'
    assert item['run_id'] == 'r-002'

    by_checkpoint = client.get('/v1/checkpoints/cp-beta')
    assert by_checkpoint.status_code == 200
    assert by_checkpoint.json()['checkpoint_id'] == 'cp-beta'

    by_run = client.get('/v1/checkpoints/r-002')
    assert by_run.status_code == 200
    assert by_run.json()['run_id'] == 'r-002'
