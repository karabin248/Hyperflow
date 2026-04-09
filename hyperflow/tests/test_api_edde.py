import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from hyperflow.api.edde_api import app


def test_api_health_and_run_endpoints_work():
    client = TestClient(app)

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    response = client.post("/v1/run", json={"prompt": "🧭 make a checklist for launch risks"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "planning"
    assert payload["run_id"]
    assert payload["contract"]["schema"] == "hyperflow/edde-contract/v1"
    assert payload["result"]["summary"]
    assert payload["result"]["plan"]
