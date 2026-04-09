"""Replay helper for deterministic trace-based debugging."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from hyperflow.contracts.version_policy import CONTRACT_VERSION, assert_contract_version


def replay_trace(trace: Mapping[str, Any]) -> dict[str, Any]:
    version = str(trace.get('replay_contract_version') or trace.get('contract_version') or CONTRACT_VERSION)
    assert_contract_version(version)
    payload = trace.get('replay_output')
    if not isinstance(payload, Mapping):
        raise ValueError('Trace is not replayable: missing replay_output mapping')
    return deepcopy(dict(payload))
