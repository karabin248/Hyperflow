from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class RuntimeState:
    run_id: str
    phase: str = "init"
    intent: str = "unknown"
    mode: str = "standard"
    mps_level: int = 2
    mps_state: str = "Stabilize"
    observer_status: str = "OK"
    risk_state: str = "low"
    observer_rigor: str = "medium"
    # Backward-compatible alias; risk_state is the canonical field.
    risk_level: str = "low"
    plan: List[str] = field(default_factory=list)
    partial_results: List[Any] = field(default_factory=list)
    insights: List[str] = field(default_factory=list)
    next_step: str = ""
    active_target: str | None = None
    llm_errors: List[str] = field(default_factory=list)
