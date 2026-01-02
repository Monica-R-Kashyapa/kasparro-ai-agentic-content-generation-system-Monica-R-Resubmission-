from typing import Any, Dict

from ..models import ContentBlock, ProductData
from .base_block import BaseContentBlock


class UsageBlock(BaseContentBlock):
    def __init__(self):
        super().__init__("usage")

    def get_rules(self) -> Dict[str, Any]:
        return {"format": "step_by_step"}

    def process(self, product_data: ProductData, **kwargs) -> ContentBlock:
        rules = self.get_rules()

        instructions = product_data.usage_instructions
        timing = {"when": "Not specified", "frequency": "Once daily"}
        lower = instructions.lower()
        if "morning" in lower:
            timing["when"] = "Morning"
        elif "evening" in lower:
            timing["when"] = "Evening"
        elif "night" in lower:
            timing["when"] = "Night"

        quantity = {"amount": "Not specified", "unit": "drops"}
        if "drops" in lower:
            import re

            m = re.search(r"(\d+)\s*[–-]?\s*(\d+)?\s*drops", lower)
            if m:
                quantity["amount"] = m.group(0).split("drops")[0].strip()

        return ContentBlock(
            block_type=self.block_type,
            content={
                "title": "How to Use",
                "steps": [instructions],
                "timing": timing,
                "quantity": quantity,
                "precautions": [],
                "format": rules["format"],
            },
            metadata={"generated_by": self.block_type},
        )
