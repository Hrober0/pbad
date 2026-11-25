"""Tabele markdown z wynikami eksperymentu 2 → wyniki/tabele.md (plik generowany, nie edytować ręcznie).

Analiza jest opisowa: mediany, iloraz median, rozkład wartości z powtórzeń.
Bez testów statystycznych (ocena.md).
"""

import re
import statistics
from collections import Counter, defaultdict
from datetime import date

from experiment.executor import sql_sha

from .analyze import (
    MIN_ILORAZ, MIN_UDZIAL_PROB, SENSITIVITY, VariantSummary, descriptive, factors, summarize,
)
from .extract import extract_all
from .generate import AnswerStore
from .paths import REPLICATION_PATH, TABLES_PATH
from .questions import load_variants

OLD_REPS = 5  # pierwsza seria (24.11) miała 5 powtórzeń; porównanie 5 vs 10 w sekcji 10


def fmt(value, unit: str = "") -> str:
    if value is None:
        return "–"
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    if isinstance(value, float):
        value = round(value, 1)
    text = f"{value:,}".replace(",", " ") if isinstance(value, (int, float)) else str(value)
    return f"{text} {unit}".strip()


def distribution(group: list[dict]) -> str:
    """Np. „500 ×8, 1 000 ×2” albo „pusty_wynik ×3”."""
    labels = [fmt(r.get("wartosc")) if r.get("wartosc") is not None else r["rodzaj"].lower() for r in group]
    counts = Counter(labels)
    return ", ".join(f"{label} ×{count}" for label, count in counts.most_common())


def ratio_text(ratio: float | None) -> str:
    return f"{ratio:.2f}" if ratio is not None else "–"


def write_report() -> str:
    rows = extract_all()
    answers = AnswerStore().good()
    variants = {v.id: v for v in load_variants()}
    summaries = summarize(rows)
    by_variant: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_variant[row["variant"]].append(row)
    for group in by_variant.values():
        group.sort(key=lambda r: r["rep"])
    sql_by_variant: dict[str, list[str]] = defaultdict(list)
    for answer in answers:
        sql_by_variant[answer["variant"]].append(sql_sha(answer["sql"]))

    out: list[str] = []
    w = out.append

    def median_of(vid: str) -> float | None:
        return summaries[vid].median if vid in summaries else None

    w("# PB2: tabele wyników (generowane)\n")
    w(f"Plik generuje `python run_h2.py report` ({date.today().isoformat()}). Nie edytować ręcznie — "
      "opis i wnioski są w [../opracowanie.md](../opracowanie.md), metoda w [../ocena.md](../ocena.md).\n")
    tin = sum(a["input_tokens"] for a in answers)
    tout = sum(a["output_tokens"] for a in answers)
    model = Counter(a["model"] for a in answers).most_common(1)[0][0]
    effort = Counter(a["effort"] for a in answers).most_common(1)[0][0]
    reps = Counter(len(g) for g in by_variant.values())
    w(f"Model `{model}`, effort `{effort}`, kontekst K2. Wariantów: {len(by_variant)}, prób: {len(answers)} "
      f"(powtórzeń na wariant: {', '.join(f'{k} × {v} wariantów' for k, v in sorted(reps.items()))}). "
      f"Tokeny: {fmt(tin)} wejściowych, {fmt(tout)} wyjściowych. "
      "Główna seria to części 2a–2g (84 warianty, 840 prób); część 2h to pytanie dodatkowe dopisane po dyskusji wyników.\n")

    # ------------------------------------------------------------ warianty
    w("## 1. Każdy wariant\n")
    w("Rodzaj dominujący (ile prób tego rodzaju), rozkład wartości z powtórzeń, mediana i zakres, liczba wierszy "
      "wyniku (mediana), w ilu próbach model podał przyjętą wartość w uwagach, ile różnych SQL.\n")
    w("| # | Pytanie | Rodzaj | Rozkład wartości | Mediana | Zakres | Wiersze | Ujawnił | Różne SQL |")
    w("|---|---|---|---|---|---|---|---|---|")
    for vid, variant in variants.items():
        group = by_variant.get(vid, [])
        if not group:
            continue
        s = summaries[vid]
        n = len(group)
        unit = next((r.get("jednostka", "") for r in group if r["rodzaj"] == s.dominant), "")
        rows_n = [r["wiersze"] for r in group if r.get("wiersze") is not None]
        span = f"{fmt(min(s.values))}–{fmt(max(s.values))}" if s.values else "–"
        w(f"| {vid} | {variant.text} | {s.dominant} ({s.n_dominant}/{n}) | {distribution(group)} | "
          f"{fmt(s.median, unit)} | {span} | {fmt(statistics.median(rows_n)) if rows_n else '–'} | "
          f"{sum(r['ujawnienie'] for r in group)}/{n} | {len(set(sql_by_variant[vid]))} |")
    w("")

    # ------------------------------------------------------------ czynniki
    w("## 2. Porównania kierunkowe (czynniki S, M, O)\n")
    w(f"`ROŚNIE`: mediana B ≥ {MIN_ILORAZ} × mediana A; `MALEJE`: mediana B ≤ mediana A / {MIN_ILORAZ}; "
      "`BEZ_ZMIANY`: pomiędzy. „Zakresy rozłączne”: każda wartość B jest większa (albo mniejsza) od każdej "
      f"wartości A. Wariant jest niestabilny, gdy mniej niż {MIN_UDZIAL_PROB:.0%} prób ma ten sam rodzaj "
      "interpretacji z odczytaną wartością (np. model odmawia).\n")
    results = factors(summaries)
    for factor in results:
        w(f"### {factor.name}\n")
        w("| A | B | Mediana A | Mediana B | B/A | Zakresy rozłączne | Wynik |")
        w("|---|---|---|---|---|---|---|")
        for c in factor.comparisons:
            disjoint = "–" if c.disjoint is None else ("tak" if c.disjoint else "nie")
            w(f"| {c.a} | {c.b} | {fmt(median_of(c.a))} | {fmt(median_of(c.b))} | {ratio_text(c.ratio)} | "
              f"{disjoint} | {c.result}{' (' + c.note + ')' if c.note else ''} |")
        w("")
    w("### Podsumowanie czynników\n")
    w("| Czynnik | Porównań | Rozstrzygniętych | Rośnie | w tym zakresy rozłączne | Bez zmiany | Maleje | Odpadło | Opis |")
    w("|---|---|---|---|---|---|---|---|---|")
    for f in results:
        w(f"| {f.name} | {len(f.comparisons)} | {f.resolved} | {f.up} | {f.up_disjoint} | {f.count('BEZ_ZMIANY')} | "
          f"{f.count('MALEJE')} | {len(f.comparisons) - f.resolved} | **{f.label}** |")
    w("")
    w("### Wrażliwość na próg ilorazu\n")
    thresholds = (MIN_ILORAZ, *SENSITIVITY)
    w("| Czynnik | " + " | ".join(f"iloraz ≥ {t}" for t in thresholds) + " |")
    w("|---|" + "---|" * len(thresholds))
    by_threshold = [factors(summaries, t) for t in thresholds]
    for i, f in enumerate(results):
        w(f"| {f.name} | " + " | ".join(f"{r[i].up}/{r[i].resolved} — {r[i].label}" for r in by_threshold) + " |")
    w("")

    # -------------------------------------------------------- opisowe
    w("## 3. Porównania bez oczekiwanego kierunku (w tym część 2f)\n")
    w("| Porównanie | A | B | Mediana A | Mediana B | B/A | Zakresy rozłączne | Wynik |")
    w("|---|---|---|---|---|---|---|---|")
    for name, comps in descriptive(summaries).items():
        for c in comps:
            disjoint = "–" if c.disjoint is None else ("tak" if c.disjoint else "nie")
            w(f"| {name} | {c.a} | {c.b} | {fmt(median_of(c.a))} | {fmt(median_of(c.b))} | {ratio_text(c.ratio)} | "
              f"{disjoint} | {c.result}{' (' + c.note + ')' if c.note else ''} |")
    w("")

    # -------------------------------------------------------- 2b prędkości
    w("## 4. Część 2b: przyjęta prędkość\n")
    w("„Promień / 15 min” to prędkość wyliczona z promienia w linii prostej. Model czasem zmniejsza promień "
      "o współczynnik krętości dróg, więc ważniejsza jest prędkość, którą sam podaje w uwagach.\n")
    w("| # | Wariant | Rozkład promienia | Promień / 15 min (km/h) | Prędkość podana w uwagach (km/h) | Uwagi wspominają krętość dróg |")
    w("|---|---|---|---|---|---|")
    uwagi = {(a["variant"], a["rep"]): a.get("uwagi", "") for a in answers}
    for vid in ("8a", "8b", "8d", "8c"):
        group = by_variant.get(vid, [])
        speeds = Counter(f"{r['wartosc'] / 1000 * 4:.1f}" for r in group if r["rodzaj"] == "PROMIEŃ")
        texts = [uwagi.get((vid, r["rep"]), "") for r in group]
        stated = Counter(m for t in texts for m in set(re.findall(r"(\d+(?:[,.]\d+)?)\s*km/h", t)))
        winding = sum(bool(re.search(r"kręto|krętoś|kręte", t, re.I)) for t in texts)
        w(f"| {vid} | {variants[vid].text} | {distribution(group)} | "
          f"{', '.join(f'{k} ×{v}' for k, v in speeds.most_common()) or '–'} | "
          f"{', '.join(f'{k} ×{v}' for k, v in stated.most_common()) or '–'} | {winding}/{len(group)} |")
    w("")

    # -------------------------------------------------------- 2f gradient
    w("## 5. Część 2f: gradient miejscowości\n")
    w("Apteki „w pobliżu stacji …”. Liczba aptek wokół stacji: [../pytania.md](../pytania.md#część-2f-dodatkowe-kontrasty-eksploracja--16-wariantów).\n")
    w("| # | Stacja | Rozkład promienia | Mediana | Wiersze (mediana) | Prób z pustym wynikiem |")
    w("|---|---|---|---|---|---|")
    for vid, name in (("1a", "Dworzec Centralny"), ("29a", "stacja Warszawa Centralna"),
                      ("29b", "stacja Warszawa Centralna, samochodem"), ("23a", "Radom Główny"), ("23b", "Siedlce"),
                      ("5a", "Tłuszcz"), ("23c", "Celestynów"), ("23d", "Krusze"), ("24", "Krusze, samochodem")):
        group = by_variant.get(vid, [])
        if not group:
            continue
        rows_n = [r["wiersze"] for r in group if r.get("wiersze") is not None]
        empty = sum(r.get("wiersze") == 0 for r in group)
        w(f"| {vid} | {name} | {distribution(group)} | {fmt(median_of(vid))} | "
          f"{fmt(statistics.median(rows_n)) if rows_n else '–'} | {empty}/{len(group)} |")
    w("")

    # -------------------------------------------------------- 2c / 2d
    w("## 6. Części 2c i 2d\n")
    w("| # | Pytanie | Rozkład wartości | Wiersze (mediana) | Prób z pustym wynikiem |")
    w("|---|---|---|---|---|")
    for vid, variant in variants.items():
        if variant.part not in {"2c", "2d"}:
            continue
        group = by_variant.get(vid, [])
        unit = group[0].get("jednostka", "") if group else ""
        rows_n = [r["wiersze"] for r in group if r.get("wiersze") is not None]
        w(f"| {vid} | {variant.text} | {distribution(group)} ({unit}) | "
          f"{fmt(statistics.median(rows_n)) if rows_n else '–'} | {sum(r.get('wiersze') == 0 for r in group)}/{len(group)} |")
    w("")

    # -------------------------------------------------------- 2e
    w("## 7. Część 2e: rozpoznanie obiektu\n")
    w("Kandydaci i wartości wzorcowe: [../pytania.md](../pytania.md#kandydaci-w-bazie-i-odległości-wzorcowe).\n")
    w("| # | Pytanie | Rozkład wyników | Ocena obiektu |")
    w("|---|---|---|---|")
    for vid, variant in variants.items():
        if variant.part != "2e":
            continue
        group = by_variant.get(vid, [])
        if vid in {"22b", "22c"}:
            w(f"| {vid} | {variant.text} | promień: {distribution(group)}; wiersze: "
              f"{', '.join(f'{k} ×{v}' for k, v in Counter(r.get('wiersze') for r in group).most_common())} | – |")
            continue
        verdicts = Counter(r.get("ocena_obiektu", r["rodzaj"].lower()) for r in group)
        w(f"| {vid} | {variant.text} | {distribution(group)} | {', '.join(f'{k} ×{v}' for k, v in verdicts.most_common())} |")
    w("")
    w("### Przyczyny pustych wyników w 2e\n")
    w("Diagnoza automatyczna: każde podzapytanie wykonane osobno; podajemy to, które zwraca 0 wierszy.\n")
    w("| # | Diagnoza | Prób |")
    w("|---|---|---|")
    for vid, variant in variants.items():
        if variant.part != "2e":
            continue
        reasons = Counter(r["opis"] for r in by_variant.get(vid, []) if r["rodzaj"] in ("PUSTY_WYNIK", "BRAK_SQL"))
        for reason, count in reasons.most_common():
            w(f"| {vid} | {reason[:160]} | {count} |")
    w("")
    w("### Wybrany kandydat w każdej próbie\n")
    w("| # | Próba | Wynik | Kandydat | Ocena |")
    w("|---|---|---|---|---|")
    for vid, variant in variants.items():
        if variant.part != "2e" or vid in {"22b", "22c"}:
            continue
        for r in by_variant.get(vid, []):
            w(f"| {vid} | {r['rep']} | {fmt(r.get('wartosc'))} | {r.get('kandydat', r['rodzaj'])} | {r.get('ocena_obiektu', '–')} |")
    w("")

    # -------------------------------------------------------- 2g
    from .references import BASE_2G

    if any(v.part == "2g" for v in variants.values()):
        w("## 7a. Część 2g: próba naprawy (K2 + wskazówka o wyszukiwaniu po nazwie)\n")
        w("Te same pytania co w 2e, w kontekście dopisana jedna ogólna wskazówka (pytania.md, część 2g).\n")
        w("| 2g | 2e | Obiekt | 2e: ocena obiektu | 2g: ocena obiektu | 2g: rozkład wyników |")
        w("|---|---|---|---|---|---|")

        def verdicts(vid: str) -> str:
            counts = Counter(r.get("ocena_obiektu") or r["rodzaj"].lower() for r in by_variant.get(vid, []))
            return ", ".join(f"{k} ×{v}" for k, v in counts.most_common())

        for new, base in BASE_2G.items():
            if new not in by_variant:
                continue
            w(f"| {new} | {base} | {variants[base].text[:70]} | {verdicts(base)} | {verdicts(new)} | {distribution(by_variant[new])} |")
        w("")
        w("### Przyczyny pustych wyników i pomyłek w 2g\n")
        w("| # | Próba | Wynik | Kandydat / diagnoza | Ocena |")
        w("|---|---|---|---|---|")
        for new in BASE_2G:
            for r in by_variant.get(new, []):
                if r.get("ocena_obiektu") not in ("poprawny", "dopuszczalny"):
                    w(f"| {new} | {r['rep']} | {fmt(r.get('wartosc'))} | {r.get('kandydat') if r.get('wartosc') is not None else r['opis'][:140]} | {r.get('ocena_obiektu', r['rodzaj'])} |")
        w("")

    # -------------------------------------------------------- puste wyniki z promieniem
    w("## 8. Puste wyniki przy pytaniach z promieniem\n")
    w("Przy pustym wyniku skrypt powtarza zapytanie z promieniem 10⁸ m. Jeśli nadal nic nie zwraca, "
      "zawiódł punkt odniesienia, a nie promień.\n")
    w("| # | Promień (rozkład) | Punkt odniesienia znaleziony | nie znaleziony |")
    w("|---|---|---|---|")
    empties: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        if "punkt_odniesienia" in r:
            empties[r["variant"]].append(r)
    for vid, group in empties.items():
        w(f"| {vid} | {distribution(group)} | {sum(r['punkt_odniesienia'] == 'znaleziony' for r in group)} | "
          f"{sum(r['punkt_odniesienia'] == 'NIE znaleziony' for r in group)} |")
    w("")

    # -------------------------------------------------------- ujawnianie
    w("## 9. Ujawnianie założeń i powtarzalność\n")
    by_part: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_part[r["part"]].append(r)
    w("| Część | Prób | Uwagi niepuste | Ujawnił wartość/założenie | Warianty z jednym SQL we wszystkich próbach | Warianty z jedną wartością we wszystkich próbach |")
    w("|---|---|---|---|---|---|")
    for part, group in sorted(by_part.items()):
        ids = sorted({r["variant"] for r in group})
        same_sql = sum(len(set(sql_by_variant[v])) == 1 for v in ids)
        same_value = sum(len({(r["rodzaj"], r.get("wartosc")) for r in by_variant[v]}) == 1 for v in ids)
        w(f"| {part} | {len(group)} | {sum(not r['uwagi_puste'] for r in group)} | {sum(r['ujawnienie'] for r in group)} | "
          f"{same_sql}/{len(ids)} | {same_value}/{len(ids)} |")
    w("")

    # -------------------------------------------------------- 5 vs 10
    first = summarize(rows, max_rep=OLD_REPS)
    if max(len(g) for g in by_variant.values()) > OLD_REPS:
        w(f"## 10. Czy więcej powtórzeń coś zmienia? Pierwsze {OLD_REPS} prób a wszystkie\n")
        w(f"Dla każdego wariantu z przyjętą wartością (części 2a–2d i 2f): rodzaj dominujący i mediana z prób 1–{OLD_REPS} "
          "oraz ze wszystkich prób. Wypisane są tylko warianty, w których coś się zmieniło. Części 2e i 2g pomijamy, "
          "bo mediana odległości miesza tam różne obiekty; dla nich patrz ocena obiektu w sekcji 7.\n")
        w("| # | Pierwsze 5: rodzaj, mediana, rozkład | Wszystkie: rodzaj, mediana, rozkład |")
        w("|---|---|---|")
        changed = 0
        compared = 0
        for vid, variant in variants.items():
            if vid not in first or vid not in summaries or variant.part in {"2e", "2g", "2h"}:
                continue
            compared += 1
            a: VariantSummary = first[vid]
            b: VariantSummary = summaries[vid]
            if a.n == b.n:
                continue
            first_group = [r for r in by_variant[vid] if r["rep"] <= OLD_REPS]
            if a.dominant != b.dominant or a.median != b.median or a.stable != b.stable:
                changed += 1
                w(f"| {vid} | {a.dominant}, {fmt(a.median)}; {distribution(first_group)} | "
                  f"{b.dominant}, {fmt(b.median)}; {distribution(by_variant[vid])} |")
        w(f"\nWariantów ze zmianą rodzaju dominującego, mediany albo stabilności: {changed} z {compared}.\n")
        w("| Czynnik | Pierwsze 5 prób | Wszystkie próby |")
        w("|---|---|---|")
        for f5, f_all in zip(factors(first), results):
            w(f"| {f_all.name} | {f5.up}/{f5.resolved} — {f5.label} | {f_all.up}/{f_all.resolved} — {f_all.label} |")
        w("")
        w("| Porównanie | Pierwsze 5 prób | Wszystkie próby |")
        w("|---|---|---|")
        d5, d_all = descriptive(first), descriptive(summaries)
        for name, comps in d_all.items():
            for c_all, c5 in zip(comps, d5.get(name, [None] * len(comps))):
                if c5 is None or c5.result != c_all.result:
                    w(f"| {name}: {c_all.a} → {c_all.b} | {c5.result if c5 else '–'} | {c_all.result} |")
        w("")

    # -------------------------------------------------------- replikacja
    if REPLICATION_PATH.exists():
        from .replicate import compare_with_main

        rep = compare_with_main()
        n = sum(r["n"] for r in rep)
        w("## 11. Replikacja (osobna seria z 24.11, 2 próby na wariant, poza analizą)\n")
        w(f"Prób: {n}. Ten sam rodzaj interpretacji co dominujący w serii głównej: {sum(r['same_kind'] for r in rep)}/{n}. "
          f"Wartość w zakresie min–max serii głównej: {sum(r['in_range'] for r in rep)}/{n} "
          "(próby bez wartości, np. odmowa albo pusty wynik, liczą się tu jako poza zakresem nawet przy zgodnym rodzaju).\n")
        w("| # | Seria główna | Replikacja | Ocena obiektu (2e) |")
        w("|---|---|---|---|")
        for r in rep:
            if r["in_range"] < r["n"]:
                vals = ", ".join(f"{k.lower()} {fmt(v)}" if v is not None else k.lower() for k, v in r["replica"])
                w(f"| {r['variant']} | {r['main']} | {vals} | {r['verdicts'] or '–'} |")
        w("")

    corrections = [r for r in rows if r["zrodlo"] == "korekta"]
    w(f"Ręcznych korekt odczytu: {len(corrections)} (wyniki/korekty.json).\n")

    TABLES_PATH.write_text("\n".join(out), encoding="utf-8")
    return str(TABLES_PATH)
