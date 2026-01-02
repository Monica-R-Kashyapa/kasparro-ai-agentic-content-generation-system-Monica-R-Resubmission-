from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Set


@dataclass
class Blackboard:
    artifacts: Dict[str, Any] = field(default_factory=dict)
    goals: Set[str] = field(default_factory=set)
    event_log: List[Dict[str, Any]] = field(default_factory=list)

    def has(self, key: str) -> bool:
        return key in self.artifacts and self.artifacts[key] is not None

    def get(self, key: str, default: Any = None) -> Any:
        return self.artifacts.get(key, default)

    def put(self, key: str, value: Any, producer: str) -> None:
        self.artifacts[key] = value
        self.event_log.append({"event": "artifact_created", "key": key, "producer": producer})
