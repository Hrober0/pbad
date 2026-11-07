from dataclasses import dataclass
from typing import Literal

Effort = Literal["low", "medium", "high", "xhigh", "max"]


@dataclass(frozen=True)
class LLMConfig:
    model: str = "claude-sonnet-5-5"
    max_tokens: int = 10000
    effort: Effort = "medium"
