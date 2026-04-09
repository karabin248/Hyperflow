from hyperflow.language.emoji_parser import extract_tokens, parse_emoji_controls, strip_tokens


def test_extract_tokens():
    raw = "🌈💎🔥🧠🔀⚡ Task: test"
    tokens = extract_tokens(raw)
    assert tokens == ["🌈", "💎", "🔥", "🧠", "🔀", "⚡"]


def test_extract_tokens_with_zwj_sequence():
    raw = "🧑‍💻🔍 Rollout plan"
    tokens = extract_tokens(raw)
    assert tokens == ["🧑‍💻", "🔍"]


def test_strip_tokens():
    raw = "🌈💎🔥 Task: test"
    parsed = parse_emoji_controls(raw)
    cleaned = strip_tokens(raw, parsed["tokens"], parsed["matched_sequences"])
    assert "🌈" not in cleaned
    assert "Task:" in cleaned


def test_extract_tokens_with_variation_selector():
    raw = "🛡️📊 safe mode"
    tokens = extract_tokens(raw)
    assert tokens == ["🛡️", "📊"]


def test_extract_tokens_keeps_order_with_repeated_multi_codepoint():
    raw = "🧑‍💻x🧑‍💻🛡️"
    tokens = extract_tokens(raw)
    assert tokens == ["🧑‍💻", "🧑‍💻", "🛡️"]


def test_combo_first_parser_resolves_combo_and_preserves_atomic_tokens():
    parsed = parse_emoji_controls("🌈💎🧠 and then explain")
    assert parsed["matched_combo"] == "🌈💎🧠"
    assert parsed["tokens"] == ["🌈", "💎", "🧠"]
    assert parsed["resolved_edde_phase"] == ["scan", "extract", "reason"]


def test_preset_parser_resolves_short_preset_and_cleans_full_sequence():
    raw = "💎🧠🧱📊📋 prepare this"
    parsed = parse_emoji_controls(raw)
    cleaned = strip_tokens(raw, parsed["tokens"], parsed["matched_sequences"])
    assert parsed["matched_preset"] == "Structured Plan"
    assert cleaned == "prepare this"


def test_canonical_cycle_resolves_options_before_choice():
    parsed = parse_emoji_controls("🌈💎🔥🧠🔀⚡ Task: test")
    assert parsed["matched_combo"] == "🌈💎🔥🧠🔀⚡"
    assert parsed["resolved_edde_phase"] == ["scan", "extract", "build", "reason", "remix", "deliver"]
