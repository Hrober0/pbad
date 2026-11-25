"""Replikacja: niezależna druga seria (domyślnie 2 próby na wariant) w osobnym pliku.

Nie wchodzi do analizy głównej. Służy tylko do sprawdzenia, czy wartości
dominujące z serii głównej powtarzają się w innym uruchomieniu (inny dzień,
inna kolejność wywołań). Wynik: sekcja "Replikacja" w wyniki/tabele.md.
"""

from collections import Counter, defaultdict

from experiment.database import execute

from .analyze import summarize
from .extract import load_extracted, read
from .generate import AnswerStore, Generator, plan
from .paths import REPLICATION_PATH
from .questions import load_variants


def run(reps: int = 2, workers: int = 6):
    store = AnswerStore(REPLICATION_PATH)
    trials = plan(load_variants(), reps, store.done())
    yield from Generator().run(trials, store, workers)


def readings() -> list[dict]:
    rows = []
    for answer in AnswerStore(REPLICATION_PATH).good():
        result = execute(answer["sql"])
        execution = {
            "executed": result.executed,
            "row_count": result.row_count,
            "rows": result.rows[:5],
            "columns": result.columns,
            "error": result.error,
        }
        rows.append(read(answer, execution))
    return rows


def compare_with_main() -> list[dict]:
    main = summarize(load_extracted())
    replica: dict[str, list[dict]] = defaultdict(list)
    for row in readings():
        replica[row["variant"]].append(row)
    out = []
    for variant in load_variants():
        reps = replica.get(variant.id, [])
        if not reps:
            continue
        m = main.get(variant.id)
        values = [(r["rodzaj"], r.get("wartosc")) for r in reps]
        same_kind = sum(kind == m.dominant for kind, _ in values)
        in_range = sum(
            kind == m.dominant and value is not None and m.values and min(m.values) <= value <= max(m.values)
            for kind, value in values
        )
        verdicts = Counter(r.get("ocena_obiektu") for r in reps if r.get("ocena_obiektu"))
        out.append({
            "variant": variant.id,
            "main": f"{m.dominant} {sorted(set(m.values))}",
            "replica": values,
            "same_kind": same_kind,
            "in_range": in_range,
            "n": len(reps),
            "verdicts": dict(verdicts),
        })
    return out
