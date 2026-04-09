from collections import deque
from dataclasses import dataclass, field
from typing import Any, Deque


@dataclass
class SessionRecord:
    run_id: str
    raw_input: str
    intent: str
    mode: str
    summary: str
    observer_status: str


@dataclass
class SessionMemory:
    max_items: int = 20
    records: Deque[SessionRecord] = field(default_factory=lambda: deque(maxlen=20))

    def add_record(self, record: SessionRecord) -> None:
        self.records.append(record)

    def get_recent(self, limit: int = 5) -> list[SessionRecord]:
        return list(self.records)[-limit:]

    def clear(self) -> None:
        self.records.clear()


SESSION_MEMORY = SessionMemory()
