"""Hard guards for canonical runtime invariants."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from hyperflow.config import get_emoji_action_routes, get_emoji_combo_registry

CANONICAL_EMOJI_SEQUENCE = "🌈💎🔥🧠🔀⚡"
LEGACY_REVERSED_SEQUENCE = "🌈💎🔥🧠⚡🔀"
CANONICAL_PHASE_ORDER = ("scan", "extract", "build", "reason", "remix", "deliver")
ALLOWED_EXTENSION_PATHS = frozenset(
    {
        "hyperflow/language/command_builder.py",
        "hyperflow/language/emoji_parser.py",
        "hyperflow/language/section_parser.py",
        "hyperflow/runtime_kernel.py",
        "hyperflow/engine/runtime_kernel.py",
        "hyperflow/interface/cli.py",
        "hyperflow/api/edde_api.py",
    }
)


def assert_canonical_phase_order(phases: Iterable[str]) -> list[str]:
    normalized = [str(item) for item in phases]
    if normalized != list(CANONICAL_PHASE_ORDER):
        raise ValueError(
            "Canonical EDDE phase order drift detected: "
            f"got {normalized!r}, expected {list(CANONICAL_PHASE_ORDER)!r}."
        )
    return normalized


def scan_for_unauthorized_extension_paths(root: Path) -> list[str]:
    root = Path(root)
    findings: list[str] = []
    for path in root.rglob('*.py'):
        rel = path.relative_to(root).as_posix()
        if not rel.startswith('hyperflow/') or '/tests/' in f'/{rel}/':
            continue
        name = path.name
        if rel in ALLOWED_EXTENSION_PATHS:
            continue
        if name.endswith('parser.py') or name.endswith('runtime.py'):
            findings.append(rel)
    return sorted(findings)


def get_registered_behavior_ids() -> set[str]:
    action_ids = {
        str(route.get('action_id', '')).strip()
        for route in get_emoji_action_routes().values()
        if str(route.get('action_id', '')).strip()
    }
    combo_ids = {
        str(entry.get('name', '')).strip()
        for entry in get_emoji_combo_registry().values()
        if str(entry.get('name', '')).strip()
    }
    return action_ids | combo_ids


def assert_behavior_registered(action_id: str) -> str:
    normalized = str(action_id or '').strip()
    if not normalized:
        raise ValueError('Behavior id must be non-empty')
    if normalized not in get_registered_behavior_ids():
        raise ValueError(f"Unregistered behavior detected: {normalized!r}")
    return normalized
