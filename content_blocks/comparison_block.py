from typing import Any, Dict, List

from ..models import ContentBlock, ProductData
from .base_block import BaseContentBlock


class ComparisonBlock(BaseContentBlock):
    def __init__(self):
        super().__init__("comparison")

    def get_rules(self) -> Dict[str, Any]:
        return {"format": "json"}

    def process(self, product_data: ProductData, **kwargs) -> ContentBlock:
        comparison_product = kwargs.get("comparison_product")
        if not isinstance(comparison_product, dict):
            raise ValueError("comparison_product is required for comparison block")

        product_a = {
            "name": product_data.name,
            "concentration": product_data.concentration,
            "skin_types": product_data.skin_types,
            "key_ingredients": product_data.key_ingredients,
            "benefits": product_data.benefits,
            "price": product_data.price,
        }
        product_b = comparison_product

        def _compare_lists(a: List[str], b: List[str]) -> Dict[str, Any]:
            a_set, b_set = set(a), set(b)
            return {
                "shared": sorted(list(a_set & b_set)),
                "only_a": sorted(list(a_set - b_set)),
                "only_b": sorted(list(b_set - a_set)),
            }

        points = {
            "ingredients": _compare_lists(product_a.get("key_ingredients", []), product_b.get("key_ingredients", [])),
            "benefits": _compare_lists(product_a.get("benefits", []), product_b.get("benefits", [])),
            "skin_types": _compare_lists(product_a.get("skin_types", []), product_b.get("skin_types", [])),
            "price": {"product_a": product_a.get("price"), "product_b": product_b.get("price")},
        }

        winners = {
            "benefits": "Tie",
            "ingredients": "Tie",
            "price": "Tie",
        }

        return ContentBlock(
            block_type=self.block_type,
            content={
                "title": f"{product_a['name']} vs {product_b.get('name', 'Product B')}",
                "product_a": product_a,
                "product_b": product_b,
                "comparison_points": points,
                "winners": winners,
            },
            metadata={"generated_by": self.block_type},
        )
