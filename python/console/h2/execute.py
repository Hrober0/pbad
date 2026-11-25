"""Wykonanie SQL z odpowiedzi modelu. Rola tylko do odczytu (PBAD_DSN)."""

import json
from collections.abc import Iterator
from dataclasses import asdict, dataclass, field
from pathlib import Path

from experiment.database import QueryResult, execute
from experiment.executor import sql_sha

from .generate import AnswerStore
from .paths import ANSWERS_PATH, EXECUTIONS_PATH

KEEP_ROWS = 100


@dataclass(frozen=True)
class Execution:
    variant: str
    rep: int
    sql_sha: str
    executed: bool
    row_count: int = 0
    truncated: bool = False
    duration_s: float = 0.0
    columns: list[str] = field(default_factory=list)
    rows: list[list] = field(default_factory=list)
    error: str = ""


class ExecutionStore:
    def __init__(self, path: Path = EXECUTIONS_PATH) -> None:
        self.path = path

    def rows(self) -> list[dict]:
        if not self.path.exists():
            return []
        return [
            json.loads(line)
            for line in self.path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def by_key(self) -> dict[tuple[str, int, str], dict]:
        return {(row["variant"], row["rep"], row["sql_sha"]): row for row in self.rows()}

    def append(self, execution: Execution) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(asdict(execution), ensure_ascii=False) + "\n")


def run(answers: Path = ANSWERS_PATH, store: ExecutionStore | None = None) -> Iterator[Execution]:
    """Wykonuje odpowiedzi, których jeszcze nie wykonano (klucz: wariant, powtórzenie, hash SQL)."""
    store = store or ExecutionStore()
    done = store.by_key()
    cache: dict[str, QueryResult] = {}
    for row in AnswerStore(answers).good():
        sha = sql_sha(row["sql"])
        if (row["variant"], row["rep"], sha) in done:
            continue
        if sha not in cache:
            cache[sha] = execute(row["sql"])
        result = cache[sha]
        execution = Execution(
            variant=row["variant"],
            rep=row["rep"],
            sql_sha=sha,
            executed=result.executed,
            row_count=result.row_count,
            truncated=result.truncated,
            duration_s=result.duration_s,
            columns=result.columns,
            rows=result.rows[:KEEP_ROWS],
            error=result.error,
        )
        store.append(execution)
        yield execution
