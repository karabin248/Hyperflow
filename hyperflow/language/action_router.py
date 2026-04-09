from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any
from unicodedata import normalize

from hyperflow.config import get_emoji_action_route_keys, get_emoji_action_routes
from hyperflow.engine.action_registry import get_registered_action


_TARGET_INLINE_PATTERNS = (
    re.compile(r"^\{(?P<target>[^{}]+)\}(?P<rest>.*)$"),
    re.compile(r"^\[(?P<target>[^\[\]]+)\](?P<rest>.*)$"),
)
_SYNTHETIC_SIGNAL_ROUTES = {
    "💎": {
        "action_id": "💎",
        "command": "signal:💎",
        "default_args": {},
        "safe_to_execute": False,
    }
}


@dataclass(frozen=True)
class EmojiActionMatch:
    emoji: str
    action_id: str
    signal: str
    command: str
    segment: str
    arguments: dict[str, str]
    missing_args: list[str]
    safe_to_execute: bool
    handler_name: str | None
    target: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "emoji": self.emoji,
            "action_id": self.action_id,
            "signal": self.signal,
            "command": self.command,
            "segment": self.segment,
            "arguments": dict(self.arguments),
            "missing_args": list(self.missing_args),
            "safe_to_execute": self.safe_to_execute,
            "handler_name": self.handler_name,
            "target": self.target,
        }


def _normalize_text(text: str) -> str:
    return normalize("NFC", text or "").strip()


def is_valid_target(target: str) -> bool:
    normalized = str(target or "").strip()
    return bool(normalized) and len(normalized) < 100


def _find_matches(text: str) -> list[tuple[int, int, str]]:
    keys = tuple(sorted({*get_emoji_action_route_keys(), *tuple(_SYNTHETIC_SIGNAL_ROUTES)}, key=len, reverse=True))
    matches: list[tuple[int, int, str]] = []
    i = 0
    while i < len(text):
        matched = None
        for emoji in keys:
            if text.startswith(emoji, i):
                matched = emoji
                break
        if matched is None:
            i += 1
            continue
        matches.append((i, i + len(matched), matched))
        i += len(matched)
    return matches


def _segment_for(text: str, matches: list[tuple[int, int, str]], index: int) -> str:
    _start, end, _emoji = matches[index]
    next_start = matches[index + 1][0] if index + 1 < len(matches) else len(text)
    return text[end:next_start].strip(" \t\n,;|")


def _extract_target(emoji: str, segment: str) -> tuple[str | None, str]:
    stripped = str(segment or "").strip()

    if emoji == "💎":
        for pattern in _TARGET_INLINE_PATTERNS:
            matched = pattern.match(stripped)
            if matched:
                target = str(matched.group("target")).strip()
                rest = str(matched.group("rest") or "").strip(" \t\n,;|")
                return target if is_valid_target(target) else None, rest
        return None, stripped

    if emoji == "🎯":
        parts = stripped.split(None, 1)
        if len(parts) == 1 and parts[0]:
            target = parts[0].strip()
            return target if is_valid_target(target) else None, ""
        return None, stripped

    return None, stripped


def _capture_arguments(spec: dict[str, Any], segment: str, emoji: str) -> tuple[dict[str, str], list[str], str | None, str]:
    target, remaining_segment = _extract_target(emoji, segment)
    arguments = {str(key): str(value) for key, value in spec.get("default_args", {}).items()}
    pattern = str(spec.get("arg_pattern", "")).strip()

    if emoji == "🎯" and target:
        arguments["target"] = target
        return arguments, [], target, remaining_segment

    if not pattern:
        return arguments, [], target, remaining_segment

    compiled = re.compile(pattern)
    matched = compiled.match(remaining_segment)
    if matched:
        for key, value in matched.groupdict().items():
            if value is not None:
                arguments[str(key)] = str(value).strip()

    group_names = list(compiled.groupindex)
    missing = [name for name in group_names if not arguments.get(name)]
    return arguments, missing, target, remaining_segment


def route_emoji_actions(text: str) -> dict[str, Any]:
    normalized = _normalize_text(text)
    routes = {**get_emoji_action_routes(), **_SYNTHETIC_SIGNAL_ROUTES}
    matches = _find_matches(normalized)

    structured_matches: list[EmojiActionMatch] = []
    errors: list[str] = []

    for index, (_start, _end, emoji) in enumerate(matches):
        spec = routes.get(emoji)
        if spec is None:
            continue
        segment = _segment_for(normalized, matches, index)
        arguments, missing_args, target, normalized_segment = _capture_arguments(spec, segment, emoji)
        handler = get_registered_action(str(spec.get("action_id", "")))
        safe_flag = bool(spec.get("safe_to_execute", False)) and not missing_args and handler is not None
        action = EmojiActionMatch(
            emoji=emoji,
            action_id=str(spec.get("action_id", "")),
            signal=emoji,
            command=str(spec.get("command", "")),
            segment=normalized_segment,
            arguments=arguments,
            missing_args=missing_args,
            safe_to_execute=safe_flag,
            handler_name=handler.handler_name if handler else None,
            target=target,
        )
        structured_matches.append(action)
        if missing_args:
            errors.append(f"missing_args:{emoji}:{','.join(missing_args)}")

    return {
        "matched": [item.to_dict() for item in structured_matches],
        "errors": errors,
        "safe_to_execute": bool(structured_matches) and all(item.safe_to_execute for item in structured_matches),
    }


__all__ = [
    "EmojiActionMatch",
    "is_valid_target",
    "route_emoji_actions",
]
