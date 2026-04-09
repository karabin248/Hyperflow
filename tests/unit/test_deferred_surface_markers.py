"""test_deferred_surface_markers.py — Verify deferred surfaces are properly gated.

Routes and modules declared as DEFERRED must:
  - carry an explicit DEFERRED docstring / comment
  - NOT be mounted in the canonical create_app()
  - expose promotion requirements in platform_surface docs
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def _normalized(relative_path: str) -> str:
    return " ".join((REPO_ROOT / relative_path).read_text().split()).lower()


def test_agents_route_module_is_marked_deferred() -> None:
    """routes_agents.py must carry an explicit DEFERRED docstring."""
    text = _normalized("hyperflow/api/routes_agents.py")
    assert "deferred" in text
    assert "not mounted in the canonical mvp app" in text


def test_workflows_route_module_is_marked_deferred() -> None:
    """routes_workflows.py must carry an explicit DEFERRED docstring."""
    text = _normalized("hyperflow/api/routes_workflows.py")
    assert "deferred" in text
    assert "not mounted in the canonical mvp app" in text


def test_deferred_routes_not_mounted_in_canonical_app() -> None:
    """create_app() must NOT include agents or workflows routers."""
    text = _normalized("hyperflow/api/edde_api.py")
    # The canonical app must not include_router for deferred surfaces
    assert "routes_agents" not in text
    assert "routes_workflows" not in text
    assert "agents_router" not in text
    assert "workflows_router" not in text


def test_worker_metadata_module_exposes_live_worker_registry() -> None:
    text = _normalized("hyperflow/platform/workers/__init__.py")
    assert "register_default_workers" in text
    assert "list_live_worker_specs" in text
    assert "worker_handlers" in text


def test_platform_surface_doc_requires_explicit_promotion() -> None:
    text = _normalized("docs/architecture/platform_surface.md")
    assert "deferred donor/product surface" in text
    assert "explicit promotion decision" in text
