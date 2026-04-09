"""registry.py — Engine-facing handler registry.

Core dispatch resolves handlers through this module only. No framework, platform,
or alternate runtime may populate canonical behavior from outside the baseline.
"""

from __future__ import annotations

from typing import Any

_TOOL_HANDLERS: dict[str, Any] = {}
_WORKER_HANDLERS: dict[str, Any] = {}


def register_tool_handler(tool_id: str, handler: Any) -> None:
    _TOOL_HANDLERS[tool_id] = handler


def register_worker_handler(worker_id: str, handler: Any) -> None:
    _WORKER_HANDLERS[worker_id] = handler


def resolve_tool_handler(tool_id: str) -> Any:
    try:
        return _TOOL_HANDLERS[tool_id]
    except KeyError as exc:
        raise ValueError(f"Unknown tool id {tool_id!r}") from exc


def resolve_worker_handler(worker_id: str) -> Any:
    try:
        return _WORKER_HANDLERS[worker_id]
    except KeyError as exc:
        raise ValueError(f"Unknown worker id {worker_id!r}") from exc


def seed_default_handlers() -> None:
    """Canonical baseline ships with no implicit external handlers."""
    return


__all__ = [
    "register_tool_handler",
    "register_worker_handler",
    "resolve_tool_handler",
    "resolve_worker_handler",
    "seed_default_handlers",
]
