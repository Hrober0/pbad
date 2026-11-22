"""Eksperyment 1 (H1): 20 pytań × 4 poziomy kontekstu × 3 powtórzenia.

Generowanie i wykonywanie SQL są rozdzielone, żeby ocenę dało się powtórzyć
bez ponownego odpytywania modelu:

    python run_h1.py one Z02 --level K2      jedno pytanie, bez zapisu
    python run_h1.py run                     cała seria do wyniki/odpowiedzi.jsonl
    python run_h1.py exec                    wykonanie SQL-i na bazie
    python run_h1.py compare                 porównanie z wzorcami i trafność
    python run_h1.py status                  postęp
"""

import argparse
import os
import sys

from dotenv import load_dotenv
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table

from experiment import Executor, Runner, Store, Trial, execute, load_questions, plan
from experiment.compare import evaluate_all
from llm import ContextLevel, SqlGenerator

console = Console()
LEVELS = [level.value for level in ContextLevel]


def main() -> int:
    load_dotenv()
    args = _parser().parse_args()
    if args.needs_key and not os.getenv("ANTHROPIC_API_KEY"):
        console.print(
            "[red]Brak klucza.[/] Wpisz go w [dim]python/console/.env[/]"
            " jako ANTHROPIC_API_KEY=sk-ant-..."
            " (klucz z platform.claude.com → Settings → API keys)."
        )
        return 1
    return args.handler(args)


def cmd_one(args: argparse.Namespace) -> int:
    question = _question(args.question_id)
    level = ContextLevel(args.level.upper())
    store = Store()
    runner = Runner(SqlGenerator(), store)
    trial = Trial(question, level, args.rep)

    console.print(f"[cyan]{question.id}[/] [dim]{level}[/] {question.text}")
    with console.status("Generowanie...", spinner="dots"):
        record = runner.run_trial(trial)

    if record.error:
        console.print(f"[red]{record.error}[/]")
        return 1

    console.print(Syntax(record.raw, "json", theme="ansi_dark", word_wrap=True))
    console.print(
        f"[dim]prompt {record.input_tokens} · output {record.output_tokens}"
        f" · {record.latency_s}s[/]"
    )

    if args.save:
        store.append(record)
        console.print(f"[green]Zapisano jako powtórzenie #{trial.rep}[/] [dim]{store.path}[/]")

    if args.exec:
        result = execute(record.sql)
        if not result.executed:
            console.print(f"[red]Baza: {result.error}[/]")
            return 1
        console.print(
            f"[green]Baza: {result.row_count} wierszy w {result.duration_s}s[/]"
        )
        console.print(_preview(result))
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    store = Store()
    levels = [ContextLevel(level.upper()) for level in args.levels]
    trials = plan(load_questions(), levels, args.reps, store.done())
    if not trials:
        console.print("[green]Nic do zrobienia — seria jest kompletna.[/]")
        return 0

    console.print(
        f"[cyan]{len(trials)}[/] wywołań do wykonania, {args.workers} równolegle."
        f" Zapis: [dim]{store.path}[/]"
    )
    if not args.yes and not _confirm():
        return 1

    runner = Runner(SqlGenerator(), store)
    failures = 0
    with console.status("Pytam model...", spinner="dots") as status:
        for index, record in enumerate(runner.run(trials, args.workers), start=1):
            failures += bool(record.error)
            mark = "[red]x[/]" if record.error else "[green]ok[/]"
            console.print(
                f"{index:>3}/{len(trials)} {mark} {record.question_id} {record.level}"
                f" #{record.rep} [dim]{record.input_tokens} tok · {record.latency_s}s[/]"
                + (f" [red]{record.error}[/]" if record.error else "")
            )
            status.update(f"Pytam model... {index}/{len(trials)}")

    console.print(f"[green]Gotowe.[/] Błędów: {failures}")
    return 1 if failures else 0


def cmd_exec(args: argparse.Namespace) -> int:
    executor = Executor()
    failures = 0
    count = 0
    for execution in executor.run(resume=not args.restart):
        count += 1
        failures += not execution.executed
        mark = "[green]ok[/]" if execution.executed else "[red]x[/]"
        console.print(
            f"{mark} {execution.question_id} {execution.level} #{execution.rep}"
            f" [dim]{execution.row_count} w. · {execution.duration_s}s[/]"
            + ("" if execution.executed else f" [red]{execution.error[:90]}[/]")
        )
    console.print(f"[green]Wykonano {count}.[/] Niewykonalnych zapytań: {failures}")
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    with console.status("Liczę wzorce i porównuję...", spinner="dots"):
        evaluations = evaluate_all()

    table = Table(title="Trafność — eksperyment 1")
    table.add_column("Pytanie")
    for level in LEVELS:
        table.add_column(level, justify="center")
    for question in load_questions():
        cells = []
        for level in LEVELS:
            group = [e for e in evaluations if e.question_id == question.id and e.level == level]
            cells.append(f"{sum(e.correct for e in group)}/{len(group)}")
        table.add_row(question.id, *cells)

    counts = [
        (sum(e.correct for e in group), len(group))
        for group in ([e for e in evaluations if e.level == level] for level in LEVELS)
    ]
    totals = [hits / total for hits, total in counts]
    table.add_section()
    table.add_row("[bold]razem[/]", *[f"[bold]{t:.0%}[/]" for t in totals])
    table.add_row(
        "[dim]95% CI[/]",
        *["[dim]{:.0%}–{:.0%}[/]".format(*_wilson(h, n)) for h, n in counts],
    )
    console.print(table)
    for (a, b), (ta, tb) in zip(zip(LEVELS, LEVELS[1:]), zip(totals, totals[1:])):
        console.print(f"przyrost {a} → {b}: [bold]{(tb - ta) * 100:+.1f} pp[/]")
    console.print("[dim]Szczegóły: eksperyment/selected/H1/wyniki/ocena.jsonl[/]")
    return 0


def _wilson(hits: int, total: int, z: float = 1.96) -> tuple[float, float]:
    if not total:
        return (0.0, 0.0)
    p = hits / total
    centre = (p + z * z / (2 * total)) / (1 + z * z / total)
    margin = z * ((p * (1 - p) / total + z * z / (4 * total * total)) ** 0.5) / (1 + z * z / total)
    return (centre - margin, centre + margin)


def cmd_status(args: argparse.Namespace) -> int:
    store = Store()
    rows = store.rows()
    questions = load_questions()
    expected = len(questions) * args.reps

    table = Table(title="Postęp eksperymentu 1")
    table.add_column("Poziom")
    table.add_column("Odpowiedzi", justify="right")
    table.add_column("Błędy", justify="right")
    table.add_column("Średnio tokenów", justify="right")
    for level in LEVELS:
        at_level = [row for row in rows if row["level"] == level]
        good = [row for row in at_level if not row.get("error")]
        tokens = [row["input_tokens"] for row in good] or [0]
        table.add_row(
            level,
            f"{len(good)}/{expected}",
            str(len(at_level) - len(good)),
            f"{sum(tokens) // len(tokens)}",
        )
    console.print(table)
    console.print(f"[dim]{store.path}[/]")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(required=True)

    one = sub.add_parser("one", help="jedno pytanie, bez zapisu do pliku")
    one.add_argument("question_id")
    one.add_argument("--level", default="K2", choices=LEVELS + [l.lower() for l in LEVELS])
    one.add_argument("--exec", action="store_true", help="wykonaj SQL na bazie")
    one.add_argument(
        "--save",
        action="store_true",
        help="dopisz próbę do odpowiedzi.jsonl (seria pominie potem to powtórzenie)",
    )
    one.add_argument("--rep", type=int, default=1, help="numer powtórzenia przy --save")
    one.set_defaults(handler=cmd_one, needs_key=True)

    run = sub.add_parser("run", help="cała seria z zapisem i wznawianiem")
    run.add_argument("--levels", nargs="+", default=LEVELS)
    run.add_argument("--reps", type=int, default=3)
    run.add_argument("--workers", type=int, default=4)
    run.add_argument("--yes", action="store_true", help="bez pytania o potwierdzenie")
    run.set_defaults(handler=cmd_run, needs_key=True)

    execute_cmd = sub.add_parser("exec", help="wykonanie zapisanych SQL-i na bazie")
    execute_cmd.add_argument("--restart", action="store_true", help="od zera")
    execute_cmd.set_defaults(handler=cmd_exec, needs_key=False)

    compare = sub.add_parser("compare", help="porównanie z wzorcami i trafność")
    compare.set_defaults(handler=cmd_compare, needs_key=False)

    status = sub.add_parser("status", help="ile prób już jest")
    status.add_argument("--reps", type=int, default=3)
    status.set_defaults(handler=cmd_status, needs_key=False)
    return parser


def _question(question_id: str):
    questions = {question.id: question for question in load_questions()}
    if question_id.upper() not in questions:
        raise SystemExit(f"Nie ma pytania {question_id}. Dostępne: {', '.join(questions)}")
    return questions[question_id.upper()]


def _preview(result, limit: int = 10) -> Table:
    table = Table(show_header=True, header_style="dim")
    for column in result.columns:
        table.add_column(column)
    for row in result.rows[:limit]:
        table.add_row(*("" if cell is None else str(cell) for cell in row))
    if result.row_count > limit:
        table.caption = f"pokazano {limit} z {result.row_count}"
    return table


def _confirm() -> bool:
    console.print("[yellow]Uruchomić? To kosztuje. [t/N][/]", end=" ")
    return input().strip().lower() in {"t", "tak", "y", "yes"}


if __name__ == "__main__":
    sys.exit(main())
