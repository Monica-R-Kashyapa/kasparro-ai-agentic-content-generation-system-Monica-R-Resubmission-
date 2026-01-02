from typing import Any, Dict, List

from ..models import ContentBlock, ProductData
from .base_block import BaseContentBlock


class BenefitsBlock(BaseContentBlock):
    def __init__(self):
        super().__init__("benefits")

    def get_rules(self) -> Dict[str, Any]:
        return {"format": "bulleted_list", "max_items": 10}

    def process(self, product_data: ProductData, **kwargs) -> ContentBlock:
        rules = self.get_rules()
        benefits: List[str] = [b.strip() for b in product_data.benefits if b and b.strip()]
        if len(benefits) > rules["max_items"]:
            benefits = benefits[: rules["max_items"]]

        return ContentBlock(
            block_type=self.block_type,
            content={
                "title": "Key Benefits",
                "benefits": benefits,
                "format": rules["format"],
                "total_count": len(benefits),
            },
            metadata={"generated_by": self.block_type},
        )
