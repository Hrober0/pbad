import json
import time
from collections.abc import Callable, Iterator
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone

import anthropic

from llm import ContextLevel, SqlGenerator

from .questions import Question
from .store import Record, Store

RETRY_DELAYS = (5, 20, 60)


@dataclass(frozen=True)
class Trial:
    question: Question
    level: ContextLevel
    rep: int

    @property
    def key(self) -> tuple[str, str, int]:
        return (self.question.id, str(self.level), self.rep)

    def __str__(self) -> str:
        return f"{self.question.id} {self.level} #{self.rep}"


def plan(
    questions: list[Question],
    levels: list[ContextLevel],
    reps: int,
    done: set[tuple[str, str, int]] | None = None,
) -> list[Trial]:
    done = done or set()
    trials = [
        Trial(question, level, rep)
        for question in questions
        for level in levels
        for rep in range(1, reps + 1)
    ]
    return [trial for trial in trials if trial.key not in done]


class Runner:
    def __init__(self, generator: SqlGenerator, store: Store) -> None:
        self._generator = generator
        self._store = store

    def run(
        self,
        trials: list[Trial],
        workers: int = 4,
        on_done: Callable[[Record], None] | None = None,
    ) -> Iterator[Record]:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            for record in pool.map(self.run_trial, trials):
                self._store.append(record)
                if on_done:
                    on_done(record)
                yield record

    def run_trial(self, trial: Trial) -> Record:
        started = time.perf_counter()
        for attempt, delay in enumerate(RETRY_DELAYS):
            try:
                answer = self._generator.generate(trial.question.text, trial.level)
            except anthropic.APIError as error:
                if not _retryable(error) or attempt == len(RETRY_DELAYS) - 1:
                    return self._failure(trial, started, error)
                time.sleep(delay)
            else:
                return self._success(trial, started, answer)
        raise AssertionError("unreachable")

    def _success(self, trial: Trial, started: float, answer) -> Record:
        try:
            parsed = json.loads(answer.raw)
        except json.JSONDecodeError as error:
            return Record(
                **self._common(trial, started),
                input_tokens=answer.tokens.prompt,
                output_tokens=answer.tokens.output,
                raw=answer.raw,
                error=f"JSONDecodeError: {error}",
            )
        return Record(
            **self._common(trial, started),
            input_tokens=answer.tokens.prompt,
            output_tokens=answer.tokens.output,
            sql=parsed.get("sql", ""),
            explanation=parsed.get("explanation", ""),
            raw=answer.raw,
        )

    def _failure(self, trial: Trial, started: float, error: Exception) -> Record:
        return Record(
            **self._common(trial, started),
            error=f"{type(error).__name__}: {error}",
        )

    def _common(self, trial: Trial, started: float) -> dict:
        config = self._generator.config
        return {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "question_id": trial.question.id,
            "level": str(trial.level),
            "rep": trial.rep,
            "model": config.model,
            "effort": config.effort,
            "latency_s": round(time.perf_counter() - started, 2),
        }


def _retryable(error: anthropic.APIError) -> bool:
    if isinstance(error, (anthropic.APIConnectionError, anthropic.RateLimitError)):
        return True
    status = getattr(error, "status_code", None)
    return status is not None and status >= 500
