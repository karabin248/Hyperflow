from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from hyperflow.config import get_edde_mode_aliases
from hyperflow.language.token_registry import get_token_info


TEXT_MODE_HINTS = {
    "architect": "build",
    "audit": "safe",
    "research": "analysis",
    "creative": "fusion",
    "synthesis": "fusion",
    "hyperflow mode": "final",
    "tryb hyperflow": "final",
}

TOKEN_MEANING_MODE_HINTS = {
    "perceive": "analysis",
    "scan_context": "analysis",
    "extract_core": "build",
    "core_extract": "build",
    "set_direction": "final",
    "ignite_direction": "final",
    "synthesize": "analysis",
    "deep_reason": "analysis",
    "generate_options": "fusion",
    "see_options": "fusion",
    "reroute_or_remix": "fusion",
    "reroute_remix": "fusion",
    "choose": "final",
    "commit_choice": "final",
    "ignite_mode": "final",
    "ignite_build": "build",
}


def _mode_from_configured_aliases(text: str) -> str | None:
    lower = text.lower()
    for configured_mode, runtime_mode in get_edde_mode_aliases().items():
        if configured_mode == "hyperflow":
            continue
        if configured_mode and configured_mode in lower:
            return runtime_mode
    return None



def _mode_from_token_meanings(tokens: Iterable[str]) -> str | None:
    resolved_modes: list[str] = []
    for token in tokens:
        meaning = str(get_token_info(token).get("meaning", "")).strip().lower()
        mode = TOKEN_MEANING_MODE_HINTS.get(meaning)
        if mode:
            resolved_modes.append(mode)

    if "fusion" in resolved_modes:
        return "fusion"
    if "final" in resolved_modes and any(mode in resolved_modes for mode in {"analysis", "build"}):
        return "final"
    if resolved_modes:
        return resolved_modes[-1]
    return None



def _mode_from_parser_state(parser_state: dict[str, Any] | None) -> str | None:
    if not parser_state or str(parser_state.get("primary_status", "")) == "experimental":
        return None

    phases = set(parser_state.get("resolved_edde_phase", []))
    outputs = set(parser_state.get("resolved_output_types", []))
    resolved_mps = int(parser_state.get("resolved_mps_mode") or 0)

    if phases & {"validate", "mitigate"} or outputs & {"audit", "risks", "fixes", "visual_analysis"}:
        return "safe"
    if phases & {"orchestrate", "remix"}:
        return "fusion"
    if phases & {"build", "structure", "package"} or outputs & {"framework", "json", "code_structure"}:
        if resolved_mps >= 5 and phases & {"deliver", "reason"} and phases & {"scan", "extract", "build"}:
            return "final"
        return "build"
    if phases & {"reason", "extract"}:
        return "analysis"
    return None



def resolve_mode(tokens: Iterable[str], text: str, parser_state: dict[str, Any] | None = None) -> str:
    token_set = set(tokens)
    lower = text.lower()

    if "🛡️" in token_set:
        return "safe"

    configured_alias = _mode_from_configured_aliases(lower)
    if configured_alias:
        return configured_alias

    for phrase, runtime_mode in TEXT_MODE_HINTS.items():
        if phrase in lower:
            return runtime_mode

    if "final" in lower or "finalny" in lower:
        return "final"
    if "🔀" in token_set and "💎" in token_set:
        return "fusion"

    parser_mode = _mode_from_parser_state(parser_state)
    if parser_mode:
        return parser_mode

    token_mode = _mode_from_token_meanings(token_set)
    if token_mode:
        return token_mode

    if "🚀" in token_set:
        return "final"
    if "🧱" in token_set:
        return "build"
    if "🧠" in token_set:
        return "analysis"
    return "standard"



def resolve_intensity(tokens: Iterable[str]) -> str:
    token_set = set(tokens)

    if "🚀" in token_set:
        return "boosted"
    if "🔥" in token_set and "⚡" in token_set:
        return "high"
    if "🔥" in token_set:
        return "high"
    return "medium"



def resolve_constraints(tokens: Iterable[str], text: str) -> list[str]:
    constraints: list[str] = []
    token_set = set(tokens)
    lower = text.lower()

    if "🛡️" in token_set:
        constraints.append("safe_mode")
    if "🧹" in token_set:
        constraints.append("reduce_noise")
    if any(term in lower for term in ("krótko", "short", "brief", "concise")):
        constraints.append("concise_output")
    if any(term in lower for term in ("pełna", "full", "detailed", "deep")):
        constraints.append("deep_output")
    configured_alias = _mode_from_configured_aliases(lower)
    if configured_alias == "build":
        constraints.append("architect_mode")
    if configured_alias == "analysis":
        constraints.append("research_mode")

    return list(dict.fromkeys(constraints))
