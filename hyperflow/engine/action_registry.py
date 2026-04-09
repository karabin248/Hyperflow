from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class RegisteredAction:
    action_id: str
    handler_name: str
    handler: Callable[..., Any]


_ACTION_REGISTRY: dict[str, RegisteredAction] = {}


def emoji_action(action_id: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Register a Python handler for a structured emoji action id."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        _ACTION_REGISTRY[action_id] = RegisteredAction(
            action_id=action_id,
            handler_name=func.__name__,
            handler=func,
        )
        return func

    return decorator


def get_registered_action(action_id: str) -> RegisteredAction | None:
    return _ACTION_REGISTRY.get(action_id)


def has_registered_action(action_id: str) -> bool:
    return action_id in _ACTION_REGISTRY


def list_registered_actions() -> list[str]:
    return sorted(_ACTION_REGISTRY)


def run_action(signal: str, *args: Any, **kwargs: Any) -> Any:
    action = get_registered_action(signal)
    if action is None:
        return None
    return action.handler(*args, **kwargs)


def run_action_on_node(signal: str, target: str, *args: Any, **kwargs: Any) -> Any:
    action = get_registered_action(signal)
    if action is None:
        return None

    node_context = dict(kwargs.pop("node_context", {}) or {})
    node_context.setdefault("target", target)

    kwargs.setdefault("target", target)
    kwargs.setdefault("node_context", node_context)
    return action.handler(*args, **kwargs)


__all__ = [
    "RegisteredAction",
    "emoji_action",
    "get_registered_action",
    "has_registered_action",
    "list_registered_actions",
    "run_action",
    "run_action_on_node",
]
