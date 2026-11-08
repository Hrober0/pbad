import json
from dataclasses import dataclass

import anthropic

from .config import LLMConfig
from .context import ContextLevel
from .prompt import RESPONSE_SCHEMA, build_system
from .tokens import Tokens


@dataclass(frozen=True)
class SqlAnswer:
    raw: str
    level: ContextLevel
    tokens: Tokens

    @property
    def sql(self) -> str:
        return json.loads(self.raw)["sql"]

    @property
    def pretty(self) -> str:
        return json.dumps(json.loads(self.raw), indent=2, ensure_ascii=False)


class SqlGenerator:
    def __init__(self, config: LLMConfig | None = None) -> None:
        self.client = anthropic.Anthropic()
        self.config = config or LLMConfig()

    def generate(self, question: str, level: ContextLevel) -> SqlAnswer:
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            output_config={
                "effort": self.config.effort,
                "format": {"type": "json_schema", "schema": RESPONSE_SCHEMA},
            },
            system=build_system(level.load()),
            messages=[{"role": "user", "content": f"Pytanie: {question}"}],
        )
        return SqlAnswer(
            raw=next(b.text for b in response.content if b.type == "text"),
            level=level,
            tokens=Tokens.of(response.usage),
        )
