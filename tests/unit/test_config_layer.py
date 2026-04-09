import json
from pathlib import Path

from hyperflow.config import (
    get_canonical_emoji_library_config,
    get_config_versions,
    get_emoji_parser_sequences,
    get_configured_output_aliases,
    get_edde_core_config,
    get_emoji_library_audit,
    get_edde_mode_aliases,
    get_mps_regulator_config,
    get_objective_intent_aliases,
    get_pipeline_stage_aliases,
    get_system_shell_config,
)
from hyperflow.control.mps_controller import resolve_mps_level
from hyperflow.engine.edde_orchestrator import run_edde
from hyperflow.engine.runtime_state import init_runtime_state
from hyperflow.language.command_builder import build_command
from hyperflow.language.mode_resolver import resolve_mode
from hyperflow.language.token_registry import get_token_info
from hyperflow.schemas.command_schema import CommandObject


ROOT = Path(__file__).resolve().parents[2]


def test_configs_load_from_repo_root():
    edde = get_edde_core_config()
    mps = get_mps_regulator_config()
    shell = get_system_shell_config()
    emoji = get_canonical_emoji_library_config()

    assert edde["schema"] == "hyperflow/edde-core/v1"
    assert mps["schema"] == "hyperflow/mps-regulator/v1"
    assert shell["schema"] == "hyperflow/system/v1"
    assert shell["executable"] is False
    assert emoji["schema"] == "hyperflow/canonical-emoji-library/v1"
    assert emoji["library"]["version"] == "1.4.0"




def test_core_config_human_text_is_english():
    edde = get_edde_core_config()
    shell = get_system_shell_config()

    assert edde["system"]["language"] == "en"
    assert edde["identity"]["description"] == (
        "Canonical decision-to-execution runtime contract for controlled perception, essence extraction, directional synthesis, option generation, and final execution in Hyperflow."
    )
    assert edde["identity"]["style"] == [
        "canonical",
        "controlled",
        "layered",
        "analytical",
        "execution-oriented",
    ]
    assert shell["system"]["purpose"] == (
        "Macro architecture visible in the diagram - vectors, engines, safety, export, runtime"
    )

def test_signal_grammar_overrides_token_meaning():
    assert get_token_info("🌈")["meaning"] == "perceive"
    assert get_token_info("🔥")["meaning"] == "set_direction"




def test_configs_fallback_to_packaged_copy_when_repo_configs_missing(monkeypatch, tmp_path):
    import hyperflow.config as config_module

    packaged_dir = tmp_path / "packaged-configs"
    packaged_dir.mkdir()
    for name in (
        "edde-core.json",
        "mps-regulator.json",
        "system-shell.json",
        "canonical-emoji-library.json",
        "emoji-action-router.json",
    ):
        source = (ROOT / "hyperflow" / "configs" / name).read_text(encoding="utf-8")
        (packaged_dir / name).write_text(source, encoding="utf-8")

    monkeypatch.setattr(config_module, "CONFIG_DIR", tmp_path / "missing-repo-configs")
    monkeypatch.setattr(config_module, "PACKAGE_CONFIG_DIR", packaged_dir)

    for fn_name in (
        "load_json_config",
        "get_edde_mode_aliases",
        "get_pipeline_stage_aliases",
        "get_objective_intent_aliases",
        "get_configured_output_aliases",
        "get_output_hint_runtime_map",
        "get_emoji_atomic_registry",
        "get_emoji_combo_registry",
        "get_emoji_short_presets",
        "get_emoji_long_presets",
        "get_emoji_parser_integration",
        "get_emoji_lookup_order",
        "get_emoji_status_priority",
        "get_emoji_parser_sequences",
        "get_config_versions",
        "get_emoji_library_audit",
        "get_emoji_action_routes",
        "get_emoji_action_route_keys",
    ):
        getattr(config_module, fn_name).cache_clear()

    try:
        assert config_module.get_edde_core_config()["schema"] == "hyperflow/edde-core/v1"
        assert config_module.get_canonical_emoji_library_config()["schema"] == "hyperflow/canonical-emoji-library/v1"
        assert config_module.get_emoji_action_router_config()["schema"] == "hyperflow/emoji-action-router/v1"
        assert config_module.get_config_versions()["action_router_schema"] == "hyperflow/emoji-action-router/v1"
    finally:
        for fn_name in (
            "load_json_config",
            "get_edde_mode_aliases",
            "get_pipeline_stage_aliases",
            "get_objective_intent_aliases",
            "get_configured_output_aliases",
            "get_output_hint_runtime_map",
            "get_emoji_atomic_registry",
            "get_emoji_combo_registry",
            "get_emoji_short_presets",
            "get_emoji_long_presets",
            "get_emoji_parser_integration",
            "get_emoji_lookup_order",
            "get_emoji_status_priority",
            "get_emoji_parser_sequences",
            "get_config_versions",
            "get_emoji_library_audit",
            "get_emoji_action_routes",
            "get_emoji_action_route_keys",
        ):
            getattr(config_module, fn_name).cache_clear()


def test_mps_resolution_uses_configured_level_shape():
    fusion = CommandObject(raw_input="💎 🔀 fusion task", tokens=["💎", "🔀"], mode="fusion", operations=["extract_core", "generate_options"], intent="synthesis", output_type="answer")
    planning = CommandObject(raw_input="💎 make a plan", tokens=["💎"], mode="standard", operations=["extract_core", "structure"], intent="planning", output_type="plan")

    assert resolve_mps_level(fusion) == 6
    assert resolve_mps_level(planning) == 5


def test_trace_config_versions_are_exposed():
    versions = get_config_versions()
    assert versions["edde_version"] == "1.0.0"
    assert versions["mps_version"] == "0.5.0"
    assert versions["shell_version"] == "0.9.0"
    assert versions["emoji_version"] == "1.4.0"


def test_mode_aliases_are_loaded_from_edde_config():
    aliases = get_edde_mode_aliases()
    assert aliases["architect"] == "build"
    assert aliases["research"] == "analysis"


def test_mode_resolver_honors_configured_mode_alias_text():
    assert resolve_mode([], "Use architect mode for this module breakdown") == "build"
    assert resolve_mode([], "Let's do research mode on this topic") == "analysis"
    assert resolve_mode([], "Need synthesis mode for these threads") == "fusion"
    assert resolve_mode([], "Enter hyperflow mode for this final pass") == "final"


def test_command_builder_uses_configured_mode_aliases():
    command = build_command("Architect mode: create a module blueprint")
    assert command.mode == "build"
    assert "architect_mode" in command.constraints


def test_pipeline_stage_aliases_are_loaded_from_edde_config():
    aliases = get_pipeline_stage_aliases()
    assert aliases["extract"] == ["scan", "extract"]
    assert aliases["discover"] == ["cluster"]
    assert aliases["do"] == ["interpret", "orchestrate", "remix"]
    assert aliases["evaluate"] == ["output"]


def test_edde_run_exposes_pipeline_alias_metadata():
    command = build_command("🧠 Analyze this repo structure")
    state = init_runtime_state(command)
    result = run_edde(command, state)

    assert result["pipeline_path"] == [
        "scan",
        "extract",
        "cluster",
        "interpret",
        "orchestrate",
        "remix",
        "output",
    ]
    assert result["pipeline_stage_map"]["do"] == ["interpret", "orchestrate", "remix"]
    assert state.partial_results[0]["pipeline_aliases"] == ["scan", "extract"]
    assert "edde_contract" not in result


def test_config_output_aliases_are_loaded_from_edde_config():
    outputs = get_configured_output_aliases()
    assert outputs["framework"] == "blueprint"
    assert outputs["prompt"] == "spec"
    assert outputs["ascii-map"] == "map"


def test_objective_aliases_are_loaded_from_edde_config():
    objectives = get_objective_intent_aliases()
    assert objectives["idea synthesis"] == "synthesis"
    assert objectives["mapping connections across layers"] == "mapping"
    assert objectives["synteza idei"] == "synthesis"
    assert objectives["mapowanie połączeń między warstwami"] == "mapping"


def test_intent_and_output_routing_use_edde_config_terms():
    framework_command = build_command("Create a framework for module orchestration")
    prompt_command = build_command("I need a prompt for repository analysis")
    map_command = build_command("Map connections across layers")

    assert framework_command.intent == "build"
    assert framework_command.output_type == "blueprint"
    assert "build_structure" in framework_command.operations

    assert prompt_command.intent == "documentation"
    assert prompt_command.output_type == "spec"
    assert "document" in prompt_command.operations

    assert map_command.intent == "mapping"
    assert map_command.output_type in {"map", "answer"}
    assert "map_relations" in map_command.operations


def test_canonical_full_combo_parser_metadata_drives_mode_and_output():
    command = build_command("🌈💎🔥🧠🔀⚡")
    assert command.parser_trace["matched_combo"] == "🌈💎🔥🧠🔀⚡"
    assert command.parser_trace["primary_name"] == "hyperflow_canonical_full_combo"
    assert command.mode == "fusion"
    assert command.output_type == "blueprint"


def test_canonical_signature_matches_canonical_combo_semantics():
    library = get_canonical_emoji_library_config()
    combo = library["combo_registry"]["🌈💎🔥🧠🔀⚡"]
    signature = library["canonical_signature"]

    assert signature["emoji"] == "🌈💎🔥🧠🔀⚡"
    assert combo["edde_phase"] == ["scan", "extract", "build", "reason", "remix", "deliver"]
    assert signature["edde_phase"] == combo["edde_phase"]

def test_canonical_signature_does_not_participate_in_parser_sequences():
    sequences = get_emoji_parser_sequences()

    assert all(seq["kind"] != "canonical_signature" for seq in sequences)
    assert sum(1 for seq in sequences if seq["emoji"] == "🌈💎🔥🧠🔀⚡") == 1
    assert next(seq for seq in sequences if seq["emoji"] == "🌈💎🔥🧠🔀⚡")["kind"] == "combo_registry"


def test_legacy_short_full_combo_remains_backward_compatible():
    command = build_command("🌈💎🔥🧠⚡")
    assert command.parser_trace["matched_combo"] == "🌈💎🔥🧠⚡"
    assert command.mode == "final"
    assert command.output_type == "blueprint"


def test_emoji_library_audit_reports_closed_combo_registry():
    audit = get_emoji_library_audit()

    assert audit["atomic_count"] == 70
    assert audit["combo_count"] == 40
    assert audit["combo_opaque_count"] == 0
    assert audit["combo_unresolved_sequences"] == []
    assert audit["preset_opaque_count"] >= 1
    assert all(item["state"] == "opaque_preset" for item in audit["preset_unresolved_sequences"])


def test_combo_extension_and_atomic_closure_parse_cleanly():
    command = build_command("📥🔍🧾 then stabilize with 🧘🫁🧊")

    assert "📥" in command.tokens
    assert "🔍" in command.tokens
    assert "🧾" in command.tokens
    assert command.parser_trace["matched_combo"] == "📥🔍🧾"
    assert "scan" in command.parser_trace["resolved_edde_phase"]
    assert "validate" in command.parser_trace["resolved_edde_phase"]


def test_output_subtype_mapping_is_formalized_from_parser_hints():
    command = build_command("👁️🔍🧠🧱⚙️")
    assert command.output_type == "report"
    assert command.output_subtype == "visual_analysis"
    assert "visual_analysis" in command.parser_trace["resolved_output_subtypes"]


def test_mps_profile_separates_state_from_risk_state():
    command = build_command("💎 make a plan")
    state = init_runtime_state(command)
    state.mps_level = resolve_mps_level(command)
    from hyperflow.control.mps_controller import apply_mps_profile

    state = apply_mps_profile(state)
    assert state.mps_state == "Dominant Core"
    assert state.risk_state == "high"
    assert state.risk_level == state.risk_state


def test_emoji_library_related_artifacts_exist_in_repo() -> None:
    library = get_canonical_emoji_library_config()
    related = library["integration"]["related_artifacts"]

    for relative_path in related:
        assert (ROOT / relative_path).exists(), relative_path




def test_system_shell_template_store_metadata_does_not_point_at_missing_paths() -> None:
    shell = get_system_shell_config()

    configured_paths = [
        shell["subsystems"]["prompt_architecture"]["templates_store"],
        shell["prompt_architecture"]["template_store"],
    ]

    for value in configured_paths:
        assert value == "inline_runtime"
        assert "/" not in value

def test_packaged_configs_match_repo_configs() -> None:
    repo_config_dir = ROOT / "configs"
    packaged_config_dir = ROOT / "hyperflow" / "configs"

    for repo_config in sorted(repo_config_dir.glob("*.json")):
        packaged_config = packaged_config_dir / repo_config.name
        assert packaged_config.exists(), repo_config.name
        assert json.loads(packaged_config.read_text(encoding="utf-8")) == json.loads(
            repo_config.read_text(encoding="utf-8")
        ), repo_config.name


def test_shipped_config_json_text_is_ascii_readable():
    for rel in (
        Path("configs/edde-core.json"),
        Path("configs/system-shell.json"),
        Path("configs/canonical-emoji-library.json"),
        Path("hyperflow/configs/edde-core.json"),
        Path("hyperflow/configs/system-shell.json"),
        Path("hyperflow/configs/canonical-emoji-library.json"),
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "Ś" not in text
        assert "ł" not in text
        assert "ą" not in text
        assert "ż" not in text
        assert "ź" not in text
        assert "ń" not in text
        assert "ó" not in text
        assert "ę" not in text
        assert "ć" not in text
        assert "→" not in text
        assert "—" not in text

