"""Canonical runtime invariants and contract helpers."""

from .version_policy import CONTRACT_VERSION, assert_contract_version, is_compatible_contract_version
from .runtime_invariants import (
    CANONICAL_EMOJI_SEQUENCE,
    CANONICAL_PHASE_ORDER,
    assert_behavior_registered,
    assert_canonical_phase_order,
    get_registered_behavior_ids,
    scan_for_unauthorized_extension_paths,
)

__all__ = [
    "CONTRACT_VERSION",
    "assert_contract_version",
    "is_compatible_contract_version",
    "CANONICAL_EMOJI_SEQUENCE",
    "CANONICAL_PHASE_ORDER",
    "assert_behavior_registered",
    "assert_canonical_phase_order",
    "get_registered_behavior_ids",
    "scan_for_unauthorized_extension_paths",
]
