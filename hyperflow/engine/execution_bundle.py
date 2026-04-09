"""execution_bundle.py — Canonical execution result envelope."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Final, Literal

from hyperflow.contracts.version_policy import CONTRACT_VERSION, assert_contract_version
from hyperflow.engine.dispatch import DispatchPurityViolation


ObserverStatus = Literal["OK", "WARN", "FALLBACK"]
_VALID_OBSERVER_STATUSES: Final = frozenset({"OK", "WARN", "FALLBACK"})
_VALID_EXECUTION_PATHS: Final = frozenset({"edde", "workflow_step", "agent_task"})


def _validate_bundle_fields(
    observer_status: str,
    confidence: float,
    execution_path: str,
) -> None:
    if observer_status not in _VALID_OBSERVER_STATUSES:
        raise ValueError(
            "ExecutionBundle.observer_status must be one of "
            f"{sorted(_VALID_OBSERVER_STATUSES)}, got {observer_status!r}."
        )

    if not (0.0 <= confidence <= 1.0):
        raise ValueError(f"ExecutionBundle.confidence must be in [0.0, 1.0], got {confidence}.")

    base_path = execution_path.split(":")[0]
    if base_path not in _VALID_EXECUTION_PATHS:
        raise ValueError(
            "ExecutionBundle.execution_path base must be one of "
            f"{sorted(_VALID_EXECUTION_PATHS)}, got {execution_path!r}."
        )


@dataclass(frozen=True)
class ExecutionBundle:
    summary: str
    confidence: float
    observer_status: ObserverStatus
    next_step: str
    execution_path: str

    contract_version: str = CONTRACT_VERSION

    plan: tuple[str, ...] = field(default_factory=tuple)
    insights: tuple[str, ...] = field(default_factory=tuple)
    actions: tuple[str, ...] = field(default_factory=tuple)

    step_ref: str = ""
    input_payload: Any = None
    output_payload: Any = None

    error_code: str = ""
    error_message: str = ""

    def __post_init__(self) -> None:
        _validate_bundle_fields(
            observer_status=self.observer_status,
            confidence=self.confidence,
            execution_path=self.execution_path,
        )
        assert_contract_version(self.contract_version)

    def __init_subclass__(cls, **kwargs: Any) -> None:
        raise TypeError(
            "ExecutionBundle is a sealed contract and may not be subclassed "
            f"(attempted subclass: {cls.__qualname__})."
        )

    @property
    def is_error(self) -> bool:
        return bool(self.error_code)

    @property
    def is_terminal_failure(self) -> bool:
        return self.observer_status == "FALLBACK" and bool(self.error_code)

    def with_attempt_suffix(self, attempt: int) -> "ExecutionBundle":
        base = self.execution_path.split(":attempt_")[0]
        return replace(self, execution_path=f"{base}:attempt_{attempt}")
