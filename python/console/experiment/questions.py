import re
from dataclasses import dataclass
from pathlib import Path

QUESTIONS_PATH = (
    Path(__file__).resolve().parents[3]
    / "eksperyment"
    / "selected"
    / "H1"
    / "pytania.md"
)

SECTION = "## Pytania"
ROW = re.compile(r"^\|\s*([ZNJAM]\d{2})\s*\|\s*(.+?)\s*\|")
EXPECTED = 20


@dataclass(frozen=True)
class Question:
    id: str
    text: str

    @property
    def category(self) -> str:
        return self.id[0]


def load_questions(path: Path = QUESTIONS_PATH) -> list[Question]:
    questions = [
        Question(match[1], match[2])
        for line in _section(path).splitlines()
        if (match := ROW.match(line))
    ]
    ids = [question.id for question in questions]
    if len(set(ids)) != len(ids):
        raise ValueError(f"Duplicate question codes in {path}")
    if len(questions) != EXPECTED:
        raise ValueError(f"Expected {EXPECTED} questions in {path}, got {len(questions)}")
    return questions


def _section(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    start = text.index(SECTION) + len(SECTION)
    end = text.find("\n## ", start)
    return text[start:end] if end != -1 else text[start:]
