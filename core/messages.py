from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Message:
    type: str
    payload: Dict[str, Any] = field(default_factory=dict)
    source: str = "system"
    trace_id: Optional[str] = None
