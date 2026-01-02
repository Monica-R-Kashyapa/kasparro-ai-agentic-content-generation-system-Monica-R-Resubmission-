from typing import Any, Dict, List

from ..models import ContentBlock, ProductData
from .base_block import BaseContentBlock


class IngredientsBlock(BaseContentBlock):
    def __init__(self):
        super().__init__("ingredients")

    def get_rules(self) -> Dict[str, Any]:
        return {"format": "list"}

    def process(self, product_data: ProductData, **kwargs) -> ContentBlock:
        rules = self.get_rules()
        ingredients: List[str] = [i.strip() for i in product_data.key_ingredients if i and i.strip()]
        main = ingredients[0] if ingredients else ""
        supporting = ingredients[1:] if len(ingredients) > 1 else []
        supporting_objs = [{"name": s, "description": "Not specified"} for s in supporting]

        return ContentBlock(
            block_type=self.block_type,
            content={
                "title": "Key Ingredients",
                "main_ingredient": {
                    "name": main,
                    "concentration": product_data.concentration,
                    "description": "Not specified",
                },
                "supporting_ingredients": supporting_objs,
                "format": rules["format"],
                "total_count": len(ingredients),
            },
            metadata={"generated_by": self.block_type},
        )
