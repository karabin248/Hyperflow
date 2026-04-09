from __future__ import annotations

from pathlib import Path

from hyperflow.contracts.runtime_invariants import scan_for_unauthorized_extension_paths
from hyperflow.engine.runtime_kernel import run as engine_run
from hyperflow.runtime_kernel import run as public_run


def _read(path: str) -> str:
    root = Path(__file__).resolve().parents[1]
    return (root / path).read_text(encoding='utf-8')


def test_single_runtime_entrypoint_is_enforced() -> None:
    assert public_run is engine_run
    repo_root = Path(__file__).resolve().parents[1]
    assert scan_for_unauthorized_extension_paths(repo_root) == []


def test_cli_and_api_reference_the_same_runtime_spine() -> None:
    cli_source = _read('hyperflow/interface/cli.py')
    api_source = _read('hyperflow/api/edde_api.py')
    assert 'from hyperflow.runtime_kernel import run' in cli_source
    assert 'from hyperflow.runtime_kernel import run' in api_source
