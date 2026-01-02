from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from .blackboard import Blackboard
from .messages import Message


class Agent(ABC):
    name: str

    @abstractmethod
    def can_handle(self, message: Message, blackboard: Blackboard) -> bool:
        raise NotImplementedError

    @abstractmethod
    def handle(self, message: Message, blackboard: Blackboard) -> List[Message]:
        raise NotImplementedError
