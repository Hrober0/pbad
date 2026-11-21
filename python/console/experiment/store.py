import json
from dataclasses import asdict, dataclass
from pathlib import Path
from threading import Lock

RESULTS_PATH = (
    Path(__file__).resolve().parents[3]
    / "eksperyment"
    / "selected"
    / "H1"
    / "wyniki"
    / "odpowiedzi.jsonl"
)

TrialKey = tuple[str, str, int]


@dataclass(frozen=True)
class Record:
    ts: str
    question_id: str
    level: str
    rep: int
    model: str
    effort: str
    latency_s: float
    input_tokens: int = 0
    output_tokens: int = 0
    sql: str = ""
    explanation: str = ""
    raw: str = ""
    error: str = ""

    @property
    def key(self) -> TrialKey:
        return (self.question_id, self.level, self.rep)


class Store:
    def __init__(self, path: Path = RESULTS_PATH) -> None:
        self.path = path
        self._lock = Lock()

    def append(self, record: Record) -> None:
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as file:
                file.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")

    def done(self) -> set[TrialKey]:
        return {
            (row["question_id"], row["level"], row["rep"])
            for row in self.rows()
            if not row.get("error")
        }

    def rows(self) -> list[dict]:
        if not self.path.exists():
            return []
        return [
            json.loads(line)
            for line in self.path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
