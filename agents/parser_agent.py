from __future__ import annotations

from typing import Any, Dict, List

from ..core import Agent, Blackboard, Message
from ..models import ProductData


class ParserAgent(Agent):
    name = "ParserAgent"

    def can_handle(self, message: Message, blackboard: Blackboard) -> bool:
        return message.type == "parse_product" and blackboard.has("raw_product_data") and not blackboard.has("product_data")

    def handle(self, message: Message, blackboard: Blackboard) -> List[Message]:
        raw: Dict[str, Any] = blackboard.get("raw_product_data")

        def _split_list(value: Any) -> List[str]:
            if value is None:
                return []
            if isinstance(value, list):
                return [str(v).strip() for v in value if str(v).strip()]
            return [v.strip() for v in str(value).split(",") if v.strip()]

        product = ProductData(
            name=str(raw.get("Product Name", "")),
            concentration=str(raw.get("Concentration", "")),
            skin_types=_split_list(raw.get("Skin Type", "")),
            key_ingredients=_split_list(raw.get("Key Ingredients", "")),
            benefits=_split_list(raw.get("Benefits", "")),
            usage_instructions=str(raw.get("How to Use", "")),
            side_effects=str(raw.get("Side Effects", "")),
            price=str(raw.get("Price", "")),
        )

        blackboard.put("product_data", product, producer=self.name)
        return [Message(type="artifact_created", payload={"key": "product_data"}, source=self.name, trace_id=message.trace_id)]
