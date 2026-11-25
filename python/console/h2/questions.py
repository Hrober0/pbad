"""Wczytuje warianty z pytania.md.

Bierze każdą tabelę markdown, której nagłówek ma kolumny "#" i "Pytanie",
a pierwsza komórka wiersza wygląda jak kod wariantu (1a, 13b, 18). Część
(2a–2h) to ostatni nagłówek "## Część 2x" nad tabelą.
"""

import re
from dataclasses import dataclass
from pathlib import Path

from .paths import QUESTIONS_PATH

CODE = re.compile(r"^\d{1,2}[a-z]?$")
PART = re.compile(r"^## Część (2[a-z])")


@dataclass(frozen=True)
class Variant:
    id: str
    part: str
    text: str

    @property
    def number(self) -> int:
        return int(re.match(r"\d+", self.id)[0])


def load_variants(path: Path = QUESTIONS_PATH) -> list[Variant]:
    variants: list[Variant] = []
    part = ""
    header: list[str] | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if match := PART.match(line):
            part = match[1]
            header = None
            continue
        if not line.startswith("|"):
            header = None
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        if "#" not in header or "Pytanie" not in header:
            continue
        code = cells[header.index("#")]
        if CODE.match(code) and part:
            variants.append(Variant(code, part, cells[header.index("Pytanie")]))

    ids = [variant.id for variant in variants]
    duplicates = {code for code in ids if ids.count(code) > 1}
    if duplicates:
        raise ValueError(f"Powtórzone kody wariantów w {path}: {sorted(duplicates)}")
    return variants
