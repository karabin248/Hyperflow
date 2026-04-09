from __future__ import annotations

import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

import hyperflow.api.edde_api as edde_api
from hyperflow.version import __version__


def test_api_rejects_missing_prompt() -> None:
    client = TestClient(edde_api.app)
    response = client.post("/v1/run", json={})
    assert response.status_code == 422


def test_api_rejects_empty_prompt() -> None:
    client = TestClient(edde_api.app)
    response = client.post("/v1/run", json={"prompt": "   "})
    assert response.status_code == 400
    assert "Input is required" in response.json()["detail"]


def test_create_app_requires_fastapi(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(edde_api, "FastAPI", None)
    with pytest.raises(ModuleNotFoundError, match="FastAPI is required"):
        edde_api.create_app()


def test_health_reports_current_version() -> None:
    client = TestClient(edde_api.app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "hyperflow", "version": __version__}
