from __future__ import annotations

from hyperflow.config import get_edde_core_config, get_emoji_atomic_registry

DEFAULT_TOKEN_MAP = {
    "🌈": {"class": "orientation", "meaning": "perceive", "weight": 0.9},
    "💎": {"class": "core", "meaning": "extract_core", "weight": 0.95},
    "🔥": {"class": "direction", "meaning": "set_direction", "weight": 0.85},
    "🧠": {"class": "cognition", "meaning": "synthesize", "weight": 0.9},
    "⚡": {"class": "decision", "meaning": "choose", "weight": 0.8},
    "🔀": {"class": "options", "meaning": "generate_options", "weight": 0.85},
    "🧱": {"class": "build", "meaning": "build_module", "weight": 0.85},
    "🧹": {"class": "cleanup", "meaning": "reduce_noise", "weight": 0.8},
    "🛡️": {"class": "safety", "meaning": "safe_mode", "weight": 0.9},
    "🔍": {"class": "inspection", "meaning": "inspect", "weight": 0.75},
    "📊": {"class": "structure", "meaning": "structured_analysis", "weight": 0.7},
    "🚀": {"class": "intensity", "meaning": "boosted", "weight": 0.95},
    "🧭": {"class": "direction", "meaning": "next_direction", "weight": 0.7},
    "🧑‍💻": {"class": "cognition", "meaning": "implementation", "weight": 0.8},
}

STATUS_WEIGHTS = {
    "core": 0.9,
    "boost": 0.75,
    "experimental": 0.6,
}


def _class_from_meaning(meaning: str) -> str:
    if not meaning:
        return "custom"
    head = meaning.split("_", 1)[0].strip().lower()
    return head or "custom"


def _build_token_map() -> dict[str, dict]:
    token_map = {token: info.copy() for token, info in DEFAULT_TOKEN_MAP.items()}
    atomic_registry = get_emoji_atomic_registry()
    signal_grammar = get_edde_core_config().get("signal_grammar", {})

    for token, entry in atomic_registry.items():
        current = token_map.get(token, {})
        meaning = str(entry.get("name", current.get("meaning", signal_grammar.get(token, token))))
        token_map[token] = {
            "class": current.get("class", _class_from_meaning(meaning)),
            "meaning": meaning,
            "weight": current.get("weight", STATUS_WEIGHTS.get(str(entry.get("status", "boost")), 0.75)),
            "status": str(entry.get("status", current.get("status", "boost"))),
            "category": str(entry.get("category", current.get("category", ""))),
            "expected_output": list(entry.get("expected_output", [])),
            "default_edde_phase": list(entry.get("default_edde_phase", [])),
            "default_mps": entry.get("default_mps"),
        }

    for token, meaning in signal_grammar.items():
        if token in atomic_registry:
            continue
        current = token_map.get(token, {})
        token_map[token] = {
            **current,
            "class": current.get("class", _class_from_meaning(str(meaning))),
            "meaning": str(meaning),
            "weight": current.get("weight", 0.8),
        }

    return token_map


TOKEN_MAP = _build_token_map()


def is_known_token(token: str) -> bool:
    return token in TOKEN_MAP


def get_token_info(token: str) -> dict:
    return TOKEN_MAP.get(
        token,
        {"class": "unknown", "meaning": "unknown", "weight": 0.1},
    )


def known_tokens() -> tuple[str, ...]:
    return tuple(TOKEN_MAP.keys())
