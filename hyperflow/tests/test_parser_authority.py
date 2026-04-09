from __future__ import annotations

from pathlib import Path

from hyperflow.language.command_builder import build_command
from hyperflow.language.emoji_parser import parse_emoji_controls


def _read(path: str) -> str:
    root = Path(__file__).resolve().parents[2]
    return (root / path).read_text(encoding='utf-8')


def test_parser_authority_is_command_builder_plus_emoji_parser_only() -> None:
    runtime_doc = _read('docs/architecture/canonical_runtime.md')
    assert 'parser/control -> `hyperflow.language.command_builder.build_command()`' in runtime_doc

    builder_source = _read('hyperflow/language/command_builder.py')
    parser_source = _read('hyperflow/language/emoji_parser.py')
    assert 'parse_emoji_controls' in builder_source
    assert 'RESOLUTION_POLICY' in parser_source


def test_longest_match_first_parser_trace_is_explicit() -> None:
    parsed = parse_emoji_controls('🌈💎🔥🧠🔀⚡ and continue with 🌈')
    assert parsed['resolution_policy'] == 'longest_match_first'
    assert parsed['matched_sequences'][0] == '🌈💎🔥🧠🔀⚡'
    assert parsed['parser_decisions'][0]['sequence'] == '🌈💎🔥🧠🔀⚡'


def test_command_builder_persists_parser_decisions() -> None:
    command = build_command('🌈💎🔥🧠🔀⚡ Task: prepare a rollout plan')
    assert command.parser_trace['resolution_policy'] == 'longest_match_first'
    assert command.parser_trace['parser_decisions']
    assert command.parser_trace['parser_decisions'][0]['kind'] == 'combo_registry'
