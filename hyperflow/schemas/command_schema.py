from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class CommandObject:
    raw_input: str
    cleaned_text: str = ""
    tokens: List[str] = field(default_factory=list)
    intent: str = "unknown"
    mode: str = "standard"
    operations: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    output_type: str = "answer"
    output_subtype: str = ""
    intensity: str = "medium"
    priority: str = "normal"
    confidence: str = "medium"
    parser_trace: dict[str, Any] = field(default_factory=dict)
    action_routes: list[dict[str, Any]] = field(default_factory=list)
