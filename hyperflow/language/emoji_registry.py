from __future__ import annotations

from typing import Any

from hyperflow.config import (
    get_emoji_atomic_registry,
    get_emoji_combo_registry,
    get_emoji_long_presets,
    get_emoji_lookup_order,
    get_emoji_parser_sequences,
    get_emoji_short_presets,
    get_emoji_status_priority,
)

RESOLUTION_POLICY = "longest_match_first"

def get_atomic_registry() -> dict[str, dict[str, Any]]:
    return dict(get_emoji_atomic_registry())

def get_combo_registry() -> dict[str, dict[str, Any]]:
    return dict(get_emoji_combo_registry())

def get_presets() -> dict[str, list[dict[str, Any]]]:
    return {
        "short": [dict(item) for item in get_emoji_short_presets()],
        "long": [dict(item) for item in get_emoji_long_presets()],
    }

def get_lookup_order() -> list[str]:
    return list(get_emoji_lookup_order())

def get_status_priority() -> list[str]:
    return list(get_emoji_status_priority())

def get_registry_sequences() -> list[dict[str, Any]]:
    return [dict(item) for item in get_emoji_parser_sequences()]

def get_registry_contract() -> dict[str, Any]:
    return {
        "resolution_policy": RESOLUTION_POLICY,
        "lookup_order": get_lookup_order(),
        "status_priority": get_status_priority(),
        "atomic_count": len(get_atomic_registry()),
        "combo_count": len(get_combo_registry()),
        "short_preset_count": len(get_presets()["short"]),
        "long_preset_count": len(get_presets()["long"]),
    }
