import json
from pathlib import Path

from .agents import (
    BenefitsAgent,
    ComparisonAgent,
    GraphAgent,
    IngredientsAgent,
    PageRenderAgent,
    ParserAgent,
    PlannerAgent,
    QuestionAgent,
    SafetyAgent,
    UsageAgent,
)
from .core import AgentRegistry, EventLoopOrchestrator, Message


def main() -> None:
    product_data = {
        "Product Name": "GlowBoost Vitamin C Serum",
        "Concentration": "10% Vitamin C",
        "Skin Type": "Oily, Combination",
        "Key Ingredients": "Vitamin C, Hyaluronic Acid",
        "Benefits": "Brightening, Fades dark spots",
        "How to Use": "Apply 2–3 drops in the morning before sunscreen",
        "Side Effects": "Mild tingling for sensitive skin",
        "Price": "₹699",
    }

    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    registry = AgentRegistry()
    registry.register(PlannerAgent())
    registry.register(ParserAgent())
    registry.register(BenefitsAgent())
    registry.register(UsageAgent())
    registry.register(IngredientsAgent())
    registry.register(SafetyAgent())
    registry.register(ComparisonAgent())
    registry.register(QuestionAgent())
    registry.register(PageRenderAgent())
    registry.register(GraphAgent())

    orchestrator = EventLoopOrchestrator(registry)

    goals = ["faq.json", "product_page.json", "comparison_page.json", "graph.json"]
    initial_messages = [
        Message(
            type="start",
            payload={"raw_product_data": product_data, "competitor_data": None, "output_dir": str(output_dir)},
            source="User",
            trace_id="run-1",
        )
    ]

    bb = orchestrator.run(initial_messages=initial_messages, goals=goals)

    # Show message flow
    print("\n=== MESSAGE FLOW ===")
    for i, event in enumerate(bb.event_log, 1):
        if event.get("event") == "message":
            print(f"{i:2d}. {event['type']} from {event.get('source', 'Unknown')}")
        elif event.get("event") == "artifact_created":
            print(f"    → Artifact created: {event['key']} by {event['producer']}")
        elif event.get("event") == "unhandled":
            print(f"    ⚠ Unhandled message: {event['type']}")

    print(f"\nTotal messages processed: {len([e for e in bb.event_log if e.get('event') == 'message'])}")
    print(f"Total artifacts created: {len([e for e in bb.event_log if e.get('event') == 'artifact_created'])}")

    # Persist artifacts (schemas must match exactly)
    for filename in ["faq.json", "product_page.json", "comparison_page.json", "graph.json"]:
        content = bb.get(filename)
        (output_dir / filename).write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✓ Created {filename}")


if __name__ == "__main__":
    main()
