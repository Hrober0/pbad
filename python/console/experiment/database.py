import os
from dataclasses import dataclass, field
from datetime import date, datetime, time
from decimal import Decimal
from time import perf_counter

import psycopg

DSN = os.getenv("PBAD_DSN", "postgresql://pbad_ro:pbad_ro@localhost:5432/pbad")
TIMEOUT_MS = int(os.getenv("PBAD_TIMEOUT_MS", "120000"))
MAX_ROWS = 2000

OPTIONS = f"-c statement_timeout={TIMEOUT_MS} -c default_transaction_read_only=on"


@dataclass(frozen=True)
class QueryResult:
    columns: list[str] = field(default_factory=list)
    rows: list[list] = field(default_factory=list)
    row_count: int = 0
    truncated: bool = False
    duration_s: float = 0.0
    error: str = ""

    @property
    def executed(self) -> bool:
        return not self.error


def execute(sql: str, dsn: str = DSN) -> QueryResult:
    if not sql.strip():
        return QueryResult(error="empty sql")

    started = perf_counter()
    try:
        with psycopg.connect(dsn, options=OPTIONS, autocommit=True) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)  # noqa: S608 - model output, run as a read-only role
                if cursor.description is None:
                    return QueryResult(
                        error="statement returned no result set",
                        duration_s=_elapsed(started),
                    )
                columns = [column.name for column in cursor.description]
                rows = cursor.fetchmany(MAX_ROWS + 1)
    except psycopg.Error as error:
        return QueryResult(
            error=f"{type(error).__name__}: {str(error).strip()}",
            duration_s=_elapsed(started),
        )

    return QueryResult(
        columns=columns,
        rows=[[_cell(value) for value in row] for row in rows[:MAX_ROWS]],
        row_count=min(len(rows), MAX_ROWS),
        truncated=len(rows) > MAX_ROWS,
        duration_s=_elapsed(started),
    )


def _elapsed(started: float) -> float:
    return round(perf_counter() - started, 3)


def _cell(value: object) -> object:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    if isinstance(value, (bytes, memoryview)):
        return bytes(value).hex()
    return str(value)
