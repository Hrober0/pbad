from collections.abc import Iterator

import anthropic

from .config import LLMConfig
from .tokens import Tokens


class Chat:
    def __init__(self, config: LLMConfig | None = None) -> None:
        self.client = anthropic.Anthropic()
        self.config = config or LLMConfig()
        self.tokens = Tokens(prompt=0, output=0)

    def ask(self, question: str) -> Iterator[str]:
        with self.client.messages.stream(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            output_config={"effort": self.config.effort},
            messages=[{"role": "user", "content": question}],
        ) as stream:
            yield from stream.text_stream
            self.tokens = Tokens.of(stream.get_final_message().usage)
