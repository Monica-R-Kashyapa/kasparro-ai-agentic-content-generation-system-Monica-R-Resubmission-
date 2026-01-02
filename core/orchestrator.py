from __future__ import annotations

from collections import deque
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any, Deque, Dict, List

from .blackboard import Blackboard
from .messages import Message
from .registry import AgentRegistry


def _to_jsonable(obj: Any) -> Any:
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, Enum):
        return obj.value
    if is_dataclass(obj):
        return {k: _to_jsonable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, dict):
        return {str(k): _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_jsonable(v) for v in obj]
    return str(obj)


class EventLoopOrchestrator:
    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    def run(self, initial_messages: List[Message], goals: List[str]) -> Blackboard:
        bb = Blackboard(goals=set(goals))
        queue: Deque[Message] = deque(initial_messages)

        while queue:
            msg = queue.popleft()
            bb.event_log.append({"event": "message", "type": msg.type, "source": msg.source})

            handlers = self.registry.route(msg, bb)
            if not handlers:
                bb.event_log.append({"event": "unhandled", "type": msg.type})
                continue

            for agent in handlers:
                out_messages = agent.handle(msg, bb)
                for out in out_messages:
                    queue.append(out)

            if self._goals_satisfied(bb):
                break

        return bb

    def _goals_satisfied(self, bb: Blackboard) -> bool:
        if not bb.goals:
            return False
        return all(bb.has(goal) for goal in bb.goals)


def blackboard_to_artifacts(bb: Blackboard) -> Dict[str, Any]:
    artifacts = bb.get("artifacts", {})
    return _to_jsonable(artifacts)
