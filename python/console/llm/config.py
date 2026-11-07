from dataclasses import dataclass


@dataclass(frozen=True)
class LLMConfig:
    model: str = "claude-sonnet-5"
    max_tokens: int = 10000
