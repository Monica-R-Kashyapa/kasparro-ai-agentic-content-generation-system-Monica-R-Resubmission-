from typing import Any, Dict, List

from ..models import ContentBlock, GeneratedPage
from .template_engine import BaseTemplate


class ComparisonTemplate(BaseTemplate):
    def __init__(self):
        super().__init__("comparison")

    def render(self, content_blocks: List[ContentBlock], **kwargs) -> GeneratedPage:
        comparison = None
        for b in content_blocks:
            if b.block_type == "comparison":
                comparison = b.content
                break

        if comparison is None:
            raise ValueError("comparison content block is required")

        products_overview = self._products_overview(comparison)
        winner_analysis = self._winner_analysis(comparison)
        recommendation = {
            "by_category": comparison.get("winners", {}),
            "note": "Recommendations are derived only from the provided comparison inputs.",
        }

        content = {
            "title": comparison.get("title", "Product Comparison"),
            "products_overview": products_overview,
            "detailed_comparison": comparison.get("comparison_points", {}),
            "winner_analysis": winner_analysis,
            "recommendation": recommendation,
            "metadata": {
                "last_updated": "2025-12-25",
                "template": self.name,
                "source_blocks": [b.block_type for b in content_blocks],
            },
        }

        return GeneratedPage(
            page_type="comparison",
            title="Product Comparison",
            content=content,
            metadata={
                "template_used": self.name,
                "content_blocks_used": len(content_blocks),
                "products_compared": 2,
            },
        )

    def _products_overview(self, comparison: Dict[str, Any]) -> Dict[str, Any]:
        product_a = comparison.get("product_a", {})
        product_b = comparison.get("product_b", {})
        return {
            "product_a": {
                "name": product_a.get("name"),
                "key_features": [
                    f"Concentration: {product_a.get('concentration', '')}",
                    f"Skin types: {', '.join(product_a.get('skin_types', []))}",
                    f"Price: {product_a.get('price', '')}",
                ],
                "main_benefit": (product_a.get("benefits") or [""])[0],
            },
            "product_b": {
                "name": product_b.get("name"),
                "key_features": [
                    f"Concentration: {product_b.get('concentration', '')}",
                    f"Skin types: {', '.join(product_b.get('skin_types', [])) if product_b.get('skin_types') else ''}",
                    f"Price: {product_b.get('price', '')}",
                ],
                "main_benefit": (product_b.get("benefits") or [""])[0],
            },
        }

    def _winner_analysis(self, comparison: Dict[str, Any]) -> Dict[str, Any]:
        winners = comparison.get("winners", {})
        counts: Dict[str, int] = {}
        for _, w in winners.items():
            counts[w] = counts.get(w, 0) + 1
        overall = max(counts, key=counts.get) if counts else "Tie"
        return {
            "category_winners": winners,
            "overall_winner": overall,
            "winning_score": counts.get(overall, 0),
            "analysis_summary": "Winner analysis is based on the provided winners mapping.",
        }
