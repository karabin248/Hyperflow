from __future__ import annotations

from pathlib import Path


def _read(path: str) -> str:
    root = Path(__file__).resolve().parents[2]
    return (root / path).read_text(encoding="utf-8")


def test_readme_freezes_baseline_identity() -> None:
    readme = _read("README.md")
    assert "MVP Core" in readme
    assert "Runtime Shell" in readme
    assert "Reasoning Authority" in readme
    assert "Control Authority" in readme
    assert "Minimal Orchestration Layer" in readme
    assert "🌈💎🔥🧠🔀⚡" in readme


def test_canonical_runtime_surface_excludes_framework_from_active_spine() -> None:
    runtime_surface = _read("core/CANONICAL_RUNTIME_SURFACE.md")
    assert "Optional framework core" not in runtime_surface
    assert "hyperflow/framework/*" not in runtime_surface
    assert "Canonical API entry" in runtime_surface


def test_repository_governance_keeps_one_active_runtime_spine() -> None:
    governance = _read("REPOSITORY_GOVERNANCE.md")
    active_runtime_section = governance.split("## 1) Active Runtime Spine", 1)[1].split("## 2)", 1)[0]
    assert "hyperflow/framework/*" not in active_runtime_section
    assert "one canonical runtime spine" in governance.lower()


def test_acceptance_doc_maps_definition_of_done() -> None:
    acceptance = _read("core/BASELINE_ACCEPTANCE.md")
    assert "Definition of Done" in acceptance
    assert "Docs match runtime truth" in acceptance
    assert "Future phases become separate by default" in acceptance


def test_canonical_pipeline_docs_keep_reversed_tail_legacy_only() -> None:
    pipeline = _read("docs/architecture/canonical_pipeline.md")
    runtime_contract = _read("docs/contracts/runtime_contract.md")

    assert "🌈💎🔥🧠🔀⚡" in pipeline
    assert "🌈💎🔥🧠⚡🔀" in pipeline
    assert "not canonical" in pipeline
    assert "deprecated legacy alias" in pipeline.lower()
    assert "legacy cycle `🌈💎🔥🧠⚡🔀` may remain supported only" in runtime_contract


def test_public_api_docs_match_runtime_guard_surface() -> None:
    docs = {
        "README": _read("README.md"),
        "authority_map": _read("docs/architecture/authority_map.md"),
        "canonical_runtime": _read("docs/architecture/canonical_runtime.md"),
        "api_contract": _read("docs/contracts/api_contract.md"),
    }

    public_endpoints = [
        "GET /v1/health",
        "POST /v1/run",
        "GET /v1/checkpoints",
        "GET /v1/checkpoints/latest",
        "GET /v1/checkpoints/{checkpoint_id}",
        "GET /v1/logs/recent",
    ]
    deferred_markers = [
        "DEFERRED metadata surface",
    ]

    for name, content in docs.items():
        for endpoint in public_endpoints:
            assert endpoint in content, f"{name} is missing {endpoint}"
        for marker in deferred_markers:
            assert marker in content, f"{name} is missing deferred marker {marker}"


def test_canonical_runtime_docs_keep_archive_reference_only() -> None:
    runtime_doc = _read("docs/architecture/canonical_runtime.md")
    authority_map = _read("docs/architecture/authority_map.md")
    runtime_contract = _read("docs/contracts/runtime_contract.md")

    assert "reference/output only" in runtime_doc
    assert "not baseline source truth" in runtime_doc
    assert "generated output, not source truth" in authority_map
    assert "runtime outputs" in runtime_contract
    assert "must not be treated as canonical source material" in runtime_contract


def test_baseline_qualification_gate_is_canonical_reference() -> None:
    acceptance = _read("core/BASELINE_ACCEPTANCE.md")
    gate = _read("core/BASELINE_QUALIFICATION_GATE.md")
    runtime_surface = _read("core/CANONICAL_RUNTIME_SURFACE.md")

    assert "No new canonical behavior may emerge outside the baseline qualification gate." in gate
    assert "Reasoning Authority" in acceptance
    assert "Control Authority" in acceptance
    assert "BASELINE_QUALIFICATION_GATE.md" in runtime_surface
    assert "make baseline-qualify" in acceptance


def test_trace_and_checkpoint_authority_are_explicit_in_docs() -> None:
    acceptance = _read("core/BASELINE_ACCEPTANCE.md")
    gate = _read("core/BASELINE_QUALIFICATION_GATE.md")
    authority_map = _read("docs/architecture/authority_map.md")

    assert "Core trace / checkpoint authority is test-backed" in acceptance
    assert "core trace / core checkpoint truth" in gate
    assert "canonical trace/checkpoint truth path singular" in gate
    assert "core trace / core checkpoint truth stays baseline-owned" in authority_map


def test_parser_mps_and_output_contract_authority_are_explicit_in_docs() -> None:
    acceptance = _read("core/BASELINE_ACCEPTANCE.md")
    gate = _read("core/BASELINE_QUALIFICATION_GATE.md")
    authority_map = _read("docs/architecture/authority_map.md")
    runtime_contract = _read("docs/contracts/runtime_contract.md")
    canonical_runtime = _read("docs/architecture/canonical_runtime.md")

    assert "Parser / control, baseline action routing, baseline action execution helpers, MPS, and output contract authority are test-backed" in acceptance
    assert "parser/control semantics stay baseline-owned" in gate
    assert "MPS mode-control semantics stay baseline-owned" in gate
    assert "output contract semantics stay baseline-owned" in gate
    assert "Parser/control authority stays baseline-owned." in authority_map
    assert "Baseline action routing stays baseline-owned." in authority_map
    assert "MPS state-policy authority stays baseline-owned." in authority_map
    assert "Baseline action execution helpers stay baseline-owned." in authority_map
    assert "Output contract authority stays baseline-owned." in authority_map
    assert "Parser / control, baseline action routing, baseline action execution helpers, MPS, and output contract behavior must qualify through `make baseline-qualify`" in runtime_contract
    assert "parser/control -> `hyperflow.language.command_builder.build_command()`" in canonical_runtime
    assert "MPS / control -> `hyperflow.control/*`" in canonical_runtime
    assert "output contract -> `hyperflow.output.run_payload.serialize_run_payload()`" in canonical_runtime
    assert "baseline action routing -> `hyperflow.language.action_router.route_emoji_actions()`" in canonical_runtime
    assert "baseline action execution -> `hyperflow.engine.action_registry.*`" in canonical_runtime
