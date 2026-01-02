from __future__ import annotations

from typing import Any, Dict, List

from ..core import Agent, Blackboard, Message


class PlannerAgent(Agent):
    name = "PlannerAgent"

    def can_handle(self, message: Message, blackboard: Blackboard) -> bool:
        return message.type in {"start", "plan", "artifact_created"}

    def handle(self, message: Message, blackboard: Blackboard) -> List[Message]:
        out: List[Message] = []

        if message.type == "start":
            raw_product_data = message.payload.get("raw_product_data")
            competitor_data = message.payload.get("competitor_data")
            output_dir = message.payload.get("output_dir")

            blackboard.put("raw_product_data", raw_product_data, producer=self.name)
            blackboard.put("competitor_data", competitor_data, producer=self.name)
            blackboard.put("output_dir", output_dir, producer=self.name)

            out.append(Message(type="plan", payload={}, source=self.name, trace_id=message.trace_id))
            return out

        # On any update, re-plan what to do next
        # This is the core "dynamic coordination" behavior.
        if not blackboard.has("product_data") and blackboard.has("raw_product_data"):
            out.append(Message(type="parse_product", payload={}, source=self.name, trace_id=message.trace_id))
            return out

        # Ensure base blocks exist
        for block_type in ["benefits", "usage", "ingredients", "safety"]:
            if not blackboard.has(f"block:{block_type}") and blackboard.has("product_data"):
                out.append(Message(type=f"generate_block:{block_type}", payload={}, source=self.name, trace_id=message.trace_id))
                return out

        # Comparison block depends on competitor data; if none provided, planner requests a fictional competitor
        if not blackboard.has("competitor_product"):
            if blackboard.get("competitor_data"):
                blackboard.put("competitor_product", blackboard.get("competitor_data"), producer=self.name)
            else:
                blackboard.put(
                    "competitor_product",
                    {
                        "name": "CitraGlow Serum B",
                        "concentration": "15% Vitamin C",
                        "skin_types": ["Normal", "Dry"],
                        "key_ingredients": ["Vitamin C", "Niacinamide"],
                        "benefits": ["Brightening", "Evens skin tone"],
                        "price": "₹899",
                        "fictional": True,
                    },
                    producer=self.name,
                )

        if not blackboard.has("block:comparison") and blackboard.has("product_data"):
            out.append(Message(type="generate_block:comparison", payload={}, source=self.name, trace_id=message.trace_id))
            return out

        # Ensure questions exist
        if not blackboard.has("questions") and blackboard.has("product_data"):
            out.append(Message(type="generate_questions", payload={}, source=self.name, trace_id=message.trace_id))
            return out

        # Render pages based on goals (schemas preserved)
        # Each render will produce a page content dict stored under the output filename key.
        if "faq.json" in blackboard.goals and not blackboard.has("faq.json"):
            out.append(Message(type="render_page:faq", payload={}, source=self.name, trace_id=message.trace_id))
            return out

        if "product_page.json" in blackboard.goals and not blackboard.has("product_page.json"):
            out.append(Message(type="render_page:product", payload={}, source=self.name, trace_id=message.trace_id))
            return out

        if "comparison_page.json" in blackboard.goals and not blackboard.has("comparison_page.json"):
            out.append(Message(type="render_page:comparison", payload={}, source=self.name, trace_id=message.trace_id))
            return out

        if "graph.json" in blackboard.goals and not blackboard.has("graph.json"):
            out.append(Message(type="build_graph", payload={}, source=self.name, trace_id=message.trace_id))
            return out

        return out
