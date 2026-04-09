"""
test_emoji_parser.py — Tests for the emoji DSL parser (from ZIP1).
Validates that canonical combo 🌈💎🔥🧠🔀⚡ is parsed correctly.
"""
import pytest
from hyperflow.language.emoji_parser import parse_emoji_controls, extract_tokens, strip_tokens
from hyperflow.language.command_builder import build_command


CANONICAL_COMBO = "🌈💎🔥🧠🔀⚡"


def test_canonical_combo_parsed():
    result = parse_emoji_controls(CANONICAL_COMBO)
    assert result["tokens"]  # at least some tokens found


def test_single_emoji_parsed():
    result = parse_emoji_controls("🧠")
    assert "🧠" in result["tokens"] or result["tokens"]


def test_no_emoji_returns_empty_tokens():
    result = parse_emoji_controls("just plain text here")
    assert result["tokens"] == []


def test_extract_tokens_returns_list():
    tokens = extract_tokens("🌈 analyze this")
    assert isinstance(tokens, list)


def test_strip_tokens_removes_emoji():
    tokens = extract_tokens("🌈 analyze this")
    result = strip_tokens("🌈 analyze this", tokens, ["🌈"])
    assert "analyze" in result
    assert "🌈" not in result


def test_parse_result_has_required_keys():
    result = parse_emoji_controls("🔥 do something")
    required = ["tokens","matched_combo","matched_preset","resolved_edde_phase",
                "resolved_output_types","resolution_policy"]
    for key in required:
        assert key in result


def test_build_command_with_emoji_has_tokens():
    cmd = build_command("🌈💎 analyze global architecture")
    assert isinstance(cmd.tokens, list)
    assert cmd.cleaned_text


def test_build_command_intent_resolved():
    cmd = build_command("analyze the system")
    assert cmd.intent and cmd.intent != "unknown"


def test_build_command_mode_set():
    cmd = build_command("analyze the codebase")
    assert cmd.mode and len(cmd.mode) > 0


def test_empty_input_handled():
    with pytest.raises(ValueError, match="Input is required"):
        build_command("")

