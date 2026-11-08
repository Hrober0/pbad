from dataclasses import dataclass
from typing import Self

from anthropic.types import Usage


@dataclass(frozen=True)
class Tokens:
    prompt: int
    output: int

    @classmethod
    def of(cls, usage: Usage) -> Self:
        return cls(prompt=usage.input_tokens, output=usage.output_tokens)
