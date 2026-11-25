"""Wywołania modelu dla eksperymentu 2.

Instrukcja jest ta sama co w eksperymencie 1 (llm/prompt.py), zmienia się tylko
format odpowiedzi: pole "uwagi" zamiast "explanation". Opis pola jest neutralny
i nie wspomina o niejasnościach ani założeniach, żeby nie podpowiadać modelowi,
że ma je zgłaszać (plan-eksperymentow.md, "Co dokładnie dostaje model").
Kontekst bazy: zawsze K2.
"""

import json
import time
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

import anthropic

from llm import ContextLevel
from llm.config import LLMConfig
from llm.prompt import INSTRUCTION
from llm.tokens import Tokens

from .paths import ANSWERS_PATH
from .questions import Variant

LEVEL = ContextLevel.K2
RETRY_DELAYS = (5, 20, 60, 120)

H2_INSTRUCTION = INSTRUCTION.replace("w polu explanation", "w polu uwagi")

H2_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "sql": {
            "type": "string",
            "description": "Samo zapytanie SELECT, bez markdown i bez komentarzy.",
        },
        "uwagi": {
            "type": "string",
            "description": "Uwagi do zapytania. Może pozostać pustym ciągiem.",
        },
    },
    "required": ["sql", "uwagi"],
    "additionalProperties": False,
}


# Część 2g (próba naprawy): K2 + jedna ogólna wskazówka o szukaniu obiektów po nazwie.
# Wskazówka nie wymienia żadnego obiektu z pytań. Dokładnie ten tekst jest w pytania.md.
NAME_SEARCH_HINT = """Wskazówka do wyszukiwania obiektów po nazwie: nie zakładaj z góry, w której tabeli i z jakim fclass zapisano dany obiekt. Szukaj go jednocześnie w tabelach punktowych i poligonowych (UNION ALL), bez warunku na fclass. W warunku na nazwę używaj rdzenia nazwy (np. ILIKE '%rdzeń%'), bo nazwy w bazie są zwykle w mianowniku i mogą się różnić od formy użytej w pytaniu. Jeśli nazwie odpowiada kilka obiektów, wybierz jeden konkretny obiekt, który najlepiej pasuje do pytania, i opisz wybór w polu uwagi."""

HINT_PARTS = {"2g"}


def system_prompt(part: str = "") -> str:
    context = LEVEL.load()
    if part in HINT_PARTS:
        context = f"{context}\n\n{NAME_SEARCH_HINT}"
    return H2_INSTRUCTION.format(context=context)


@dataclass(frozen=True)
class Answer:
    ts: str
    variant: str
    part: str
    rep: int
    question: str
    model: str
    effort: str
    latency_s: float
    input_tokens: int = 0
    output_tokens: int = 0
    sql: str = ""
    uwagi: str = ""
    raw: str = ""
    error: str = ""

    @property
    def key(self) -> tuple[str, int]:
        return (self.variant, self.rep)


class AnswerStore:
    def __init__(self, path: Path = ANSWERS_PATH) -> None:
        self.path = path
        self._lock = Lock()

    def append(self, answer: Answer) -> None:
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as file:
                file.write(json.dumps(asdict(answer), ensure_ascii=False) + "\n")

    def rows(self) -> list[dict]:
        if not self.path.exists():
            return []
        return [
            json.loads(line)
            for line in self.path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def good(self) -> list[dict]:
        """Udane odpowiedzi, po jednej na (wariant, powtórzenie) — ostatnia wygrywa."""
        latest: dict[tuple[str, int], dict] = {}
        for row in self.rows():
            if not row.get("error"):
                latest[(row["variant"], row["rep"])] = row
        return list(latest.values())

    def done(self) -> set[tuple[str, int]]:
        return {(row["variant"], row["rep"]) for row in self.good()}


class Generator:
    def __init__(self, config: LLMConfig | None = None) -> None:
        self.client = anthropic.Anthropic()
        self.config = config or LLMConfig()
        self.systems = {"": system_prompt(), **{part: system_prompt(part) for part in HINT_PARTS}}

    def ask(self, variant: Variant, rep: int) -> Answer:
        started = time.perf_counter()
        common = {
            "variant": variant.id,
            "part": variant.part,
            "rep": rep,
            "question": variant.text,
            "model": self.config.model,
            "effort": self.config.effort,
        }
        for attempt, delay in enumerate(RETRY_DELAYS):
            try:
                response = self.client.messages.create(
                    model=self.config.model,
                    max_tokens=self.config.max_tokens,
                    output_config={
                        "effort": self.config.effort,
                        "format": {"type": "json_schema", "schema": H2_SCHEMA},
                    },
                    system=self.systems.get(variant.part, self.systems[""]),
                    messages=[{"role": "user", "content": f"Pytanie: {variant.text}"}],
                )
            except anthropic.APIError as error:
                if not _retryable(error) or attempt == len(RETRY_DELAYS) - 1:
                    return Answer(
                        **common,
                        ts=_now(),
                        latency_s=_since(started),
                        error=f"{type(error).__name__}: {error}",
                    )
                time.sleep(delay)
                continue

            raw = next((b.text for b in response.content if b.type == "text"), "")
            tokens = Tokens.of(response.usage)
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError as error:
                return Answer(
                    **common,
                    ts=_now(),
                    latency_s=_since(started),
                    input_tokens=tokens.prompt,
                    output_tokens=tokens.output,
                    raw=raw,
                    error=f"JSONDecodeError: {error}",
                )
            return Answer(
                **common,
                ts=_now(),
                latency_s=_since(started),
                input_tokens=tokens.prompt,
                output_tokens=tokens.output,
                sql=parsed.get("sql", ""),
                uwagi=parsed.get("uwagi", ""),
                raw=raw,
            )
        raise AssertionError("unreachable")

    def run(
        self,
        trials: list[tuple[Variant, int]],
        store: AnswerStore,
        workers: int = 4,
    ) -> Iterator[Answer]:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            for answer in pool.map(lambda trial: self.ask(*trial), trials):
                store.append(answer)
                yield answer


def plan(
    variants: list[Variant], reps: int, done: set[tuple[str, int]]
) -> list[tuple[Variant, int]]:
    # Kolejność: najpierw powtórzenie 1 wszystkich wariantów, potem 2 itd.,
    # żeby przerwana seria dawała zrównoważony materiał.
    return [
        (variant, rep)
        for rep in range(1, reps + 1)
        for variant in variants
        if (variant.id, rep) not in done
    ]


def _retryable(error: anthropic.APIError) -> bool:
    if isinstance(error, (anthropic.APIConnectionError, anthropic.RateLimitError)):
        return True
    status = getattr(error, "status_code", None)
    return status is not None and status >= 500


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _since(started: float) -> float:
    return round(time.perf_counter() - started, 2)
