from dataclasses import dataclass, field
from typing import List


@dataclass
class ObserverReport:
    observer_status: str = "OK"
    issues: List[str] = field(default_factory=list)
    recommended_action: str = "continue"
    confidence_adjustment: str = "none"
    threshold_status: str = "OK"
    threshold_reason: str = "within_threshold"
