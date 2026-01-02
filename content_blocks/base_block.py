from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseContentBlock(ABC):
    def __init__(self, block_type: str):
        self.block_type = block_type

    @abstractmethod
    def get_rules(self) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def process(self, product_data, **kwargs):
        raise NotImplementedError
