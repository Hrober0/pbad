"""Opisowe porównania wariantów (ocena.md). Bez testów statystycznych.

Dla pary wariantów (A, B) podajemy mediany, iloraz median i to, czy zakresy
wartości z powtórzeń się nakładają. Słowny opis zmiany:
    ROŚNIE      mediana B ≥ 1,25 × mediana A
    MALEJE      mediana B ≤ mediana A / 1,25
    BEZ_ZMIANY  pomiędzy
Wszystkie stałe są tu, w jednym miejscu, i odpowiadają ocena.md.
"""

import math
import statistics
from dataclasses import dataclass, field

MIN_UDZIAL_PROB = 0.6   # wariant stabilny: ≥ 60% prób tego samego rodzaju z odczytaną wartością
MIN_ILORAZ = 1.25
MIN_UDZIAL = 2 / 3
SENSITIVITY = (1.5, 2.0)

NUMERIC = {"PROMIEŃ", "K_NAJBLIŻSZYCH", "OBSZAR", "PRÓG", "K_SKRAJNYCH", "ODLEGŁOŚĆ", "LICZBA"}

LETTERS = ("a", "b", "c")
# (A, B): oczekiwany kierunek wartość(B) > wartość(A)
FACTORS: dict[str, list[tuple[str, str]]] = {
    "S: sytuacja pytającego": [
        ("1b", "1c"), ("2b", "2c"), ("3b", "3c"), ("4b", "4c"), ("5b", "5c"),
        ("6b", "6c"), ("7b", "7c"), ("8b", "8d"), ("8d", "8c"),
    ],
    "M: miejsce": [(f"1{x}", f"3{x}") for x in LETTERS]
    + [(f"1{x}", f"5{x}") for x in LETTERS]
    + [(f"2{x}", f"4{x}") for x in LETTERS],
    "O: rodzaj i skala obiektu": [(f"1{x}", f"2{x}") for x in LETTERS]
    + [(f"3{x}", f"4{x}") for x in LETTERS]
    + [(f"6{x}", f"7{x}") for x in LETTERS],
}

DESCRIPTIVE: dict[str, list[tuple[str, str]]] = {
    "„w pobliżu” a „niedaleko”": [("1a", "1d")],
    "sytuacja wywnioskowana (pośpiech)": [("1a", "1e"), ("1b", "1e")],
    "domyślny środek transportu w 15 minut": [("8a", "8b"), ("8a", "8d"), ("8a", "8c")],
    "brak informacji → pieszo": [(f"{n}a", f"{n}b") for n in range(1, 8)],
    "brak informacji → samochodem": [(f"{n}a", f"{n}c") for n in range(1, 8)],
    "„centrum” w różnych miastach": [("9a", "9b"), ("9a", "9c"), ("10a", "10b"), ("9a", "10a"), ("9b", "10b")],
    "próg „duży”: Warszawa → mniejsze miasto": [("11a", "11b"), ("11a", "11c"), ("11b", "11c")],
    "próg „mały”: Warszawa → mniejsze miasto": [("12a", "12b"), ("12a", "12c"), ("12b", "12c")],
    "„mały” → „duży” w tym samym mieście": [("12a", "11a"), ("12b", "11b"), ("12c", "11c")],
    "2f: gradient miejscowości (od Warszawy)": [
        ("1a", "23a"), ("1a", "23b"), ("1a", "5a"), ("1a", "23c"), ("1a", "23d"),
    ],
    "2f: gradient miejscowości (kolejne kroki)": [("23a", "23b"), ("23b", "5a"), ("5a", "23c"), ("23c", "23d")],
    "2f: wieś, samochodem": [("23d", "24"), ("1c", "24")],
    "2f: siła określenia (od „w pobliżu”)": [("1a", "25a"), ("1a", "25b"), ("1a", "25c"), ("1a", "25d")],
    "2f: sytuacja wywnioskowana (od braku informacji)": [("1a", "27a"), ("1a", "27b"), ("1a", "27c"), ("1a", "27d")],
    "2f: sytuacja wywnioskowana (od „pieszo”)": [("1b", "27a"), ("1b", "27b"), ("1b", "27c"), ("1b", "27d")],
    "2f: język pytania": [("1a", "28a"), ("1c", "28b"), ("28a", "28b")],
    "2f: kontrola sformułowania („Dworzec Centralny” → „stacja Warszawa Centralna”)": [("1a", "29a"), ("1c", "29b")],
    "2f: gradient od „stacji Warszawa Centralna”": [("29a", "23a"), ("29a", "23b"), ("29a", "23d"), ("29a", "29b")],
}


@dataclass
class VariantSummary:
    id: str
    n: int
    kinds: dict[str, int]
    dominant: str
    n_dominant: int
    values: list[float] = field(default_factory=list)

    @property
    def stable(self) -> bool:
        return self.dominant in NUMERIC and len(self.values) >= math.ceil(MIN_UDZIAL_PROB * self.n)

    @property
    def median(self) -> float | None:
        return statistics.median(self.values) if self.values else None


def summarize(rows: list[dict], max_rep: int | None = None) -> dict[str, VariantSummary]:
    by_variant: dict[str, list[dict]] = {}
    for row in rows:
        if max_rep is None or row["rep"] <= max_rep:
            by_variant.setdefault(row["variant"], []).append(row)
    out = {}
    for variant, group in by_variant.items():
        kinds: dict[str, int] = {}
        for row in group:
            kinds[row["rodzaj"]] = kinds.get(row["rodzaj"], 0) + 1
        dominant = max(kinds, key=lambda k: (kinds[k], k in NUMERIC))
        values = [float(r["wartosc"]) for r in group if r["rodzaj"] == dominant and r.get("wartosc") is not None]
        out[variant] = VariantSummary(variant, len(group), kinds, dominant, kinds[dominant], values)
    return out


@dataclass
class Comparison:
    a: str
    b: str
    result: str
    ratio: float | None = None
    disjoint: bool | None = None
    note: str = ""


def compare(sa: VariantSummary | None, sb: VariantSummary | None, min_ratio: float = MIN_ILORAZ) -> Comparison:
    if sa is None or sb is None:
        return Comparison(sa.id if sa else "?", sb.id if sb else "?", "BRAK_DANYCH")
    if not sa.stable or not sb.stable:
        which = ", ".join(s.id for s in (sa, sb) if not s.stable)
        return Comparison(sa.id, sb.id, "NIESTABILNY", note=f"niestabilny: {which}")
    if sa.dominant != sb.dominant:
        return Comparison(sa.id, sb.id, "ZMIANA_INTERPRETACJI", note=f"{sa.dominant} → {sb.dominant}")
    ma, mb = sa.median, sb.median
    ratio = mb / ma if ma else math.inf
    disjoint = min(sb.values) > max(sa.values) or max(sb.values) < min(sa.values)
    if ratio >= min_ratio:
        result = "ROŚNIE"
    elif ratio <= 1 / min_ratio:
        result = "MALEJE"
    else:
        result = "BEZ_ZMIANY"
    return Comparison(sa.id, sb.id, result, ratio, disjoint)


@dataclass
class FactorResult:
    name: str
    comparisons: list[Comparison]

    def count(self, result: str) -> int:
        return sum(c.result == result for c in self.comparisons)

    @property
    def resolved(self) -> int:
        return sum(c.result in {"ROŚNIE", "BEZ_ZMIANY", "MALEJE"} for c in self.comparisons)

    @property
    def up(self) -> int:
        return self.count("ROŚNIE")

    @property
    def up_disjoint(self) -> int:
        return sum(c.result == "ROŚNIE" and c.disjoint for c in self.comparisons)

    @property
    def label(self) -> str:
        if self.resolved < math.ceil(len(self.comparisons) / 2):
            return "za mało danych"
        share = self.up / self.resolved
        down = self.count("MALEJE")
        if down > self.up and down / self.resolved >= MIN_UDZIAL:
            return "wpływ przeciwny do oczekiwań"
        if share >= MIN_UDZIAL:
            return "wyraźny wpływ"
        if share >= 1 / 3:
            return "częściowy wpływ"
        return "brak wyraźnego wpływu"


def factors(summaries: dict[str, VariantSummary], min_ratio: float = MIN_ILORAZ) -> list[FactorResult]:
    return [
        FactorResult(name, [compare(summaries.get(a), summaries.get(b), min_ratio) for a, b in pairs])
        for name, pairs in FACTORS.items()
    ]


def descriptive(summaries: dict[str, VariantSummary]) -> dict[str, list[Comparison]]:
    return {
        name: [compare(summaries.get(a), summaries.get(b)) for a, b in pairs]
        for name, pairs in DESCRIPTIVE.items()
        if all(x in summaries for pair in pairs for x in pair)
    }
