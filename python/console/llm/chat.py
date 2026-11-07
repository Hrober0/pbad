from collections.abc import Iterator

import anthropic

from .config import LLMConfig


class Chat:
    def __init__(self, config: LLMConfig | None = None) -> None:
        self.client = anthropic.Anthropic()
        self.config = config or LLMConfig()

    def ask(self, question: str) -> Iterator[str]:
        with self.client.messages.stream(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            output_config={"effort": self.config.effort},
            messages=[{"role": "user", "content": question}],
        ) as stream:
            yield from stream.text_stream
