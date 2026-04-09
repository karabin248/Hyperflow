from __future__ import annotations

from typing import Any

from hyperflow.config import get_configured_output_aliases, resolve_output_hint


TEXT_OUTPUT_HINTS = {
    "plan": ("plan", "checklist", "roadmap", "lista", "checklista"),
    "spec": (
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
    "blueprint": ("blueprint", "framework", "function", "funkcj", "algorithm", "algorytm", "program", "code", "kod"),
    "map": ("mapa", "map", "mapping", "ascii-map", "ascii map"),
    "json": ("json",),
}


def _output_from_config(lower: str) -> str | None:
    for configured_output, runtime_output in get_configured_output_aliases().items():
        if configured_output and configured_output in lower:
            return runtime_output
    return None


def _output_from_parser_state(parser_state: dict[str, Any] | None) -> str | None:
    if not parser_state or str(parser_state.get("primary_status", "")) == "experimental":
        return None

    for hinted_output in parser_state.get("resolved_output_types", []):
        runtime, _subtype = resolve_output_hint(str(hinted_output))
        if runtime:
            return runtime
    return None


def resolve_output_type(text: str, parser_state: dict[str, Any] | None = None) -> str:
    lower = text.lower()

    for output_type, terms in TEXT_OUTPUT_HINTS.items():
        if any(term in lower for term in terms):
            return output_type

    configured_output = _output_from_config(lower)
    if configured_output:
        return configured_output

    parser_output = _output_from_parser_state(parser_state)
    if parser_output:
        return parser_output

    if "repo" in lower:
        return "blueprint"

    return "answer"


def resolve_output_subtype(text: str, output_type: str, parser_state: dict[str, Any] | None = None) -> str:
    lower = text.lower()
    if output_type in {"plan", "spec", "blueprint", "map", "json"}:
        if output_type == "blueprint" and any(term in lower for term in ("function", "funkcj", "algorithm", "algorytm", "program", "code", "kod")):
            return "code_structure"
        return output_type

    if parser_state and str(parser_state.get("primary_status", "")) != "experimental":
        for hinted_output in parser_state.get("resolved_output_types", []):
            runtime, subtype = resolve_output_hint(str(hinted_output))
            if runtime == output_type and subtype:
                return subtype

    for configured_output in get_configured_output_aliases().keys():
        if configured_output and configured_output in lower:
            _runtime, subtype = resolve_output_hint(configured_output)
            if subtype:
                return subtype

    return output_type if output_type != "answer" else "summary"
