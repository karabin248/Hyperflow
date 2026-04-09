from __future__ import annotations

from pathlib import Path

import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from hyperflow.api.edde_api import app


def test_post_run_creates_run_linked_checkpoint(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    client = TestClient(app)

    response = client.post('/v1/run', json={'prompt': '🌈💎🔥🧠🔀⚡ Task: validate checkpoint linkage'})
    assert response.status_code == 200
    run_id = response.json()['run_id']

    listing = client.get('/v1/checkpoints')
    assert listing.status_code == 200
    items = listing.json()['items']
    assert items, 'expected at least one checkpoint after /v1/run'
    assert any(item['run_id'] == run_id for item in items)

    by_run = client.get(f'/v1/checkpoints/{run_id}')
    assert by_run.status_code == 200
    checkpoint = by_run.json()
    assert checkpoint['run_id'] == run_id
    assert checkpoint['checkpoint_id'] == run_id
