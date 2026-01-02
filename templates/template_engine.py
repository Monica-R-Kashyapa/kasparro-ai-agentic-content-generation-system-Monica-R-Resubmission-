from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ..models import ContentBlock, GeneratedPage


class BaseTemplate(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def render(self, content_blocks: List[ContentBlock], **kwargs) -> GeneratedPage:
        raise NotImplementedError


class TemplateEngine:
    def __init__(self):
        from .faq_template import FAQTemplate
        from .product_template import ProductTemplate
        from .comparison_template import ComparisonTemplate

        self._templates: Dict[str, BaseTemplate] = {
            "faq": FAQTemplate(),
            "product": ProductTemplate(),
            "comparison": ComparisonTemplate(),
        }

    def list_templates(self) -> List[str]:
        return sorted(self._templates.keys())

    def render_page(self, template_name: str, content_blocks: List[ContentBlock], **kwargs) -> GeneratedPage:
        if template_name not in self._templates:
            raise ValueError(f"Unknown template: {template_name}")
        return self._templates[template_name].render(content_blocks=content_blocks, **kwargs)
