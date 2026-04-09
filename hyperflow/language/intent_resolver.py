from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from hyperflow.config import get_configured_output_aliases, get_objective_intent_aliases
from hyperflow.language.token_registry import get_token_info

TEXT_INTENT_HINTS = {
    "planning": ("plan", "checklist", "roadmap", "lista", "checklista"),
    "documentation": (
        "spec",
        "specification",
        "specyfik",
        "prompt",
        "definition",
        "definicj",
        "explain",
        "wytłumacz",
        "wyjaśnij",
        "essay",
        "esej",
        "guide",
        "poradnik",
        "instruction",
        "instructions",
        "instrukcj",
        "history",
        "histori",
    ),
    "mapping": ("map", "mapping", "mapa", "connections", "connection", "relations", "relation", "połączeń", "relacji"),
    "build": (
        "zbuduj",
        "build",
        "repo",
        "framework",
        "architecture",
        "architektur",
        "function",
        "funkcj",
        "algorithm",
        "algorytm",
        "program",
        "code",
        "kod",
    ),
    "cleanup": ("cleanup", "clean up", "clean", "remove", "usuń", "wyczyść"),
}

TOKEN_INTENT_HINTS = {
    "perceive": "analysis",
    "scan_context": "analysis",
    "extract_core": "build",
    "core_extract": "build",
    "set_direction": "planning",
    "ignite_direction": "planning",
    "synthesize": "synthesis",
    "deep_reason": "analysis",
    "generate_options": "synthesis",
    "see_options": "synthesis",
    "reroute_remix": "synthesis",
    "reroute_or_remix": "synthesis",
    "choose": "planning",
    "commit_choice": "planning",
}

OUTPUT_INTENT_HINTS = {
    "blueprint": "build",
    "spec": "documentation",
    "map": "mapping",
}


def _intent_from_config_objectives(lower: str) -> str | None:
    for objective_text, intent in get_objective_intent_aliases().items():
        if objective_text and objective_text in lower:
            return intent
    return None


def _intent_from_config_outputs(lower: str) -> str | None:
    for output_text, output_type in get_configured_output_aliases().items():
        if output_text and output_text in lower:
            return OUTPUT_INTENT_HINTS.get(output_type)
    return None


def _intent_from_token_meanings(tokens: Iterable[str]) -> str | None:
    for token in tokens:
        meaning = str(get_token_info(token).get("meaning", "")).strip().lower()
        intent = TOKEN_INTENT_HINTS.get(meaning)
        if intent:
            return intent
    return None


def _intent_from_parser_state(parser_state: dict[str, Any] | None) -> str | None:
    if not parser_state or str(parser_state.get("primary_status", "")) == "experimental":
        return None

    outputs = set(parser_state.get("resolved_output_types", []))
    phases = set(parser_state.get("resolved_edde_phase", []))

    if outputs & {"audit", "risks", "fixes", "visual_analysis"} or phases & {"validate", "mitigate"}:
        return "analysis"
    if "system_flow" in outputs:
        return "mapping"
    if "plan" in outputs:
        return "planning"
    if outputs & {"framework", "json", "code_structure"} or phases & {"build", "structure", "package", "deliver"}:
        return "build"
    if outputs & {"ideas", "variants"} or "remix" in phases:
        return "synthesis"
    if phases & {"scan", "extract", "reason"}:
        return "analysis"
    return None


def resolve_intent(tokens: Iterable[str], text: str, parser_state: dict[str, Any] | None = None) -> str:
    lower = text.lower()

    cleanup_terms = TEXT_INTENT_HINTS["cleanup"]
    if any(term in lower for term in cleanup_terms):
        return "cleanup"

    # Explicit text wins before emoji-driven routing.
    for intent, terms in TEXT_INTENT_HINTS.items():
        if intent == "cleanup":
            continue
        if any(term in lower for term in terms):
            return intent

    config_output_intent = _intent_from_config_outputs(lower)
    if config_output_intent:
        return config_output_intent

    config_objective_intent = _intent_from_config_objectives(lower)
    if config_objective_intent:
        return config_objective_intent

    parser_intent = _intent_from_parser_state(parser_state)
    if parser_intent:
        return parser_intent

    token_set = set(tokens)
    if "🧱" in token_set:
        return "build"
    if "🧹" in token_set:
        return "cleanup"
    if "🔀" in token_set and "💎" in token_set:
        return "synthesis"
    if "🧠" in token_set:
        return "analysis"

    token_meaning_intent = _intent_from_token_meanings(token_set)
    if token_meaning_intent:
        return token_meaning_intent

    return "analysis"


def resolve_operations(tokens: Iterable[str], text: str, parser_state: dict[str, Any] | None = None) -> list[str]:
    token_set = set(tokens)
    # NOTE: operations list is intentionally built with possible duplicates here.
    # `build_structure` may be added both via token path (🧱) and text-hint path below.
    # This is safe: dict.fromkeys() at the end deduplicates while preserving insertion order.
    operations: list[str] = []
    # Warn #3 guard: is_canonical_full_combo relies on combo_registry having the entry.
    # Verified in canonical-emoji-library.json combo_registry key '🌈💎🔥🧠🔀⚡'
    # with name 'hyperflow_canonical_full_combo' and status 'core'. If combo_registry
    # is ever changed, the canonical flag field also guards this path.
    is_canonical_full_combo = (
        str((parser_state or {}).get("primary_name", "")) == "hyperflow_canonical_full_combo"
        or bool((parser_state or {}).get("canonical", False))
    )

    if "🌈" in token_set:
        operations.append("perceive")
    if "💎" in token_set:
        operations.append("extract_core")
    if "🔥" in token_set:
        operations.append("set_direction")
    if "🧠" in token_set:
        operations.append("synthesize")
    if "🔀" in token_set:
        operations.append("generate_options")
    if "⚡" in token_set:
        operations.append("choose")
    if "🧹" in token_set:
        operations.append("cleanup")
    if "🧱" in token_set:
        operations.append("build_structure")  # may also be added via text hints below — dedup at return
    if "🔍" in token_set:
        operations.append("inspect")
    if "📊" in token_set:
        operations.append("structure")
    if "👁️" in token_set or "🛡️" in token_set or "⚠️" in token_set:
        operations.append("validate")
    if "⚙️" in token_set:
        operations.append("orchestrate")
    if "📦" in token_set:
        operations.append("package")

    if parser_state:
        phases = set(parser_state.get("resolved_edde_phase", []))
        phase_operation_map = {
            "validate": "validate",
            "mitigate": "mitigate",
            "orchestrate": "orchestrate",
            "package": "package",
            "deliver": "deliver",
            "structure": "structure",
            "build": "build_structure",
        }
        blocked_for_canonical_full_combo = {"deliver", "structure", "build_structure"}
        for phase, operation in phase_operation_map.items():
            if phase in phases and not (is_canonical_full_combo and operation in blocked_for_canonical_full_combo):
                operations.append(operation)

    lower = text.lower()
    if not is_canonical_full_combo:
        if any(term in lower for term in TEXT_INTENT_HINTS["planning"]) and "structure" not in operations:
            operations.append("structure")
        # build_structure may already be present from token path (🧱); dict.fromkeys at return deduplicates.
        if any(term in lower for term in ("framework", "architecture", "architektur", "function", "funkcj", "algorithm", "algorytm", "program", "code")):
            operations.append("build_structure")
        if any(term in lower for term in (
            "prompt",
            "definition",
            "definicj",
            "explain",
            "wytłumacz",
            "wyjaśnij",
            "essay",
            "esej",
            "guide",
            "poradnik",
            "instruction",
            "instructions",
            "instrukcj",
            "history",
            "histori",
        )):
            operations.append("document")
        if any(term in lower for term in ("mapping", "mapa", "map", "connections", "connection", "relations", "relation", "połączeń", "relacji")):
            operations.append("map_relations")
    if not operations:
        operations.append("analyze")

    # dict.fromkeys preserves insertion order and removes all duplicates.
    return list(dict.fromkeys(operations))
