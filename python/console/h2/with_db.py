"""Sprawdzenie dodatkowe: te same pytania, ale model może wykonywać zapytania na bazie.

Różnica wobec serii głównej (generate.py) jest jedna: model dostaje narzędzie
run_sql (SELECT rolą tylko do odczytu) i może sprawdzić dane, zanim poda
końcową odpowiedź {"sql", "uwagi"}. Instrukcja, kontekst K2, model i effort
są te same; do instrukcji dochodzi tylko akapit o narzędziu (DB_ACCESS_NOTE).

Dla każdej próby zapisujemy (wyniki/z_baza.jsonl):
    kroki          każde zapytanie wykonane narzędziem: SQL, liczba wierszy, błąd
    sql, uwagi     końcowa odpowiedź, odczytywana tym samym extract.read co seria główna
    tokeny         suma po wszystkich krokach, z podziałem na cache
Dzięki temu da się porównać:
    - pierwszą przyjętą wartość (pierwsze zapytanie z promieniem lub progiem)
      z serią główną: czy dostęp do danych zmienia samą interpretację,
    - wartość końcową: czy model ją poprawia po obejrzeniu danych,
    - wynik końcowy (puste wyniki, ocena obiektu) i koszt w tokenach.
"""

import json
import time
from collections import Counter, defaultdict
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from statistics import mean

import anthropic

from experiment.database import QueryResult, execute
from llm.config import LLMConfig

from .extract import load_extracted, read
from .generate import H2_SCHEMA, RETRY_DELAYS, AnswerStore, _now, _retryable, _since, system_prompt
from .paths import DB_ANSWERS_PATH, DB_REPORT_PATH
from .questions import Variant

MAX_STEPS = 8          # tyle odpowiedzi modelu na próbę; w ostatniej narzędzie jest wyłączone
TOOL_ROWS = 20         # tyle wierszy wyniku widzi model
TOOL_CELL_CHARS = 200  # dłuższe wartości (np. geometrie) są ucinane
VALUE_KINDS = {"PROMIEŃ", "PRÓG", "K_NAJBLIŻSZYCH", "OBSZAR"}

DB_ACCESS_NOTE = """Masz dostęp do opisanej wyżej bazy przez narzędzie run_sql. Możesz nim wykonywać zapytania SELECT i oglądać ich wyniki, zanim podasz odpowiedź. Odpowiedzią końcową jest jedno zapytanie SELECT w polu sql, tak jak bez narzędzia."""

RUN_SQL_TOOL = {
    "name": "run_sql",
    "description": (
        "Wykonuje jedno zapytanie SELECT na bazie (tylko odczyt) i zwraca nazwy kolumn, "
        f"liczbę wierszy oraz najwyżej {TOOL_ROWS} pierwszych wierszy."
    ),
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {"sql": {"type": "string", "description": "Zapytanie SELECT."}},
        "required": ["sql"],
        "additionalProperties": False,
    },
}


@dataclass(frozen=True)
class DbAnswer:
    ts: str
    variant: str
    part: str
    rep: int
    question: str
    model: str
    effort: str
    latency_s: float
    steps: list[dict] = field(default_factory=list)
    responses: int = 0
    step_limit_hit: bool = False
    input_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    output_tokens: int = 0
    sql: str = ""
    uwagi: str = ""
    raw: str = ""
    error: str = ""


def tool_output(result: QueryResult) -> str:
    if result.error:
        return json.dumps({"blad": result.error[:500]}, ensure_ascii=False)
    rows = [
        [cell[:TOOL_CELL_CHARS] if isinstance(cell, str) else cell for cell in row]
        for row in result.rows[:TOOL_ROWS]
    ]
    return json.dumps(
        {"kolumny": result.columns, "liczba_wierszy": result.row_count, "wiersze": rows},
        ensure_ascii=False,
        default=str,
    )


class DbGenerator:
    def __init__(self, config: LLMConfig | None = None) -> None:
        self.client = anthropic.Anthropic()
        self.config = config or LLMConfig()
        # Stała część promptu jest cache'owana: przy kilku krokach na próbę oszczędza to
        # większość kosztu wejścia (K2 ma ok. 9 tys. tokenów).
        self.system = [{
            "type": "text",
            "text": f"{system_prompt()}\n\n{DB_ACCESS_NOTE}",
            "cache_control": {"type": "ephemeral"},
        }]

    def _create(self, messages: list[dict], last: bool):
        for attempt, delay in enumerate(RETRY_DELAYS):
            try:
                return self.client.messages.create(
                    model=self.config.model,
                    max_tokens=self.config.max_tokens,
                    output_config={
                        "effort": self.config.effort,
                        "format": {"type": "json_schema", "schema": H2_SCHEMA},
                    },
                    system=self.system,
                    tools=[RUN_SQL_TOOL],
                    tool_choice={"type": "none"} if last else {"type": "auto"},
                    messages=messages,
                )
            except anthropic.APIError as error:
                if not _retryable(error) or attempt == len(RETRY_DELAYS) - 1:
                    raise
                time.sleep(delay)
        raise AssertionError("unreachable")

    def ask(self, variant: Variant, rep: int) -> DbAnswer:
        started = time.perf_counter()
        common = {
            "variant": variant.id, "part": variant.part, "rep": rep, "question": variant.text,
            "model": self.config.model, "effort": self.config.effort,
        }
        messages: list[dict] = [{"role": "user", "content": f"Pytanie: {variant.text}"}]
        steps: list[dict] = []
        usage = Counter()
        response = None
        responses = 0
        try:
            for index in range(MAX_STEPS):
                last = index == MAX_STEPS - 1
                response = self._create(messages, last)
                responses += 1
                u = response.usage
                usage["input"] += u.input_tokens
                usage["cache_read"] += u.cache_read_input_tokens or 0
                usage["cache_write"] += u.cache_creation_input_tokens or 0
                usage["output"] += u.output_tokens
                if response.stop_reason != "tool_use":
                    break
                messages.append({"role": "assistant", "content": response.content})
                results = []
                for block in response.content:
                    if block.type != "tool_use":
                        continue
                    sql = block.input.get("sql", "")
                    result = execute(sql)
                    steps.append({
                        "krok": index + 1, "sql": sql, "wiersze": result.row_count,
                        "blad": result.error[:300], "czas_s": result.duration_s,
                    })
                    results.append({
                        "type": "tool_result", "tool_use_id": block.id,
                        "content": tool_output(result), "is_error": bool(result.error),
                    })
                messages.append({"role": "user", "content": results})
        except anthropic.APIError as error:
            return DbAnswer(**common, ts=_now(), latency_s=_since(started), steps=steps,
                            responses=responses, error=f"{type(error).__name__}: {error}")

        tokens = {
            "input_tokens": usage["input"], "cache_read_tokens": usage["cache_read"],
            "cache_write_tokens": usage["cache_write"], "output_tokens": usage["output"],
        }
        hit = response is not None and response.stop_reason == "tool_use"
        raw = next((b.text for b in response.content if b.type == "text"), "") if response else ""
        if response is not None and response.stop_reason == "refusal":
            return DbAnswer(**common, **tokens, ts=_now(), latency_s=_since(started), steps=steps,
                            responses=responses, raw=raw, error="refusal")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as error:
            return DbAnswer(**common, **tokens, ts=_now(), latency_s=_since(started), steps=steps,
                            responses=responses, step_limit_hit=hit, raw=raw,
                            error=f"JSONDecodeError: {error}")
        return DbAnswer(
            **common, **tokens, ts=_now(), latency_s=_since(started), steps=steps,
            responses=responses, step_limit_hit=hit,
            sql=parsed.get("sql", ""), uwagi=parsed.get("uwagi", ""), raw=raw,
        )

    def run(self, trials: list[tuple[Variant, int]], store: AnswerStore, workers: int) -> Iterator[DbAnswer]:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            for answer in pool.map(lambda trial: self.ask(*trial), trials):
                store.append(answer)
                yield answer


def store() -> AnswerStore:
    return AnswerStore(DB_ANSWERS_PATH)


# ------------------------------------------------------------------ odczyt


def _execution(result: QueryResult) -> dict:
    return {**asdict(result), "executed": result.executed}


def first_value(answer: dict, kind: str | None) -> dict | None:
    """Pierwsza wartość tego samego rodzaju co w serii głównej (np. promień) w zapytaniach narzędzia.

    Zapytania rozpoznawcze innego rodzaju (np. "10 najbliższych aptek z odległościami")
    nie są interpretacją, tylko oglądaniem danych; liczymy je w polu "przed".
    """
    kinds = {kind} if kind else VALUE_KINDS
    for position, step in enumerate(answer.get("steps", [])):
        reading = read({**answer, "sql": step["sql"], "uwagi": ""}, None)
        if reading["rodzaj"] in kinds and reading.get("wartosc") is not None:
            return {"krok": step["krok"], "przed": position, "rodzaj": reading["rodzaj"], "wartosc": reading["wartosc"]}
    return None


def main_kinds() -> dict[str, str]:
    """Dominujący rodzaj wartości w serii głównej dla każdego wariantu."""
    kinds = defaultdict(Counter)
    for row in load_extracted():
        if row["rodzaj"] in VALUE_KINDS:
            kinds[row["variant"]][row["rodzaj"]] += 1
    return {variant: counter.most_common(1)[0][0] for variant, counter in kinds.items()}


def read_all() -> list[dict]:
    rows = []
    kinds = main_kinds()
    for answer in store().good():
        execution = _execution(execute(answer["sql"])) if answer["sql"].strip() else None
        final = read(answer, execution)
        first = first_value(answer, kinds.get(answer["variant"])) if answer["part"] not in {"2e", "2g", "2h"} else None
        rows.append({
            "variant": answer["variant"], "part": answer["part"], "rep": answer["rep"],
            "kroki": len(answer["steps"]), "limit": answer["step_limit_hit"],
            "pierwsza": first, "koncowa": final,
            "tokeny_we": answer["input_tokens"] + answer["cache_read_tokens"] + answer["cache_write_tokens"],
            "tokeny_cache": answer["cache_read_tokens"], "tokeny_wy": answer["output_tokens"],
        })
    return rows


# ------------------------------------------------------------------ raport


def _dist(values: list) -> str:
    counts = Counter(values)
    return ", ".join(f"{_fmt(v)} ×{n}" for v, n in counts.most_common()) or "–"


def _fmt(value) -> str:
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return f"{value:,}".replace(",", " ") if isinstance(value, (int, float)) else str(value)


def _outcome(reading: dict) -> str:
    if "ocena_obiektu" in reading:
        return reading["ocena_obiektu"]
    if reading["rodzaj"] in {"BRAK_SQL", "BŁĄD_WYKONANIA"}:
        return reading["rodzaj"].lower()
    if reading["rodzaj"] == "PUSTY_WYNIK":
        return "pusty"
    if reading.get("wykonane") and reading.get("wiersze") == 0:
        return "pusty"
    return reading.get("wartosc") if reading.get("wartosc") is not None else reading["rodzaj"]


def report(rows: list[dict] | None = None) -> str:
    rows = read_all() if rows is None else rows
    main = defaultdict(list)
    for row in load_extracted():
        main[row["variant"]].append(row)
    by_variant = defaultdict(list)
    for row in rows:
        by_variant[row["variant"]].append(row)

    out = [
        "# Sprawdzenie dodatkowe: odpowiedzi z dostępem do bazy\n",
        "Plik generuje `python run_h2.py zbaza-raport`. Model, effort i kontekst K2 jak w serii głównej; "
        "do instrukcji dochodzi akapit o narzędziu `run_sql` (h2/with_db.py).\n",
        "**Pierwsza wartość** to promień, próg albo `LIMIT` z pierwszego zapytania narzędzia, które go zawiera "
        "(interpretacja przed obejrzeniem danych). Może to być też zapytanie rozpoznawcze, np. liczenie aptek w 5 km, "
        "więc przed opisem warto obejrzeć kroki (`python run_h2.py zbaza-show <wariant>`). "
        "**Końcowa** to odczyt z końcowego SQL, tym samym skryptem co seria główna; „pusty” oznacza 0 wierszy.\n",
        "| # | Prób | Seria główna (bez bazy) | Z bazą: pierwsza wartość | Zapytań przed nią | Z bazą: końcowa | Kroki (średnio) | Tokeny wej. / wyj. (średnio) |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for vid in sorted(by_variant, key=lambda v: (int("".join(c for c in v if c.isdigit())), v)):
        group = by_variant[vid]
        base = _dist([_outcome(r) for r in main.get(vid, [])])
        first = _dist([r["pierwsza"]["wartosc"] if r["pierwsza"] else "brak" for r in group]) \
            if group[0]["part"] not in {"2e", "2g", "2h"} else "–"
        final = _dist([_outcome(r["koncowa"]) for r in group])
        before = [r["pierwsza"]["przed"] for r in group if r["pierwsza"]]
        before_text = f"{mean(before):.1f}" if before else "–"
        out.append(
            f"| {vid} | {len(group)} | {base} | {first} | {before_text} | {final} | {mean(r['kroki'] for r in group):.1f} | "
            f"{_fmt(round(mean(r['tokeny_we'] for r in group)))} / {_fmt(round(mean(r['tokeny_wy'] for r in group)))} |"
        )
    if rows:
        total_in = sum(r["tokeny_we"] for r in rows)
        total_cache = sum(r["tokeny_cache"] for r in rows)
        out.append(
            f"\nRazem {len(rows)} prób, tokeny wejściowe {_fmt(total_in)} (w tym z cache {_fmt(total_cache)}), "
            f"wyjściowe {_fmt(sum(r['tokeny_wy'] for r in rows))}. "
            f"Próby, które doszły do limitu {MAX_STEPS} odpowiedzi: {sum(r['limit'] for r in rows)}.\n"
        )
    text = "\n".join(out) + "\n"
    DB_REPORT_PATH.write_text(text, encoding="utf-8")
    return text
