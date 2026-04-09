from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = REPO_ROOT / "configs"
PACKAGE_CONFIG_DIR = Path(__file__).resolve().parent / "configs"


def get_config_search_dirs() -> tuple[Path, ...]:
    search_dirs: list[Path] = []

    env_dir = os.getenv("HYPERFLOW_CONFIG_DIR", "").strip()
    if env_dir:
        search_dirs.append(Path(env_dir))

    search_dirs.append(CONFIG_DIR)
    search_dirs.append(PACKAGE_CONFIG_DIR)

    unique: list[Path] = []
    seen: set[str] = set()
    for path in search_dirs:
        key = str(path.resolve()) if path.exists() else str(path)
        if key in seen:
            continue
        unique.append(path)
        seen.add(key)

    return tuple(unique)

RUNTIME_MODE_ALIASES = {
    "architect": "build",
    "architecture": "build",
    "audit": "safe",
    "research": "analysis",
    "creative": "fusion",
    "synthesis": "fusion",
    "hyperflow": "final",
}

PIPELINE_STAGE_MAP = {
    "extract": ["scan", "extract"],
    "discover": ["cluster"],
    "do": ["interpret", "orchestrate", "remix"],
    "evaluate": ["output"],
}

OBJECTIVE_INTENT_ALIASES = {
    "knowledge organization": "planning",
    "knowledge mapping": "mapping",
    "idea synthesis": "synthesis",
    "framework construction": "build",
    "build framework": "build",
    "prompt creation": "documentation",
    "write prompt": "documentation",
    "hyperflow architecture evolution": "build",
    "hyperflow architecture": "build",
    "mapping connections across layers": "mapping",
    "map connections across layers": "mapping",
    # Backward-compatible legacy aliases.
    "organizacja wiedzy": "planning",
    "synteza idei": "synthesis",
    "budowa frameworków": "build",
    "tworzenie promptów": "documentation",
    "rozwój architektury hyperflow": "build",
    "mapowanie połączeń między warstwami": "mapping",
}

OUTPUT_TYPE_ALIASES = {
    "summary": "answer",
    "framework": "blueprint",
    "prompt": "spec",
    "json": "json",
    "markdown": "answer",
    "ascii-map": "map",
}

OUTPUT_HINT_RUNTIME_MAP = {
    "summary": {"runtime": "answer", "subtype": "summary"},
    "insight": {"runtime": "answer", "subtype": "insight"},
    "structured_explanation": {"runtime": "spec", "subtype": "structured_explanation"},
    "framework": {"runtime": "blueprint", "subtype": "framework"},
    "json": {"runtime": "json", "subtype": "json"},
    "markdown": {"runtime": "answer", "subtype": "markdown"},
    "plan": {"runtime": "plan", "subtype": "plan"},
    "ideas": {"runtime": "answer", "subtype": "ideas"},
    "variants": {"runtime": "answer", "subtype": "variants"},
    "audit": {"runtime": "report", "subtype": "audit"},
    "risks": {"runtime": "report", "subtype": "risks"},
    "fixes": {"runtime": "report", "subtype": "fixes"},
    "system_flow": {"runtime": "map", "subtype": "system_flow"},
    "code_structure": {"runtime": "blueprint", "subtype": "code_structure"},
    "visual_analysis": {"runtime": "report", "subtype": "visual_analysis"},
}


def _read_json_config(filename: str) -> dict[str, Any]:
    for base_dir in get_config_search_dirs():
        path = base_dir / filename
        if not path.exists():
            continue

        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    return {}


@lru_cache(maxsize=None)
def load_json_config(filename: str) -> dict[str, Any]:
    return _read_json_config(filename)


def get_edde_core_config() -> dict[str, Any]:
    return load_json_config("edde-core.json")


def get_mps_regulator_config() -> dict[str, Any]:
    return load_json_config("mps-regulator.json")


def get_system_shell_config() -> dict[str, Any]:
    return load_json_config("system-shell.json")


def get_emoji_action_router_config() -> dict[str, Any]:
    return load_json_config("emoji-action-router.json")


def get_canonical_emoji_library_config() -> dict[str, Any]:
    return load_json_config("canonical-emoji-library.json")


@lru_cache(maxsize=1)
def get_edde_mode_aliases() -> dict[str, str]:
    config = get_edde_core_config()
    aliases: dict[str, str] = {}
    for mode in config.get("modes", []):
        normalized = str(mode).strip().lower()
        if normalized:
            aliases[normalized] = RUNTIME_MODE_ALIASES.get(normalized, normalized)

    return aliases


@lru_cache(maxsize=1)
def get_pipeline_stage_aliases() -> dict[str, list[str]]:
    config = get_edde_core_config()
    configured = [str(item).strip() for item in config.get("flows", {}).get("pipeline", []) if str(item).strip()]
    configured_set = set(configured)

    aliases: dict[str, list[str]] = {}
    for runtime_phase, default_aliases in PIPELINE_STAGE_MAP.items():
        phase_aliases = [alias for alias in default_aliases if alias in configured_set]
        aliases[runtime_phase] = phase_aliases or default_aliases[:]

    return aliases


@lru_cache(maxsize=1)
def get_objective_intent_aliases() -> dict[str, str]:
    config = get_edde_core_config()
    aliases: dict[str, str] = dict(OBJECTIVE_INTENT_ALIASES)
    for objective in config.get("objectives", []):
        normalized = str(objective).strip().lower()
        if normalized and normalized not in aliases:
            aliases[normalized] = "analysis"

    return aliases


@lru_cache(maxsize=1)
def get_configured_output_aliases() -> dict[str, str]:
    config = get_edde_core_config()
    aliases: dict[str, str] = {}
    for output in config.get("flows", {}).get("outputs", []):
        normalized = str(output).strip().lower()
        if normalized:
            aliases[normalized] = OUTPUT_TYPE_ALIASES.get(normalized, "answer")

    return aliases


@lru_cache(maxsize=1)
def get_output_hint_runtime_map() -> dict[str, dict[str, str]]:
    return {key: value.copy() for key, value in OUTPUT_HINT_RUNTIME_MAP.items()}


def resolve_output_hint(hint: str) -> tuple[str, str | None]:
    entry = get_output_hint_runtime_map().get(str(hint).strip().lower())
    if not entry:
        return "answer", None
    return str(entry.get("runtime", "answer")), str(entry.get("subtype")) if entry.get("subtype") else None


@lru_cache(maxsize=1)
def get_emoji_atomic_registry() -> dict[str, dict[str, Any]]:
    return dict(get_canonical_emoji_library_config().get("atomic_registry", {}))


@lru_cache(maxsize=1)
def get_emoji_combo_registry() -> dict[str, dict[str, Any]]:
    return dict(get_canonical_emoji_library_config().get("combo_registry", {}))


@lru_cache(maxsize=1)
def get_emoji_short_presets() -> list[dict[str, Any]]:
    return [dict(item) for item in get_canonical_emoji_library_config().get("short_presets", [])]


@lru_cache(maxsize=1)
def get_emoji_long_presets() -> list[dict[str, Any]]:
    return [dict(item) for item in get_canonical_emoji_library_config().get("long_presets", [])]


@lru_cache(maxsize=1)
def get_emoji_parser_integration() -> dict[str, Any]:
    return dict(get_canonical_emoji_library_config().get("parser_integration", {}))


@lru_cache(maxsize=1)
def get_emoji_lookup_order() -> list[str]:
    parser_cfg = get_emoji_parser_integration()
    order = [str(item).strip() for item in parser_cfg.get("lookup_order", []) if str(item).strip()]
    return order or ["combo_registry", "short_presets", "long_presets", "atomic_registry"]


@lru_cache(maxsize=1)
def get_emoji_status_priority() -> list[str]:
    parser_cfg = get_emoji_parser_integration()
    priority = [str(item).strip() for item in parser_cfg.get("resolution_rules", {}).get("status_priority", []) if str(item).strip()]
    return priority or ["core", "boost", "experimental"]


@lru_cache(maxsize=1)
def get_emoji_parser_sequences() -> list[dict[str, Any]]:
    library = get_canonical_emoji_library_config()
    sequences: list[dict[str, Any]] = []

    for emoji, entry in library.get("combo_registry", {}).items():
        sequences.append({
            "kind": "combo_registry",
            "emoji": emoji,
            "name": str(entry.get("name", emoji)),
            "metadata": dict(entry),
        })

    for preset in library.get("short_presets", []):
        sequences.append({
            "kind": "short_presets",
            "emoji": str(preset.get("emoji", "")),
            "name": str(preset.get("name", "short_preset")),
            "metadata": dict(preset),
        })

    for preset in library.get("long_presets", []):
        sequences.append({
            "kind": "long_presets",
            "emoji": str(preset.get("emoji", "")),
            "name": str(preset.get("name", "long_preset")),
            "metadata": dict(preset),
        })


    for emoji, entry in library.get("atomic_registry", {}).items():
        sequences.append({
            "kind": "atomic_registry",
            "emoji": emoji,
            "name": str(entry.get("name", emoji)),
            "metadata": dict(entry),
        })

    kind_priority = {name: idx for idx, name in enumerate(get_emoji_lookup_order())}
    return sorted(
        [seq for seq in sequences if seq["emoji"]],
        key=lambda item: (
            -len(item["emoji"]),
            kind_priority.get(item["kind"], 99),
            get_emoji_status_priority().index(str(item["metadata"].get("status", "experimental"))) if str(item["metadata"].get("status", "experimental")) in get_emoji_status_priority() else 99,
        ),
    )


@lru_cache(maxsize=1)
def get_config_versions() -> dict[str, str]:
    edde = get_edde_core_config()
    mps = get_mps_regulator_config()
    shell = get_system_shell_config()
    emoji = get_canonical_emoji_library_config()
    action_router = get_emoji_action_router_config()
    return {
        "edde_schema": str(edde.get("schema", "")),
        "mps_schema": str(mps.get("schema", "")),
        "shell_schema": str(shell.get("schema", "")),
        "emoji_schema": str(emoji.get("schema", "")),
        "edde_version": str(edde.get("system", {}).get("version", "")),
        "mps_version": str(mps.get("system", {}).get("version", "")),
        "shell_version": str(shell.get("system", {}).get("version", "")),
        "emoji_version": str(emoji.get("library", {}).get("version", "")),
        "action_router_schema": str(action_router.get("schema", "")),
        "action_router_version": str(action_router.get("system", {}).get("version", "")),
    }


def _decompose_sequence_with_atoms(sequence: str, atomic_keys: tuple[str, ...]) -> tuple[list[str], list[str]]:
    resolved: list[str] = []
    unresolved: list[str] = []
    i = 0
    while i < len(sequence):
        matched = None
        for atom in atomic_keys:
            if sequence.startswith(atom, i):
                matched = atom
                break
        if matched is not None:
            resolved.append(matched)
            i += len(matched)
        else:
            unresolved.append(sequence[i])
            i += 1
    return resolved, unresolved


@lru_cache(maxsize=1)
def get_emoji_library_audit() -> dict[str, Any]:
    library = get_canonical_emoji_library_config()
    atomic_keys = tuple(sorted(get_emoji_atomic_registry().keys(), key=len, reverse=True))

    def classify(sequence_groups: list[tuple[str, str]], opaque_state: str) -> dict[str, Any]:
        unresolved_sequences: list[dict[str, Any]] = []
        closed_count = 0
        opaque_count = 0
        for source, emoji in sequence_groups:
            resolved, unresolved = _decompose_sequence_with_atoms(emoji, atomic_keys)
            if unresolved:
                opaque_count += 1
                unresolved_sequences.append({
                    "source": source,
                    "emoji": emoji,
                    "resolved_atoms": resolved,
                    "unresolved_fragments": unresolved,
                    "state": opaque_state,
                })
            else:
                closed_count += 1
        return {
            "closed_count": closed_count,
            "opaque_count": opaque_count,
            "unresolved_sequences": unresolved_sequences,
        }

    combo_sequences: list[tuple[str, str]] = [("combo_registry", str(emoji)) for emoji in library.get("combo_registry", {})]

    preset_sequences: list[tuple[str, str]] = []
    for preset in library.get("short_presets", []):
        if preset.get("emoji"):
            preset_sequences.append(("short_presets", str(preset.get("emoji"))))
    for preset in library.get("long_presets", []):
        if preset.get("emoji"):
            preset_sequences.append(("long_presets", str(preset.get("emoji"))))

    combo_audit = classify(combo_sequences, "opaque_combo")
    preset_audit = classify(preset_sequences, "opaque_preset")

    return {
        "atomic_count": len(get_emoji_atomic_registry()),
        "combo_count": len(library.get("combo_registry", {})),
        "short_preset_count": len(library.get("short_presets", [])),
        "long_preset_count": len(library.get("long_presets", [])),
        "closed_sequence_count": combo_audit["closed_count"] + preset_audit["closed_count"],
        "opaque_sequence_count": combo_audit["opaque_count"] + preset_audit["opaque_count"],
        "combo_closed_count": combo_audit["closed_count"],
        "combo_opaque_count": combo_audit["opaque_count"],
        "combo_unresolved_sequences": combo_audit["unresolved_sequences"],
        "preset_closed_count": preset_audit["closed_count"],
        "preset_opaque_count": preset_audit["opaque_count"],
        "preset_unresolved_sequences": preset_audit["unresolved_sequences"],
        "unresolved_sequences": combo_audit["unresolved_sequences"] + preset_audit["unresolved_sequences"],
    }


@lru_cache(maxsize=1)
def get_emoji_action_routes() -> dict[str, dict[str, Any]]:
    return {str(key): dict(value) for key, value in get_emoji_action_router_config().get("routes", {}).items()}


@lru_cache(maxsize=1)
def get_emoji_action_route_keys() -> tuple[str, ...]:
    return tuple(sorted(get_emoji_action_routes().keys(), key=len, reverse=True))
