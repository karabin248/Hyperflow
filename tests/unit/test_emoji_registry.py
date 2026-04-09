from __future__ import annotations

from hyperflow.language.emoji_registry import (
    RESOLUTION_POLICY,
    get_atomic_registry,
    get_combo_registry,
    get_lookup_order,
    get_presets,
    get_registry_contract,
)


def test_emoji_registry_is_canonical_source() -> None:
    contract = get_registry_contract()
    assert RESOLUTION_POLICY == 'longest_match_first'
    assert contract['resolution_policy'] == 'longest_match_first'
    assert get_lookup_order()[0] == 'combo_registry'
    assert '🌈' in get_atomic_registry()
    assert '🌈💎🔥🧠🔀⚡' in get_combo_registry()
    presets = get_presets()
    assert isinstance(presets['short'], list)
    assert isinstance(presets['long'], list)
