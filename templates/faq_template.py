from typing import Any, Dict, List

from ..models import ContentBlock, GeneratedPage, ProductData, Question
from .template_engine import BaseTemplate


class FAQTemplate(BaseTemplate):
    def __init__(self):
        super().__init__("faq")

    def render(
        self,
        content_blocks: List[ContentBlock],
        questions: List[Question] = None,
        product_data: ProductData = None,
        **kwargs,
    ) -> GeneratedPage:
        if questions is None:
            questions = []

        if product_data is None:
            raise ValueError("product_data is required for FAQ template")

        faq_items: List[Dict[str, Any]] = []
        for q in questions:
            faq_items.append(
                {
                    "id": 0,
                    "question": q.text,
                    "answer": self._answer(q, product_data),
                    "category": q.category.value,
                    "priority": self._get_priority(q.category.value),
                }
            )

        # Sort by category then priority (desc)
        faq_items.sort(key=lambda x: (x["category"], -x["priority"]))
        for idx, item in enumerate(faq_items, start=1):
            item["id"] = idx

        categorized: Dict[str, List[Dict[str, Any]]] = {}
        for item in faq_items:
            categorized.setdefault(item["category"], []).append(item)

        content = {
            "title": "Frequently Asked Questions",
            "introduction": "Find answers to common questions about this product. If you don't find what you're looking for, please contact our customer support team.",
            "faq_items": faq_items,
            "categorized_faq_items": categorized,
            "categories": self._get_category_summary(categorized),
            "total_questions": len(faq_items),
            "metadata": {
                "last_updated": "2025-12-25",
                "template": self.name,
                "source_blocks": [b.block_type for b in content_blocks],
            },
        }

        return GeneratedPage(
            page_type="faq",
            title="FAQ",
            content=content,
            metadata={
                "template_used": self.name,
                "content_blocks_used": len(content_blocks),
                "questions_processed": len(questions),
            },
        )

    def _answer(self, question: Question, product_data: ProductData) -> str:
        q = question.text.lower()

        if question.category.value == "informational":
            return (
                f"{product_data.name} is a vitamin C serum with {product_data.concentration}. "
                f"Key ingredients: {', '.join(product_data.key_ingredients)}. "
                f"Suitable for: {', '.join(product_data.skin_types)}."
            )

        if question.category.value == "usage":
            return product_data.usage_instructions

        if question.category.value == "safety":
            return f"Reported side effect: {product_data.side_effects}."

        if question.category.value == "purchase":
            if "worth" in q:
                return f"The listed price is {product_data.price}. Whether it's worth it depends on your preferences and budget."
            if "how much" in q or "cost" in q or "price" in q:
                return f"Price: {product_data.price}."
            if "where" in q or "buy" in q:
                return f"The dataset includes the price ({product_data.price}) but does not include purchase locations."
            if "size" in q:
                return "The dataset does not include the product size."
            return f"Price: {product_data.price}."

        return (
            f"{product_data.name} has {product_data.concentration} with key ingredients: {', '.join(product_data.key_ingredients)} "
            f"and benefits: {', '.join(product_data.benefits)}. A detailed comparison requires the alternative product's data."
        )

    def _get_priority(self, category: str) -> int:
        priorities = {
            "informational": 3,
            "safety": 5,
            "usage": 4,
            "purchase": 2,
            "comparison": 1,
        }
        return priorities.get(category, 1)

    def _get_category_summary(self, categorized_faqs: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        return {
            category: {"count": len(items), "description": self._get_category_description(category)}
            for category, items in categorized_faqs.items()
        }

    def _get_category_description(self, category: str) -> str:
        descriptions = {
            "informational": "Basic product information and ingredients",
            "safety": "Safety precautions and potential side effects",
            "usage": "How to use the product effectively",
            "purchase": "Pricing and purchasing information",
            "comparison": "How this product compares to alternatives",
        }
        return descriptions.get(category, "General information")
