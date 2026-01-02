from __future__ import annotations

from typing import List

from ..content_blocks import BenefitsBlock, ComparisonBlock, IngredientsBlock, SafetyBlock, UsageBlock
from ..core import Agent, Blackboard, Message
from ..models import ContentBlock, ProductData


class _BaseBlockAgent(Agent):
    block_type: str

    def _store(self, blackboard: Blackboard, block: ContentBlock, message: Message) -> List[Message]:
        blackboard.put(f"block:{self.block_type}", block, producer=self.name)
        return [Message(type="artifact_created", payload={"key": f"block:{self.block_type}"}, source=self.name, trace_id=message.trace_id)]


class BenefitsAgent(_BaseBlockAgent):
    name = "BenefitsAgent"
    block_type = "benefits"

    def __init__(self):
        self._block = BenefitsBlock()

    def can_handle(self, message: Message, blackboard: Blackboard) -> bool:
        return message.type == "generate_block:benefits" and blackboard.has("product_data") and not blackboard.has("block:benefits")

    def handle(self, message: Message, blackboard: Blackboard) -> List[Message]:
        product: ProductData = blackboard.get("product_data")
        block = self._block.process(product)
        return self._store(blackboard, block, message)


class UsageAgent(_BaseBlockAgent):
    name = "UsageAgent"
    block_type = "usage"

    def __init__(self):
        self._block = UsageBlock()

    def can_handle(self, message: Message, blackboard: Blackboard) -> bool:
        return message.type == "generate_block:usage" and blackboard.has("product_data") and not blackboard.has("block:usage")

    def handle(self, message: Message, blackboard: Blackboard) -> List[Message]:
        product: ProductData = blackboard.get("product_data")
        block = self._block.process(product)
        return self._store(blackboard, block, message)


class IngredientsAgent(_BaseBlockAgent):
    name = "IngredientsAgent"
    block_type = "ingredients"

    def __init__(self):
        self._block = IngredientsBlock()

    def can_handle(self, message: Message, blackboard: Blackboard) -> bool:
        return message.type == "generate_block:ingredients" and blackboard.has("product_data") and not blackboard.has("block:ingredients")

    def handle(self, message: Message, blackboard: Blackboard) -> List[Message]:
        product: ProductData = blackboard.get("product_data")
        block = self._block.process(product)
        return self._store(blackboard, block, message)


class SafetyAgent(_BaseBlockAgent):
    name = "SafetyAgent"
    block_type = "safety"

    def __init__(self):
        self._block = SafetyBlock()

    def can_handle(self, message: Message, blackboard: Blackboard) -> bool:
        return message.type == "generate_block:safety" and blackboard.has("product_data") and not blackboard.has("block:safety")

    def handle(self, message: Message, blackboard: Blackboard) -> List[Message]:
        product: ProductData = blackboard.get("product_data")
        block = self._block.process(product)
        return self._store(blackboard, block, message)


class ComparisonAgent(_BaseBlockAgent):
    name = "ComparisonAgent"
    block_type = "comparison"

    def __init__(self):
        self._block = ComparisonBlock()

    def can_handle(self, message: Message, blackboard: Blackboard) -> bool:
        return (
            message.type == "generate_block:comparison"
            and blackboard.has("product_data")
            and blackboard.has("competitor_product")
            and not blackboard.has("block:comparison")
        )

    def handle(self, message: Message, blackboard: Blackboard) -> List[Message]:
        product: ProductData = blackboard.get("product_data")
        competitor = blackboard.get("competitor_product")
        block = self._block.process(product, comparison_product=competitor)
        return self._store(blackboard, block, message)
