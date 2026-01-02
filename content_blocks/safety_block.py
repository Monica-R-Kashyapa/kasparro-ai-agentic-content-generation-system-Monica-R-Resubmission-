from typing import Any, Dict

from ..models import ContentBlock, ProductData
from .base_block import BaseContentBlock


class SafetyBlock(BaseContentBlock):
    def __init__(self):
        super().__init__("safety")

    def get_rules(self) -> Dict[str, Any]:
        return {"format": "categorized_warnings"}

    def process(self, product_data: ProductData, **kwargs) -> ContentBlock:
        rules = self.get_rules()
        return ContentBlock(
            block_type=self.block_type,
            content={
                "title": "Safety Information",
                "side_effects": [{"effect": product_data.side_effects}] if product_data.side_effects else [],
                "precautions": [],
                "warnings": [],
                "recommendations": [],
                "format": rules["format"],
            },
            metadata={"generated_by": self.block_type},
        )
