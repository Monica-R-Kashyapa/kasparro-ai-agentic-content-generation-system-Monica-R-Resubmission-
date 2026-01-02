from __future__ import annotations

from typing import Dict, List

from ..core import Agent, Blackboard, Message
from ..models import ProductData, Question, QuestionCategory


class QuestionAgent(Agent):
    name = "QuestionAgent"

    def __init__(self):
        self.question_templates = self._initialize_templates()

    def can_handle(self, message: Message, blackboard: Blackboard) -> bool:
        return message.type == "generate_questions" and blackboard.has("product_data") and not blackboard.has("questions")

    def handle(self, message: Message, blackboard: Blackboard) -> List[Message]:
        product: ProductData = blackboard.get("product_data")

        questions: List[Question] = []
        for category, templates in self.question_templates.items():
            for template in templates:
                text = template.replace("{product_name}", product.name)
                questions.append(Question(text=text, category=category, answer_template=""))

        blackboard.put("questions", questions, producer=self.name)
        return [Message(type="artifact_created", payload={"key": "questions"}, source=self.name, trace_id=message.trace_id)]

    def _initialize_templates(self) -> Dict[QuestionCategory, List[str]]:
        return {
            QuestionCategory.INFORMATIONAL: [
                "What is {product_name}?",
                "What concentration does {product_name} contain?",
                "What are the key ingredients in {product_name}?",
                "What skin types is {product_name} suitable for?",
            ],
            QuestionCategory.SAFETY: [
                "Are there any side effects of using {product_name}?",
                "Is {product_name} safe for sensitive skin?",
                "Can {product_name} cause skin irritation?",
                "What precautions should I take when using {product_name}?",
            ],
            QuestionCategory.USAGE: [
                "How do I use {product_name}?",
                "When should I apply {product_name}?",
                "How many drops of {product_name} should I use?",
                "Can I use {product_name} with other skincare products?",
            ],
            QuestionCategory.PURCHASE: [
                "How much does {product_name} cost?",
                "Where can I buy {product_name}?",
                "Is {product_name} worth the price?",
                "What size is {product_name} available in?",
            ],
            QuestionCategory.COMPARISON: [
                "How does {product_name} compare to other vitamin C serums?",
                "Is {product_name} better than other vitamin C serums?",
                "What makes {product_name} different from competitors?",
                "Should I choose {product_name} or other vitamin C serums?",
            ],
        }
