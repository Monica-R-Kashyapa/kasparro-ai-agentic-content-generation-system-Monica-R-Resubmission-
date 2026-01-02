from __future__ import annotations

from typing import List

from ..core import Agent, Blackboard, Message
from ..models import ContentBlock, ProductData, Question
from ..templates import TemplateEngine


class PageRenderAgent(Agent):
    name = "PageRenderAgent"

    def __init__(self):
        self._engine = TemplateEngine()

    def can_handle(self, message: Message, blackboard: Blackboard) -> bool:
        if not message.type.startswith("render_page:"):
            return False
        page_type = message.type.split(":", 1)[1]
        output_key = self._output_key(page_type)
        return blackboard.has("product_data") and not blackboard.has(output_key)

    def handle(self, message: Message, blackboard: Blackboard) -> List[Message]:
        page_type = message.type.split(":", 1)[1]
        product: ProductData = blackboard.get("product_data")

        blocks: List[ContentBlock] = [
            blackboard.get("block:benefits"),
            blackboard.get("block:usage"),
            blackboard.get("block:ingredients"),
            blackboard.get("block:safety"),
        ]

        if page_type == "comparison":
            blocks.append(blackboard.get("block:comparison"))

        # Questions are only required for FAQ
        additional = {"product_data": product}
        if page_type == "faq":
            additional["questions"] = blackboard.get("questions", [])

        page = self._engine.render_page(template_name=page_type, content_blocks=blocks, **additional)

        # Store exactly the JSON content schema under the output filename key
        output_key = self._output_key(page_type)
        blackboard.put(output_key, page.content, producer=self.name)
        return [Message(type="artifact_created", payload={"key": output_key}, source=self.name, trace_id=message.trace_id)]

    def _output_key(self, page_type: str) -> str:
        if page_type == "faq":
            return "faq.json"
        if page_type == "product":
            return "product_page.json"
        if page_type == "comparison":
            return "comparison_page.json"
        raise ValueError(f"Unknown page_type: {page_type}")
