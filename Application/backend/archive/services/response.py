from dataclasses import dataclass
from typing import Any


@dataclass
class ChatResponse:
    success: bool
    answer: str
    tool: str | None = None
    command: str | None = None
    raw_output: str | None = None
    execution_time: float | None = None
    metadata: dict[str, Any] | None = None