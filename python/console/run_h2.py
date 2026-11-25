"""Eksperyment 2 (PB2): 84 warianty × 10 powtórzeń w części głównej (2a–2g) i 1 pytanie dodatkowe (2h),
kontekst K2 (w części 2g z dodatkową wskazówką).

Kroki są rozdzielone, żeby analizę dało się powtórzyć bez odpytywania modelu:

    python run_h2.py one 15a               jedno pytanie, bez zapisu (podgląd)
    python run_h2.py run                   cała seria do wyniki/odpowiedzi.jsonl
    python run_h2.py exec                  wykonanie SQL-i na bazie (wyniki/wykonania.jsonl)
    python run_h2.py extract               odczyt przyjętych wartości (wyniki/odczyty.jsonl)
    python run_h2.py report                porównania i tabele (wyniki/tabele.md)
    python run_h2.py all                   run + exec + extract + report
    python run_h2.py status                postęp
    python run_h2.py show 15a              odpowiedzi i odczyty jednego wariantu
    python run_h2.py replicate             seria kontrolna (2 próby/wariant) do wyniki/replikacja.jsonl

Sprawdzenie dodatkowe z dostępem do bazy (h2/with_db.py, osobny plik wyników):

    python run_h2.py zbaza --only 24 15a --reps 3   model może wykonywać SELECT-y narzędziem run_sql
    python run_h2.py zbaza-raport                   porównanie z serią główną → wyniki/z_baza.md
    python run_h2.py zbaza-show 24                  kroki i końcowe SQL jednego wariantu

Ręczne poprawki odczytów: wyniki/korekty.json (opis w ocena.md).
"""

import argparse
import os
import sys
from collections import Counter

from dotenv import load_dotenv
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table

from h2 import execute as h2_execute
from h2.generate import AnswerStore, Generator, plan
from h2.questions import load_variants

console = Console()


def main() -> int:
    load_dotenv()
    args = _parser().parse_args()
    if args.needs_key and not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[red]Brak ANTHROPIC_API_KEY w python/console/.env[/]")
        return 1
    return args.handler(args)


def cmd_one(args: argparse.Namespace) -> int:
    variant = _variant(args.variant)
    console.print(f"[cyan]{variant.id}[/] {variant.text}")
    with console.status("Generowanie...", spinner="dots"):
        answer = Generator().ask(variant, rep=0)
    if answer.error:
        console.print(f"[red]{answer.error}[/]")
        return 1
    console.print(Syntax(answer.sql, "sql", theme="ansi_dark", word_wrap=True))
    console.print(f"[yellow]uwagi:[/] {answer.uwagi}")
    if args.exec:
        from experiment.database import execute

        result = execute(answer.sql)
        console.print(result.error or f"{result.row_count} wierszy: {result.rows[:5]}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    store = AnswerStore()
    variants = load_variants()
    if args.only:
        variants = [v for v in variants if v.id in set(args.only) or v.part in set(args.only)]
    trials = plan(variants, args.reps, store.done())
    if not trials:
        console.print("[green]Seria kompletna.[/]")
        return 0
    console.print(f"[cyan]{len(trials)}[/] wywołań, {args.workers} równolegle → {store.path}")
    failures = 0
    for index, answer in enumerate(Generator().run(trials, store, args.workers), start=1):
        failures += bool(answer.error)
        mark = "[red]x[/]" if answer.error else "[green]ok[/]"
        console.print(
            f"{index:>3}/{len(trials)} {mark} {answer.variant:<4} #{answer.rep}"
            f" [dim]{answer.input_tokens}+{answer.output_tokens} tok · {answer.latency_s}s[/]"
            + (f" [red]{answer.error[:120]}[/]" if answer.error else "")
        )
    console.print(f"Gotowe. Błędów: {failures}")
    return 1 if failures else 0


def cmd_exec(args: argparse.Namespace) -> int:
    count = failures = 0
    for execution in h2_execute.run():
        count += 1
        failures += not execution.executed
        if not execution.executed:
            console.print(f"[red]x[/] {execution.variant} #{execution.rep} {execution.error[:120]}")
    console.print(f"Wykonano {count}, niewykonalnych {failures}.")
    return 0


def cmd_extract(args: argparse.Namespace) -> int:
    from h2.extract import extract_all

    rows = extract_all()
    kinds = Counter(row["rodzaj"] for row in rows)
    console.print(f"Odczytano {len(rows)} prób: {dict(kinds)}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    from h2.report import write_report

    path = write_report()
    console.print(f"Zapisano {path}")
    return 0


def cmd_all(args: argparse.Namespace) -> int:
    code = cmd_run(args)
    cmd_exec(args)
    cmd_extract(args)
    cmd_report(args)
    return code


def cmd_status(args: argparse.Namespace) -> int:
    rows = AnswerStore().rows()
    good = AnswerStore().good()
    variants = load_variants()
    table = Table(title="Postęp eksperymentu 2")
    for column in ("Część", "Warianty", "Udane", "Oczekiwane", "Błędy API"):
        table.add_column(column)
    for part in sorted({v.part for v in variants}):
        ids = {v.id for v in variants if v.part == part}
        table.add_row(
            part,
            str(len(ids)),
            str(sum(row["variant"] in ids for row in good)),
            str(len(ids) * args.reps),
            str(sum(row["variant"] in ids and bool(row.get("error")) for row in rows)),
        )
    console.print(table)
    tokens_in = sum(row.get("input_tokens", 0) for row in rows)
    tokens_out = sum(row.get("output_tokens", 0) for row in rows)
    console.print(f"Tokeny: wejście {tokens_in:,}, wyjście {tokens_out:,}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    from h2.extract import load_extracted

    extracted = {(r["variant"], r["rep"]): r for r in load_extracted()}
    for row in sorted(AnswerStore().good(), key=lambda r: r["rep"]):
        if row["variant"] != args.variant:
            continue
        info = extracted.get((row["variant"], row["rep"]), {})
        console.rule(f"{row['variant']} #{row['rep']}  {info.get('rodzaj', '?')} {info.get('wartosc', '')}")
        console.print(Syntax(row["sql"], "sql", theme="ansi_dark", word_wrap=True))
        console.print(f"[yellow]uwagi:[/] {row['uwagi']}")
        if info:
            console.print(f"[dim]{info.get('opis', '')} | wynik: {info.get('wynik', '')}[/]")
    return 0


def cmd_replicate(args: argparse.Namespace) -> int:
    from h2.replicate import run

    for index, answer in enumerate(run(args.reps, args.workers), start=1):
        console.print(f"{index:>3} {answer.variant} #{answer.rep} {answer.error[:100]}")
    return 0


def cmd_db_run(args: argparse.Namespace) -> int:
    from h2.with_db import DbGenerator, store

    answers = store()
    variants = [v for v in load_variants() if v.id in set(args.only) or v.part in set(args.only)]
    if not variants:
        console.print("[red]Podaj warianty albo części w --only, np. --only 24 15a 2d[/]")
        return 1
    trials = plan(variants, args.reps, answers.done())
    if not trials:
        console.print("[green]Wszystkie próby już są.[/]")
        return 0
    console.print(f"[cyan]{len(trials)}[/] prób z dostępem do bazy, {args.workers} równolegle → {answers.path}")
    failures = 0
    for index, answer in enumerate(DbGenerator().run(trials, answers, args.workers), start=1):
        failures += bool(answer.error)
        mark = "[red]x[/]" if answer.error else "[green]ok[/]"
        tokens = answer.input_tokens + answer.cache_read_tokens + answer.cache_write_tokens
        console.print(
            f"{index:>3}/{len(trials)} {mark} {answer.variant:<4} #{answer.rep} "
            f"[dim]{len(answer.steps)} zapytań · {tokens}+{answer.output_tokens} tok "
            f"(cache {answer.cache_read_tokens}) · {answer.latency_s}s[/]"
            + (f" [red]{answer.error[:120]}[/]" if answer.error else "")
        )
    console.print(f"Gotowe. Błędów: {failures}")
    return 1 if failures else 0


def cmd_db_report(args: argparse.Namespace) -> int:
    from h2.with_db import report

    console.print(report())
    return 0


def cmd_db_show(args: argparse.Namespace) -> int:
    from h2.with_db import store

    rows = sorted((a for a in store().good() if a["variant"] == args.variant), key=lambda a: a["rep"])
    if not rows:
        console.print(f"[yellow]Brak prób z bazą dla {args.variant}[/]")
        return 1
    console.print(f"[cyan]{args.variant}[/] {rows[0]['question']}")
    for answer in rows:
        console.rule(f"#{answer['rep']} · {len(answer['steps'])} zapytań narzędzia")
        for step in answer["steps"]:
            console.print(f"[dim]krok {step['krok']}: {step['wiersze']} wierszy {step['blad']}[/]")
            console.print(Syntax(step["sql"], "sql", theme="ansi_dark", word_wrap=True))
        console.print("[bold]końcowe:[/]")
        console.print(Syntax(answer["sql"], "sql", theme="ansi_dark", word_wrap=True))
        console.print(f"[yellow]uwagi:[/] {answer['uwagi']}")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(required=True)

    one = sub.add_parser("one", help="jedno pytanie, bez zapisu")
    one.add_argument("variant")
    one.add_argument("--exec", action="store_true")
    one.set_defaults(handler=cmd_one, needs_key=True)

    for name, handler in (("run", cmd_run), ("all", cmd_all)):
        cmd = sub.add_parser(name)
        cmd.add_argument("--reps", type=int, default=10)
        cmd.add_argument("--workers", type=int, default=4)
        cmd.add_argument("--only", nargs="+", help="kody wariantów albo części, np. 15a 2e")
        cmd.set_defaults(handler=handler, needs_key=True)

    for name, handler in (("exec", cmd_exec), ("extract", cmd_extract), ("report", cmd_report)):
        sub.add_parser(name).set_defaults(handler=handler, needs_key=False)

    status = sub.add_parser("status")
    status.add_argument("--reps", type=int, default=10)
    status.set_defaults(handler=cmd_status, needs_key=False)

    replicate = sub.add_parser("replicate", help="seria kontrolna do wyniki/replikacja.jsonl")
    replicate.add_argument("--reps", type=int, default=2)
    replicate.add_argument("--workers", type=int, default=6)
    replicate.set_defaults(handler=cmd_replicate, needs_key=True)

    show = sub.add_parser("show")
    show.add_argument("variant")
    show.set_defaults(handler=cmd_show, needs_key=False)

    db_run = sub.add_parser("zbaza", help="sprawdzenie dodatkowe: model z dostępem do bazy (wyniki/z_baza.jsonl)")
    db_run.add_argument("--only", nargs="+", required=True, help="kody wariantów albo części, np. 24 15a 2d")
    db_run.add_argument("--reps", type=int, default=3)
    db_run.add_argument("--workers", type=int, default=3)
    db_run.set_defaults(handler=cmd_db_run, needs_key=True)

    sub.add_parser("zbaza-raport", help="porównanie z serią główną (wyniki/z_baza.md)").set_defaults(
        handler=cmd_db_report, needs_key=False)

    db_show = sub.add_parser("zbaza-show", help="kroki i końcowe SQL jednego wariantu z bazą")
    db_show.add_argument("variant")
    db_show.set_defaults(handler=cmd_db_show, needs_key=False)
    return parser


def _variant(code: str):
    variants = {v.id: v for v in load_variants()}
    if code not in variants:
        raise SystemExit(f"Nie ma wariantu {code}. Dostępne: {', '.join(variants)}")
    return variants[code]


if __name__ == "__main__":
    sys.exit(main())
