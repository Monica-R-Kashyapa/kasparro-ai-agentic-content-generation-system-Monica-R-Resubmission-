from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .agent import Agent
from .blackboard import Blackboard
from .messages import Message


@dataclass
class AgentRegistry:
    agents: List[Agent] = field(default_factory=list)

    def register(self, agent: Agent) -> None:
        self.agents.append(agent)

    def route(self, message: Message, blackboard: Blackboard) -> List[Agent]:
        return [a for a in self.agents if a.can_handle(message, blackboard)]
