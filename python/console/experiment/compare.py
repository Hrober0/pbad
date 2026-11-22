"""Porównanie wyników zapytań modelu z wzorcami według zasad z metody:
kolumny kluczowe, wiersze jako zbiory (kolejność tylko w „najbliższych"
i „top k"), liczby z tolerancją 1% (liczności dokładnie), napisy dokładnie.
Odpowiedź jest poprawna, gdy zgadza się z wzorcem albo z którymkolwiek
wariantem dopuszczalnym `<kod>.v<n>.sql`."""

import json
import os
import re
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path

from .database import QueryResult, execute
from .executor import EXECUTIONS_PATH
from .store import RESULTS_PATH

PATTERNS_DIR = RESULTS_PATH.parents[1] / "wzorce"
EVALUATION_PATH = RESULTS_PATH.with_name("ocena.jsonl")
ADMIN_DSN = os.getenv("PBAD_ADMIN_DSN", "postgresql://pbad:pbad@localhost:5432/pbad")

ID_COLUMNS = {"osm_id", "fid", "code", "id", "gid", "geom", "geometry"}
TOLERANCE = 0.01


@dataclass(frozen=True)
class Rule:
    kind: str
    k: int = 0
    exact: bool = False


RULES: dict[str, Rule] = {
    "Z01": Rule("number", exact=True),
    "Z02": Rule("names"),
    "Z05": Rule("number", exact=True),
    "Z07": Rule("number", exact=True),
    "N01": Rule("first_name"),
    "N03": Rule("name_number"),
    "N04": Rule("ordered_names", k=5),
    "N07": Rule("ordered_name_number", k=3),
    "J01": Rule("names"),
    "J02": Rule("number", exact=True),
    "J05": Rule("names"),
    "J08": Rule("names"),
    "A01": Rule("numbers", exact=True),
    "A03": Rule("top_k", k=5),
    "A07": Rule("numbers", exact=True),
    "A08": Rule("numbers", exact=True),
    "M02": Rule("number"),
    "M03": Rule("number"),
    "M05": Rule("number"),
    "M07": Rule("number"),
}


@dataclass(frozen=True)
class Evaluation:
    question_id: str
    level: str
    rep: int
    executed: bool
    correct: bool
    matched: str
    reason: str


class Patterns:
    """Wyniki wzorców i wariantów, liczone raz na przebieg."""

    def __init__(self, directory: Path = PATTERNS_DIR) -> None:
        self._directory = directory
        self._cache: dict[str, list[tuple[str, QueryResult]]] = {}

    def for_question(self, question_id: str) -> list[tuple[str, QueryResult]]:
        if question_id not in self._cache:
            files = [self._directory / f"{question_id}.sql"] + sorted(
                self._directory.glob(f"{question_id}.v*.sql")
            )
            results = []
            for path in files:
                result = execute(path.read_text(encoding="utf-8"), dsn=ADMIN_DSN)
                if not result.executed:
                    raise RuntimeError(f"Wzorzec {path.name} nie działa: {result.error}")
                label = "wzorzec" if path.stem == question_id else path.stem.split(".")[1]
                results.append((label, result))
            self._cache[question_id] = results
        return self._cache[question_id]


def evaluate_all(
    patterns: Patterns | None = None,
    executions: Path = EXECUTIONS_PATH,
    out: Path = EVALUATION_PATH,
) -> list[Evaluation]:
    patterns = patterns or Patterns()
    rows = [
        json.loads(line)
        for line in executions.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    evaluations = [
        evaluate(row, patterns) for row in rows if row["question_id"] in RULES
    ]
    out.write_text(
        "".join(json.dumps(asdict(e), ensure_ascii=False) + "\n" for e in evaluations),
        encoding="utf-8",
    )
    return evaluations


def evaluate(row: dict, patterns: Patterns) -> Evaluation:
    base = {"question_id": row["question_id"], "level": row["level"], "rep": row["rep"]}
    if not row["executed"]:
        return Evaluation(**base, executed=False, correct=False, matched="", reason="nie wykonuje się")
    if not row["rows"]:
        return Evaluation(**base, executed=True, correct=False, matched="", reason="pusty wynik")

    model = QueryResult(columns=row["columns"], rows=row["rows"], row_count=row["row_count"])
    rule = RULES[row["question_id"]]
    check = CHECKS[rule.kind]
    for label, pattern in patterns.for_question(row["question_id"]):
        if check(model, pattern, rule):
            return Evaluation(**base, executed=True, correct=True, matched=label, reason="")
    return Evaluation(**base, executed=True, correct=False, matched="", reason="inny wynik")


# --- wyciąganie wartości z wiersza ---------------------------------------


def _key_columns(result: QueryResult) -> list[int]:
    return [
        index
        for index, column in enumerate(result.columns)
        if column.lower() not in ID_COLUMNS
        and not column.lower().endswith("_id")
        and "geom" not in column.lower()
    ]


def _number(value: object) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str) and re.fullmatch(r"-?\d+(\.\d+)?", value.strip()):
        return float(value)
    return None


def _texts(result: QueryResult, row: list) -> list[str]:
    return [
        "" if row[i] is None else row[i]
        for i in _key_columns(result)
        if (isinstance(row[i], str) or row[i] is None) and _number(row[i]) is None
    ]


def _numbers(result: QueryResult, row: list) -> list[float]:
    return [n for i in _key_columns(result) if (n := _number(row[i])) is not None]


def _first_text(result: QueryResult, row: list) -> str | None:
    """Tekst z kolumny nazwy, jeśli model ją tak nazwał, inaczej z pierwszej tekstowej."""
    columns = _key_columns(result)
    preferred = [
        i for i in columns
        if any(word in result.columns[i].lower() for word in ("name", "nazw"))
    ]
    for i in preferred + columns:
        value = row[i]
        if (isinstance(value, str) or value is None) and _number(value) is None:
            return "" if value is None else value
    return None


def _close(a: float, b: float, exact: bool) -> bool:
    if exact:
        return round(a) == round(b) and abs(a - round(a)) < 1e-9
    return abs(a - b) <= TOLERANCE * abs(b) if b else abs(a) < 1e-9


# --- reguły porównania ------------------------------------------------------


def _number_rule(model: QueryResult, pattern: QueryResult, rule: Rule) -> bool:
    expected = _numbers(pattern, pattern.rows[0])[0]
    if len(model.rows) != 1:
        return False
    return any(_close(n, expected, rule.exact) for n in _numbers(model, model.rows[0]))


def _names_rule(model: QueryResult, pattern: QueryResult, rule: Rule) -> bool:
    expected = {_first_text(pattern, row) for row in pattern.rows}
    got = {_first_text(model, row) for row in model.rows}
    return None not in got and got == expected


def _first_name_rule(model: QueryResult, pattern: QueryResult, rule: Rule) -> bool:
    return _first_text(model, model.rows[0]) == _first_text(pattern, pattern.rows[0])


def _name_number_rule(model: QueryResult, pattern: QueryResult, rule: Rule) -> bool:
    expected_name = _first_text(pattern, pattern.rows[0])
    expected_number = _numbers(pattern, pattern.rows[0])[0]
    row = model.rows[0]
    return _first_text(model, row) == expected_name and any(
        _close(n, expected_number, False) for n in _numbers(model, row)
    )


def _ordered_names_rule(model: QueryResult, pattern: QueryResult, rule: Rule) -> bool:
    if len(model.rows) != rule.k:
        return False
    return [_first_text(model, r) for r in model.rows] == [
        _first_text(pattern, r) for r in pattern.rows[: rule.k]
    ]


def _ordered_name_number_rule(model: QueryResult, pattern: QueryResult, rule: Rule) -> bool:
    if not _ordered_names_rule(model, pattern, rule):
        return False
    return all(
        any(_close(n, _numbers(pattern, p)[0], False) for n in _numbers(model, m))
        for m, p in zip(model.rows, pattern.rows)
    )


def _numbers_rule(model: QueryResult, pattern: QueryResult, rule: Rule) -> bool:
    expected = sorted(n for row in pattern.rows for n in _numbers(pattern, row))
    got = sorted(n for row in model.rows for n in _numbers(model, row))
    return len(got) == len(expected) and all(
        _close(g, e, rule.exact) for g, e in zip(got, expected)
    )


def _top_k_rule(model: QueryResult, pattern: QueryResult, rule: Rule) -> bool:
    """Remis na granicy k: dowolny wybór spośród obiektów o wartości granicznej."""
    if len(model.rows) != rule.k:
        return False
    expected = {_first_text(pattern, r): _numbers(pattern, r)[0] for r in pattern.rows}
    top = sorted(expected.values(), reverse=True)[: rule.k]
    got = [(_first_text(model, r), _numbers(model, r)) for r in model.rows]
    if any(name not in expected for name, _ in got) or len({n for n, _ in got}) != rule.k:
        return False
    values = [expected[name] for name, _ in got]
    counts_ok = all(any(_close(n, expected[name], True) for n in nums) for name, nums in got)
    return counts_ok and values == sorted(values, reverse=True) and sorted(values, reverse=True) == top


CHECKS: dict[str, Callable[[QueryResult, QueryResult, Rule], bool]] = {
    "number": _number_rule,
    "names": _names_rule,
    "first_name": _first_name_rule,
    "name_number": _name_number_rule,
    "ordered_names": _ordered_names_rule,
    "ordered_name_number": _ordered_name_number_rule,
    "numbers": _numbers_rule,
    "top_k": _top_k_rule,
}
