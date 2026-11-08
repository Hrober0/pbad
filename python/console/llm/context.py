from enum import StrEnum
from functools import cache
from pathlib import Path
from typing import Self

CONTEXTS_DIR = (
    Path(__file__).resolve().parents[3]
    / "eksperyment"
    / "selected"
    / "H1"
    / "konteksty"
)


class ContextLevel(StrEnum):
    K0 = "K0"
    K1 = "K1"
    K2 = "K2"
    K3 = "K3"

    @property
    def path(self) -> Path:
        return CONTEXTS_DIR / self.value / "kontekst.txt"

    @property
    def next(self) -> Self:
        levels = list(ContextLevel)
        return levels[(levels.index(self) + 1) % len(levels)]

    def load(self) -> str:
        return load_context(self)


@cache
def load_context(level: ContextLevel) -> str:
    return level.path.read_text(encoding="utf-8").strip()
