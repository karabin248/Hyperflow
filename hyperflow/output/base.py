from dataclasses import dataclass, field
from typing import Any

from hyperflow.contracts.version_policy import CONTRACT_VERSION


@dataclass
class BaseOutput:
    kind: str
    intent: str
    mode: str
    summary: str
    confidence: str
    observer_status: str
    next_step: str
    contract_version: str = CONTRACT_VERSION
    output_subtype: str = ""
    insights: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    plan: list[str] = field(default_factory=list)
    run_id: str = ""
    edde_contract: dict[str, Any] = field(default_factory=dict)
    observer_contract: dict[str, Any] = field(default_factory=dict)

    def to_dict(self, *, include_contract: bool = True) -> dict[str, Any]:
        payload = {
            "kind": self.kind,
            "intent": self.intent,
            "mode": self.mode,
            "summary": self.summary,
            "confidence": self.confidence,
            "observer_status": self.observer_status,
            "next_step": self.next_step,
            "contract_version": self.contract_version,
            "output_subtype": self.output_subtype,
            "insights": self.insights,
            "actions": self.actions,
            "plan": self.plan,
        }
        if self.run_id:
            payload["run_id"] = self.run_id
        if self.observer_contract:
            payload["observer_contract"] = self.observer_contract
        if include_contract and self.edde_contract:
            payload["edde_contract"] = self.edde_contract
        return payload
