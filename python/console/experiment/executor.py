import hashlib
import json
from collections.abc import Iterator
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .database import QueryResult, execute
from .store import RESULTS_PATH, Store

EXECUTIONS_PATH = RESULTS_PATH.with_name("wykonania.jsonl")


@dataclass(frozen=True)
class Execution:
    question_id: str
    level: str
    rep: int
    sql_sha: str
    executed: bool
    row_count: int = 0
    truncated: bool = False
    duration_s: float = 0.0
    columns: list[str] = field(default_factory=list)
    rows: list[list] = field(default_factory=list)
    error: str = ""

    @property
    def key(self) -> tuple[str, str, int]:
        return (self.question_id, self.level, self.rep)


class Executor:
    """Wykonuje SQL wygenerowany przez model. Osobny krok, żeby dało się
    powtórzyć ocenę bez ponownego odpytywania modelu."""

    def __init__(
        self,
        answers: Path = RESULTS_PATH,
        executions: Path = EXECUTIONS_PATH,
    ) -> None:
        self._answers = Store(answers)
        self._path = executions
        self._cache: dict[str, QueryResult] = {}

    def run(self, resume: bool = True) -> Iterator[Execution]:
        done = self._done() if resume else set()
        pending = [
            row
            for row in self._answers.rows()
            if not row.get("error")
            and (row["question_id"], row["level"], row["rep"]) not in done
        ]
        for row in pending:
            execution = self._execute(row)
            self._append(execution)
            yield execution

    def _execute(self, row: dict) -> Execution:
        sql = row.get("sql", "")
        sha = sql_sha(sql)
        if sha not in self._cache:
            self._cache[sha] = execute(sql)
        result = self._cache[sha]
        return Execution(
            question_id=row["question_id"],
            level=row["level"],
            rep=row["rep"],
            sql_sha=sha,
            executed=result.executed,
            row_count=result.row_count,
            truncated=result.truncated,
            duration_s=result.duration_s,
            columns=result.columns,
            rows=result.rows,
            error=result.error,
        )

    def _append(self, execution: Execution) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(asdict(execution), ensure_ascii=False) + "\n")

    def _done(self) -> set[tuple[str, str, int]]:
        if not self._path.exists():
            return set()
        return {
            (row["question_id"], row["level"], row["rep"])
            for row in map(json.loads, self._path.read_text(encoding="utf-8").splitlines())
        }


def sql_sha(sql: str) -> str:
    return hashlib.sha256(" ".join(sql.split()).encode("utf-8")).hexdigest()[:12]
