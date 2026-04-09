from __future__ import annotations

import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from hyperflow.api.edde_api import app



def test_api_run_contract_is_canonical() -> None:
    client = TestClient(app)
    response = client.post('/v1/run', json={'prompt': '🌈💎🔥🧠🔀⚡ Task: prepare an MVP rollout plan'})
    assert response.status_code == 200

    payload = response.json()
    assert list(payload.keys()) == ['run_id', 'intent', 'mode', 'output_type', 'result', 'contract']
    assert 'edde_contract' not in payload
    assert payload['contract']['schema'] == 'hyperflow/edde-contract/v1'
    assert payload['run_id'] == payload['result']['run_id'] == payload['contract']['trace_id']
