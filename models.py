from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class QuestionCategory(str, Enum):
    INFORMATIONAL = "informational"
    SAFETY = "safety"
    USAGE = "usage"
    PURCHASE = "purchase"
    COMPARISON = "comparison"


@dataclass
class ProductData:
    name: str
    concentration: str
    skin_types: List[str]
    key_ingredients: List[str]
    benefits: List[str]
    usage_instructions: str
    side_effects: str
    price: str


@dataclass
class Question:
    text: str
    category: QuestionCategory
    answer_template: str = ""


@dataclass
class ContentBlock:
    block_type: str
    content: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Template:
    name: str
    fields: List[str]
    rules: Dict[str, Any]
    format: str
    dependencies: List[str]


@dataclass
class GeneratedPage:
    page_type: str
    title: str
    content: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
