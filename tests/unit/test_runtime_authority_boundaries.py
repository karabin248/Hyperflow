from __future__ import annotations

from pathlib import Path


def _read(path: str) -> str:
    root = Path(__file__).resolve().parents[2]
    return (root / path).read_text(encoding="utf-8")


def test_canonical_entrypoints_do_not_import_future_layers() -> None:
    entrypoints = {
        "hyperflow/__main__.py": _read("hyperflow/__main__.py"),
        "hyperflow/interface/cli.py": _read("hyperflow/interface/cli.py"),
        "hyperflow/api/edde_api.py": _read("hyperflow/api/edde_api.py"),
        "hyperflow/runtime_kernel.py": _read("hyperflow/runtime_kernel.py"),
        "hyperflow/engine/runtime_kernel.py": _read("hyperflow/engine/runtime_kernel.py"),
    }

    forbidden = ("hyperflow.framework", "hyperflow.platform", "hyperflow.agent_runtime", "hyperflow.extensions")

    for path, content in entrypoints.items():
        for needle in forbidden:
            assert needle not in content, f"{path} must not import {needle}"


def test_module_entry_remains_cli_adapter_only() -> None:
    text = _read("hyperflow/__main__.py")
    assert "from hyperflow.interface.cli import main" in text
    assert "runtime_kernel" not in text


def test_cli_and_api_share_runtime_kernel_authority() -> None:
    cli = _read("hyperflow/interface/cli.py")
    api = _read("hyperflow/api/edde_api.py")
    assert "from hyperflow.runtime_kernel import run" in cli
    assert "from hyperflow.runtime_kernel import run" in api


def test_aux_kernel_helpers_do_not_become_runtime_entrypoint() -> None:
    cli = _read("hyperflow/interface/cli.py")
    api = _read("hyperflow/api/edde_api.py")
    runtime = _read("hyperflow/engine/runtime_kernel.py")

    assert "hyperflow.engine.kernel_execution" not in cli
    assert "hyperflow.engine.kernel_execution" not in api
    assert "hyperflow.engine.kernel_execution" not in runtime


def test_canonical_schema_validation_does_not_import_future_layers() -> None:
    schema = _read("hyperflow/schemas/edde_contract_schema.py")
    assert "hyperflow.framework" not in schema
    assert "hyperflow.agent_runtime" not in schema


def test_trace_and_checkpoint_modules_do_not_import_future_layers() -> None:
    baseline_modules = {
        "hyperflow/memory/traces.py": _read("hyperflow/memory/traces.py"),
        "hyperflow/checkpoint/snapshot.py": _read("hyperflow/checkpoint/snapshot.py"),
        "hyperflow/checkpoint/history.py": _read("hyperflow/checkpoint/history.py"),
        "hyperflow/api/routes_logs.py": _read("hyperflow/api/routes_logs.py"),
        "hyperflow/api/routes_checkpoints.py": _read("hyperflow/api/routes_checkpoints.py"),
    }

    forbidden = ("hyperflow.framework", "hyperflow.platform", "hyperflow.agent_runtime", "hyperflow.extensions")

    for path, content in baseline_modules.items():
        for needle in forbidden:
            assert needle not in content, f"{path} must not import {needle}"


def test_parser_control_mps_and_output_modules_do_not_import_future_layers() -> None:
    baseline_modules = {
        "hyperflow/language/command_builder.py": _read("hyperflow/language/command_builder.py"),
        "hyperflow/language/emoji_parser.py": _read("hyperflow/language/emoji_parser.py"),
        "hyperflow/control/mps_controller.py": _read("hyperflow/control/mps_controller.py"),
        "hyperflow/control/observer.py": _read("hyperflow/control/observer.py"),
        "hyperflow/output/run_payload.py": _read("hyperflow/output/run_payload.py"),
        "hyperflow/engine/edde_orchestrator.py": _read("hyperflow/engine/edde_orchestrator.py"),
    }

    forbidden = ("hyperflow.framework", "hyperflow.platform", "hyperflow.agent_runtime", "hyperflow.extensions")

    for path, content in baseline_modules.items():
        for needle in forbidden:
            assert needle not in content, f"{path} must not import {needle}"


def test_make_baseline_qualification_uses_dedicated_gate() -> None:
    makefile = _read("Makefile")
    script = _read("scripts/baseline_qualification.sh")
    assert "baseline-qualify:" in makefile
    assert "bash scripts/baseline_qualification.sh" in makefile
    for required_test in (
        "test_runtime_authority_boundaries.py",
        "test_command_builder.py",
        "test_config_layer.py",
        "test_contract_golden.py",
        "test_run_payload_golden.py",
        "test_edde_contract_schema.py",
        "test_runtime_kernel.py",
        "test_run_payload_serializer.py",
        "test_recent_traces.py",
        "test_emoji_action_router.py",
        "test_parser_authority.py",
        "test_emoji_registry.py",
        "test_runtime_persists_trace.py",
        "test_checkpoint_history.py",
        "test_runtime_storage_policy.py",
        "test_observability_routes.py",
        "test_checkpoint_identity.py",
    ):
        assert required_test in script
    assert "python -m hyperflow.release_verify --pretty" in script


def test_engine_dispatch_does_not_import_framework_runtime() -> None:
    """engine/dispatch.py must never import hyperflow.framework.runtime or call
    create_operational_framework().  Dispatch is framework-free by design; framework
    and platform layers register handlers INTO engine.registry at init time, and
    dispatch is a pure consumer.  This test enforces that dependency direction.
    """
    source = _read("hyperflow/engine/dispatch.py")
    assert "framework.runtime" not in source
    assert "create_operational_framework" not in source
    assert "_get_runtime_framework" not in source
    assert "_get_operational_framework" not in source


def test_engine_registry_does_not_import_framework_runtime() -> None:
    """engine/registry.py must not import hyperflow.framework.runtime."""
    source = _read("hyperflow/engine/registry.py")
    assert "framework.runtime" not in source
    assert "create_operational_framework" not in source


def test_canonical_api_does_not_mount_deferred_routers() -> None:
    """create_app() in edde_api.py must not mount agents or workflows routers.
    Those are DEFERRED surfaces pending an explicit promotion decision.
    """
    source = _read("hyperflow/api/edde_api.py")
    assert "routes_agents" not in source
    assert "routes_workflows" not in source
    assert "agents_router" not in source
    assert "workflows_router" not in source


def test_import_guard_scan_script_passes() -> None:
    import subprocess
    import sys

    root = Path(__file__).resolve().parents[2]
    completed = subprocess.run(
        [sys.executable, 'scripts/import_guard_scan.py'],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout
