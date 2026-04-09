from __future__ import annotations

from pathlib import Path

import pytest

from hyperflow.contracts.runtime_invariants import (
    assert_canonical_phase_order,
    scan_for_unauthorized_extension_paths,
)


def test_negative_guard_detects_second_parser(tmp_path: Path) -> None:
    (tmp_path / 'hyperflow' / 'language').mkdir(parents=True)
    (tmp_path / 'hyperflow' / 'language' / 'command_builder.py').write_text(
        'def build_command():\n    return None\n', encoding='utf-8'
    )
    (tmp_path / 'hyperflow' / 'language' / 'emoji_parser.py').write_text(
        'def parse_emoji_controls():\n    return {}\n', encoding='utf-8'
    )
    (tmp_path / 'hyperflow' / 'language' / 'shadow_parser.py').write_text(
        'def parse():\n    return {}\n', encoding='utf-8'
    )

    findings = scan_for_unauthorized_extension_paths(tmp_path)
    assert findings == ['hyperflow/language/shadow_parser.py']


def test_negative_guard_detects_second_runtime(tmp_path: Path) -> None:
    (tmp_path / 'hyperflow' / 'engine').mkdir(parents=True)
    (tmp_path / 'hyperflow' / 'engine' / 'runtime_kernel.py').write_text(
        'def run(command):\n    return command\n', encoding='utf-8'
    )
    (tmp_path / 'hyperflow' / 'engine' / 'fallback_runtime.py').write_text(
        'def run(command):\n    return command\n', encoding='utf-8'
    )

    findings = scan_for_unauthorized_extension_paths(tmp_path)
    assert findings == ['hyperflow/engine/fallback_runtime.py']


def test_negative_guard_rejects_swapped_canonical_phase_order() -> None:
    with pytest.raises(ValueError, match='phase order drift'):
        assert_canonical_phase_order(['scan', 'extract', 'build', 'reason', 'deliver', 'remix'])
