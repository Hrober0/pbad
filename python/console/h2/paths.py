from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
H2_DIR = ROOT / "eksperyment" / "selected" / "H2"
QUESTIONS_PATH = H2_DIR / "pytania.md"
RESULTS_DIR = H2_DIR / "wyniki"
ANSWERS_PATH = RESULTS_DIR / "odpowiedzi.jsonl"
EXECUTIONS_PATH = RESULTS_DIR / "wykonania.jsonl"
EXTRACTED_PATH = RESULTS_DIR / "odczyty.jsonl"
CORRECTIONS_PATH = RESULTS_DIR / "korekty.json"
TABLES_PATH = RESULTS_DIR / "tabele.md"
REPLICATION_PATH = RESULTS_DIR / "replikacja.jsonl"
DB_ANSWERS_PATH = RESULTS_DIR / "z_baza.jsonl"
DB_REPORT_PATH = RESULTS_DIR / "z_baza.md"
