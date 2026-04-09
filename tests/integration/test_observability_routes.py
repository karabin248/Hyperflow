from __future__ import annotations

import json
from pathlib import Path

import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from hyperflow.api.edde_api import app
from hyperflow.memory.traces import append_trace



def test_logs_and_checkpoints_routes_reflect_canonical_storage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)

    append_trace(
        {
            'run_id': 'r-001',
            'timestamp': '2026-03-22T10:00:00+00:00',
            'intent': 'analysis',
            'mode': 'analysis',
            'observer_status': 'OK',
            'confidence': 'high',
            'summary': 'inventory route smoke',
        }
    )

    checkpoint_dir = tmp_path / 'storage' / 'checkpoints'
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_payload = {
        'generated_at': '2026-03-22T10:05:00+00:00',
        'version': '0.2.0',
        'status': 'stable-operational',
        'development_phase': 'structured-operational',
        'dominant_work_style': 'planning-fusion',
        'dominant_intent': 'planning',
        'dominant_mode': 'fusion',
        'core_operating_kernel': ['perceive', 'extract_core', 'set_direction', 'synthesize', 'generate_options', 'choose'],
        'satellite_modes': ['analysis'],
    }
    (checkpoint_dir / 'cp-alpha.json').write_text(json.dumps(checkpoint_payload), encoding='utf-8')

    client = TestClient(app)

    logs = client.get('/v1/logs/recent')
    assert logs.status_code == 200
    assert logs.json()['items'][0]['run_id'] == 'r-001'

    checkpoints = client.get('/v1/checkpoints')
    assert checkpoints.status_code == 200
    items = checkpoints.json()['items']
    assert len(items) == 1
    assert items[0]['file_name'] == 'cp-alpha.json'
    assert items[0]['checkpoint_id'] == 'cp-alpha'

    latest = client.get('/v1/checkpoints/latest')
    assert latest.status_code == 200
    assert latest.json()['file_name'] == 'cp-alpha.json'

    single = client.get('/v1/checkpoints/cp-alpha')
    assert single.status_code == 200
    assert single.json()['version'] == '0.2.0'
