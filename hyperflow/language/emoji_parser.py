from __future__ import annotations

from functools import lru_cache
from typing import Any
from unicodedata import normalize

from hyperflow.config import get_emoji_parser_integration, resolve_output_hint
from hyperflow.language.emoji_registry import (
    RESOLUTION_POLICY,
    get_atomic_registry,
    get_lookup_order,
    get_registry_sequences,
    get_status_priority,
)
from hyperflow.language.token_registry import get_token_info, known_tokens


SPECIFICITY_PRIORITY = {
    "combo_registry": 0,
    "short_presets": 1,
    "long_presets": 2,
    "atomic_registry": 3,
}


def _build_token_trie(sequences: tuple[tuple[str, str, str, str, int], ...]) -> dict[str, Any]:
    root: dict[str, Any] = {}
    for emoji, kind, name, status, order in sequences:
        node = root
        for ch in emoji:
            node = node.setdefault(ch, {})
        node.setdefault("_entries", []).append(
            {
                "emoji": emoji,
                "kind": kind,
                "name": name,
                "status": status,
                "order": order,
            }
        )
    return root


@lru_cache(maxsize=1)
def _status_rank() -> dict[str, int]:
    return {status: idx for idx, status in enumerate(get_status_priority())}


@lru_cache(maxsize=1)
def _control_trie() -> dict[str, Any]:
    configured = list(get_registry_sequences())
    seen = {item["emoji"] for item in configured}
    for token in known_tokens():
        if token in seen:
            continue
        info = get_token_info(token)
        configured.append(
            {
                "emoji": token,
                "kind": "atomic_registry",
                "name": str(info.get("meaning", token)),
                "metadata": {
                    "status": str(info.get("status", "experimental")),
                    "expected_output": list(info.get("expected_output", [])),
                    "default_edde_phase": list(info.get("default_edde_phase", [])),
                    "default_mps": info.get("default_mps"),
                },
            }
        )

    sequences = tuple(
        (
            item["emoji"],
            str(item["kind"]),
            str(item["name"]),
            str(item["metadata"].get("status", "experimental")),
            index,
        )
        for index, item in enumerate(configured)
    )
    return _build_token_trie(sequences)


@lru_cache(maxsize=1)
def _atomic_trie() -> dict[str, Any]:
    atomic_entries = []
    seen = set()
    atomic_registry = get_atomic_registry()
    for index, emoji in enumerate(known_tokens()):
        info = atomic_registry.get(emoji, get_token_info(emoji))
        if emoji in seen:
            continue
        seen.add(emoji)
        atomic_entries.append(
            (emoji, "atomic_registry", str(info.get("meaning", emoji)), str(info.get("status", "experimental")), index)
        )
    return _build_token_trie(tuple(atomic_entries))


@lru_cache(maxsize=1)
def _sequence_metadata() -> dict[tuple[str, str, str], dict[str, Any]]:
    metadata: dict[tuple[str, str, str], dict[str, Any]] = {}
    for item in get_registry_sequences():
        metadata[(item["emoji"], str(item["kind"]), str(item["name"]))] = dict(item["metadata"])
    return metadata


@lru_cache(maxsize=1)
def _normalization_mode() -> str:
    return str(get_emoji_parser_integration().get("normalization", {}).get("unicode_normalization", "NFC"))


@lru_cache(maxsize=1)
def _lookup_order() -> list[str]:
    return [str(item).strip() for item in get_lookup_order() if str(item).strip()]


@lru_cache(maxsize=1)
def _kind_rank() -> dict[str, int]:
    order = _lookup_order() or ["combo_registry", "short_presets", "long_presets", "atomic_registry"]
    return {kind: idx for idx, kind in enumerate(order)}


def _normalize_text(text: str) -> str:
    normalized = normalize(_normalization_mode(), text)
    if get_emoji_parser_integration().get("normalization", {}).get("trim_whitespace", True):
        normalized = normalized.strip()
    return normalized


def _best_entry(entries: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not entries:
        return None
    return sorted(
        entries,
        key=lambda entry: (
            _kind_rank().get(str(entry.get("kind", "atomic_registry")), 99),
            _status_rank().get(str(entry.get("status", "experimental")), 99),
            int(entry.get("order", 9999)),
        ),
    )[0]


def _longest_entry_at(text: str, start: int, trie: dict[str, Any]) -> dict[str, Any] | None:
    node = trie
    i = start
    longest: dict[str, Any] | None = None

    while i < len(text) and text[i] in node:
        node = node[text[i]]
        i += 1
        entries = node.get("_entries")
        if entries:
            candidate = _best_entry(entries)
            if candidate is not None:
                longest = candidate

    return longest


def _decompose_to_atoms(sequence: str) -> list[str]:
    atoms: list[str] = []
    i = 0
    trie = _atomic_trie()
    while i < len(sequence):
        matched = _longest_entry_at(sequence, i, trie)
        if matched is not None:
            atoms.append(str(matched["emoji"]))
            i += len(str(matched["emoji"]))
            continue
        i += 1
    return atoms


def _unique_extend(target: list[str], values: list[str]) -> None:
    for value in values:
        if value not in target:
            target.append(value)


def _metadata_for(entry: dict[str, Any]) -> dict[str, Any]:
    metadata = _sequence_metadata().get((str(entry["emoji"]), str(entry["kind"]), str(entry["name"])))
    if metadata is not None:
        return metadata
    info = get_token_info(str(entry["emoji"]))
    return {
        "status": info.get("status", entry.get("status", "experimental")),
        "expected_output": info.get("expected_output", []),
        "default_edde_phase": info.get("default_edde_phase", []),
        "default_mps": info.get("default_mps"),
    }


def _parser_output_hint(entry: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    raw_outputs = [str(item) for item in metadata.get("expected_output", []) if str(item)]
    return {
        "kind": str(entry["kind"]),
        "name": str(entry["name"]),
        "emoji": str(entry["emoji"]),
        "status": str(metadata.get("status", entry.get("status", "experimental"))),
        "mps_mode": metadata.get("mps_mode", metadata.get("default_mps")),
        "edde_phase": [str(item) for item in metadata.get("edde_phase", metadata.get("default_edde_phase", [])) if str(item)],
        "expected_output": raw_outputs,
        "runtime_output": [resolve_output_hint(item)[0] for item in raw_outputs],
        "runtime_subtype": [resolve_output_hint(item)[1] for item in raw_outputs if resolve_output_hint(item)[1]],
    }


def parse_emoji_controls(text: str) -> dict[str, Any]:
    normalized = _normalize_text(text)
    trie = _control_trie()
    i = 0
    tokens: list[str] = []
    unmatched_atoms: list[str] = []
    resolved_edde_phase: list[str] = []
    resolved_output_types: list[str] = []
    runtime_output_types: list[str] = []
    resolved_output_subtypes: list[str] = []
    trace: list[dict[str, Any]] = []
    matched_sequences: list[str] = []
    resolved_mps_mode = 0
    primary_match: dict[str, Any] | None = None
    matched_combo: str | None = None
    matched_preset: str | None = None

    while i < len(normalized):
        matched = _longest_entry_at(normalized, i, trie)
        if matched is None:
            i += 1
            continue

        metadata = _metadata_for(matched)
        parser_hint = _parser_output_hint(matched, metadata)
        trace.append(parser_hint)
        matched_sequences.append(str(matched["emoji"]))
        resolved_mps_mode = max(resolved_mps_mode, int(parser_hint["mps_mode"] or 0))
        _unique_extend(resolved_edde_phase, list(parser_hint["edde_phase"]))
        _unique_extend(resolved_output_types, list(parser_hint["expected_output"]))
        _unique_extend(runtime_output_types, list(parser_hint["runtime_output"]))
        _unique_extend(resolved_output_subtypes, [item for item in parser_hint.get("runtime_subtype", []) if item])

        if primary_match is None:
            primary_match = parser_hint

        if matched["kind"] == "combo_registry" and matched_combo is None:
            matched_combo = str(matched["emoji"])
        elif matched["kind"] in {"short_presets", "long_presets"} and matched_preset is None:
            matched_preset = str(matched["name"])

        if matched["kind"] == "atomic_registry":
            token = str(matched["emoji"])
            tokens.append(token)
            unmatched_atoms.append(token)
        else:
            tokens.extend(_decompose_to_atoms(str(matched["emoji"])))

        i += len(str(matched["emoji"]))

    parser_decisions = [
        {
            "sequence": item.get("emoji"),
            "kind": item.get("kind"),
            "name": item.get("name"),
            "status": item.get("status"),
            "resolved_phase": list(item.get("edde_phase", [])),
            "runtime_output": list(item.get("runtime_output", [])),
        }
        for item in trace
    ]

    return {
        "tokens": tokens,
        "matched_combo": matched_combo,
        "matched_preset": matched_preset,
        "matched_sequences": matched_sequences,
        "unmatched_atoms": unmatched_atoms,
        "resolved_mps_mode": resolved_mps_mode or None,
        "resolved_edde_phase": resolved_edde_phase,
        "resolved_output_types": resolved_output_types,
        "runtime_output_types": runtime_output_types,
        "resolved_output_subtypes": resolved_output_subtypes,
        "primary_name": primary_match.get("name") if primary_match else None,
        "primary_match_type": primary_match.get("kind") if primary_match else None,
        "primary_status": primary_match.get("status") if primary_match else None,
        "resolution_policy": RESOLUTION_POLICY,
        "parser_decisions": parser_decisions,
        "trace": trace,
    }


def extract_tokens(text: str) -> list[str]:
    return parse_emoji_controls(text)["tokens"]


def strip_tokens(text: str, tokens: list[str], matched_sequences: list[str] | None = None) -> str:
    cleaned = text
    for sequence in sorted(matched_sequences or [], key=len, reverse=True):
        cleaned = cleaned.replace(sequence, " ")
    for token in sorted(tokens, key=len, reverse=True):
        cleaned = cleaned.replace(token, " ")
    return " ".join(cleaned.split())
