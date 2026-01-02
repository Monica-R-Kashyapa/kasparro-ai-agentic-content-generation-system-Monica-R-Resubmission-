from typing import Any, Dict, List

from ..models import ContentBlock, GeneratedPage, ProductData
from .template_engine import BaseTemplate


class ProductTemplate(BaseTemplate):
    def __init__(self):
        super().__init__("product")

    def render(self, content_blocks: List[ContentBlock], product_data: ProductData = None, **kwargs) -> GeneratedPage:
        if product_data is None:
            raise ValueError("product_data is required for product template")

        blocks: Dict[str, Any] = {b.block_type: b.content for b in content_blocks}

        content = {
            "title": product_data.name,
            "overview": {
                "product_name": product_data.name,
                "concentration": product_data.concentration,
                "skin_types": product_data.skin_types,
                "price": product_data.price,
            },
            "key_ingredients": blocks.get("ingredients", {}),
            "benefits": blocks.get("benefits", {}),
            "usage_instructions": blocks.get("usage", {}),
            "safety_information": blocks.get("safety", {}),
            "metadata": {
                "last_updated": "2025-12-25",
                "template": self.name,
                "source_blocks": [b.block_type for b in content_blocks],
            },
        }

        return GeneratedPage(
            page_type="product",
            title="Product Description",
            content=content,
            metadata={
                "template_used": self.name,
                "content_blocks_used": len(content_blocks),
                "sections_generated": len(content) - 1,
            },
        )
