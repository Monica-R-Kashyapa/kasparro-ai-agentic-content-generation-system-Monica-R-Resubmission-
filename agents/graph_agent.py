from __future__ import annotations

from typing import Any, Dict, List

from ..core import Agent, Blackboard, Message


class GraphAgent(Agent):
    name = "GraphAgent"

    def can_handle(self, message: Message, blackboard: Blackboard) -> bool:
        return message.type == "build_graph" and not blackboard.has("graph.json")

    def handle(self, message: Message, blackboard: Blackboard) -> List[Message]:
        # A lightweight dynamic graph derived from message flow.
        nodes: Dict[str, Dict[str, Any]] = {}
        edges: List[Dict[str, Any]] = []

        last_by_source: Dict[str, str] = {}
        for entry in blackboard.event_log:
            if entry.get("event") != "message":
                continue
            mtype = entry.get("type")
            source = entry.get("source")

            node_id = f"{source}:{mtype}"
            if node_id not in nodes:
                nodes[node_id] = {"id": node_id, "agent": source, "message_type": mtype}

            prev = last_by_source.get(source)
            if prev and prev != node_id:
                edges.append({"from": prev, "to": node_id})
            last_by_source[source] = node_id

        graph = {"nodes": list(nodes.values()), "edges": edges}
        blackboard.put("graph.json", graph, producer=self.name)
        return [Message(type="artifact_created", payload={"key": "graph.json"}, source=self.name, trace_id=message.trace_id)]
