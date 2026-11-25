"""Odczyt przyjętej wartości i rodzaju interpretacji z SQL (ocena.md, "Odczyt").

Dla każdej próby powstaje jeden wiersz w wyniki/odczyty.jsonl:

    rodzaj     PROMIEŃ | K_NAJBLIŻSZYCH | OBSZAR | PRÓG | K_SKRAJNYCH | WZGLĘDNY
               | ODLEGŁOŚĆ | LICZBA | BRAK_SQL | BŁĄD_WYKONANIA | INNY
    wartosc    liczba w jednostce z kolumny "jednostka" (m, szt., m², …)
    opis       skąd wartość pochodzi (fragment SQL po normalizacji)
    stopnie    True, gdy promień podano w stopniach (błąd techniczny; wartość przeliczona)
    wynik      liczba wierszy albo pierwsza wartość wyniku
    ujawnienie czy pole "uwagi" podaje przyjętą wartość lub założenie
    zrodlo     auto | korekta (ręczna poprawka z wyniki/korekty.json)

Odczyt jest heurystyczny: wszystko, czego skrypt nie umie odczytać, dostaje
rodzaj INNY i trafia do ręcznego przejrzenia. Ręczne decyzje zapisujemy w
korekty.json z uzasadnieniem, nigdy w kodzie.
"""

import json
import math
import re
from functools import cache
from pathlib import Path

from experiment.database import execute
from experiment.executor import sql_sha

from .execute import ExecutionStore
from .generate import AnswerStore
from .paths import CORRECTIONS_PATH, EXTRACTED_PATH
from .identify import identify
from .references import classify_result

M_PER_DEG = 111_320  # metry na stopień szerokości; dla długości w Warszawie ok. 68 400

# ---------------------------------------------------------------- parsowanie


def normalize(sql: str) -> str:
    sql = re.sub(r"--[^\n]*", " ", sql)
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    return " ".join(sql.split())


def calls(sql: str, name: str) -> list[tuple[list[str], int]]:
    """Wszystkie wywołania funkcji `name` jako (argumenty, pozycja końca)."""
    found = []
    for match in re.finditer(rf"\b{name}\s*\(", sql, flags=re.I):
        depth, start, args, i = 1, match.end(), [], match.end()
        in_str = False
        while i < len(sql) and depth:
            ch = sql[i]
            if ch == "'":
                in_str = not in_str
            elif not in_str:
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                    if depth == 0:
                        args.append(sql[start:i].strip())
                        break
                elif ch == "," and depth == 1:
                    args.append(sql[start:i].strip())
                    start = i + 1
            i += 1
        found.append((args, i + 1))
    return found


def constants(sql: str) -> dict[str, float]:
    """Stałe nazwane w zapytaniu, np. `SELECT 1000 AS promien_m` albo `1000::float AS r`."""
    env = {}
    for match in re.finditer(
        r"(?<![\w.])(\d+(?:\.\d+)?(?:\s*[*/+-]\s*\d+(?:\.\d+)?)*)\s*(?:::\s*\w+(?:\s+precision)?)?\s+(?:as\s+)?(\w+)",
        sql,
        flags=re.I,
    ):
        value = eval_num(match[1])
        name = match[2].lower()
        if value is not None and name not in KEYWORDS:
            env[name] = value
    return env


KEYWORDS = {
    "and", "or", "then", "else", "end", "when", "limit", "order", "from", "where",
    "union", "group", "having", "desc", "asc", "offset", "rows", "row", "as", "is",
    "not", "between", "select", "join", "on", "cross", "left", "inner", "true", "false",
}

SAFE = re.compile(r"^[\d\s.+\-*/()]+$")


def eval_num(expr: str, env: dict[str, float] | None = None) -> float | None:
    if expr is None:
        return None
    text = expr.strip()
    text = re.sub(r"::\s*(numeric|float8?|double precision|real|int(eger)?|bigint|decimal)(\(\d+(,\d+)?\))?", "", text, flags=re.I)
    text = re.sub(r"\bcast\s*\((.*?)\s+as\s+\w+(\s+precision)?\)", r"\1", text, flags=re.I)
    if env:
        for name, value in sorted(env.items(), key=lambda item: -len(item[0])):
            text = re.sub(rf"(?<![\w.])(\w+\.)?{re.escape(name)}\b", repr(value), text, flags=re.I)
    text = text.strip()
    if not text or not SAFE.match(text):
        return None
    try:
        value = eval(text, {"__builtins__": {}}, {})  # noqa: S307 - tylko cyfry i operatory
    except Exception:  # noqa: BLE001
        return None
    return float(value) if isinstance(value, (int, float)) else None


def in_meters(args: list[str]) -> bool:
    joined = " ".join(args).lower()
    return "geography" in joined or "st_transform" in joined or "st_distancesphere" in joined


# ------------------------------------------------------- odległość / promień

COMPARE = r"\s*(<=|<)\s*"


def radius_candidates(sql: str) -> list[tuple[float, str, bool]]:
    """(promień w metrach, opis, czy w stopniach)."""
    env = constants(sql)
    found: list[tuple[float, str, bool]] = []

    for args, _ in calls(sql, "st_dwithin"):
        if len(args) >= 3:
            value = eval_num(args[2], env)
            if value is None:
                continue
            degrees = not in_meters(args[:2]) and value < 5
            found.append((value * M_PER_DEG if degrees else value, f"ST_DWithin(..., {args[2]})", degrees))

    for args, _ in calls(sql, "st_buffer"):
        if len(args) >= 2:
            value = eval_num(args[1], env)
            if value is None:
                continue
            degrees = not in_meters(args[:1]) and value < 5
            found.append((value * M_PER_DEG if degrees else value, f"ST_Buffer(..., {args[1]})", degrees))

    for fname in ("st_distance", "st_distancesphere", "st_distance_sphere"):
        for args, end in calls(sql, fname):
            tail = sql[end:end + 80]
            match = re.match(r"\s*(?:([*/])\s*([\d.]+(?:\s*[*/]\s*[\d.]+)*|\([^()]*\)))?" + COMPARE + r"([\w.]+(?:\s*[*/+-]\s*[\w.()]+)*)", tail)
            if match:
                limit = eval_num(match[4], env)
                if limit is None:
                    continue
                factor = eval_num(match[2], env) if match[1] else 1.0
                if factor in (None, 0):
                    continue
                value = limit / factor if match[1] == "*" else limit * factor if match[1] == "/" else limit
                degrees = not in_meters(args) and value < 5
                found.append((value * M_PER_DEG if degrees else value, f"{fname}(...) {match[0].strip()}", degrees))
            between = re.match(r"\s*between\s+[\d.]+\s+and\s+([\d.]+)", tail, flags=re.I)
            if between:
                found.append((float(between[1]), f"{fname}(...) BETWEEN", False))

        # alias: ST_Distance(...) AS d ... WHERE d <= 1000
        for args, end in calls(sql, fname):
            alias = re.match(r"\s*(?:::\s*\w+)?\s*(?:[*/]\s*[\d.]+\s*)?(?:as\s+)?(\w+)", sql[end:end + 60], flags=re.I)
            if not alias or alias[1].lower() in KEYWORDS:
                continue
            name = alias[1]
            scale = re.match(r"\s*(?:::\s*\w+)?\s*([*/])\s*([\d.]+)", sql[end:end + 40])
            for match in re.finditer(rf"(?<![\w])(?:\w+\.)?{re.escape(name)}\s*(<=|<)\s*([\d.]+(?:\s*[*/+-]\s*[\d.]+)*)", sql, flags=re.I):
                value = eval_num(match[2], env)
                if value is None:
                    continue
                if scale:  # alias liczony w km albo minutach
                    factor = float(scale[2])
                    value = value * factor if scale[1] == "/" else value / factor
                degrees = not in_meters(args) and value < 5
                found.append((value * M_PER_DEG if degrees else value, f"{name} {match[1]} {match[2]}", degrees))
    return found


def limits(sql: str) -> list[int]:
    return [int(value) for value in re.findall(r"\blimit\s+(\d+)", sql, flags=re.I)]


# ------------------------------------------------------------------- obszar


@cache
def admin_area(name: str, fclass: str | None) -> float | None:
    condition = "fclass = %s AND " if fclass else ""
    sql = f"SELECT max(ST_Area(geom::geography)) FROM gis_osm_adminareas_a_free WHERE {condition} name = %s"
    import psycopg

    from experiment.database import DSN

    with psycopg.connect(DSN) as connection, connection.cursor() as cursor:
        cursor.execute(sql, [fclass, name] if fclass else [name])
        row = cursor.fetchone()
    return float(row[0]) if row and row[0] else None


def area_reading(sql: str) -> tuple[float, str] | None:
    lower = sql.lower()
    # granica jednostki administracyjnej z nazwą
    if "gis_osm_adminareas_a_free" in lower:
        names = re.findall(r"name\s*(?:=|ilike|like)\s*'([^']+)'", sql, flags=re.I)
        fclasses = re.findall(r"fclass\s*=\s*'(admin_level\d+)'", sql, flags=re.I)
        city_names = {"warszawa", "płock", "radom"}
        units = [n for n in names if n.lower().strip("%") not in city_names]
        if units:
            unit = units[0].strip("%")
            fclass = next((f for f in fclasses if f != "admin_level6"), None)
            area = admin_area(unit, fclass) or admin_area(unit, None)
            if area:
                return area, f"granica „{unit}” ({fclass or 'bez fclass'})"
    for args, _ in calls(sql, "st_makeenvelope"):
        numbers = [eval_num(arg) for arg in args[:4]]
        if all(n is not None for n in numbers):
            x1, y1, x2, y2 = numbers
            width = abs(x2 - x1) * M_PER_DEG * math.cos(math.radians((y1 + y2) / 2))
            height = abs(y2 - y1) * M_PER_DEG
            return width * height, f"prostokąt {args[:4]}"
    return None


# ------------------------------------------------------------------- próg


def area_thresholds(sql: str) -> list[tuple[float, str, str]]:
    """(próg w m², kierunek '>' lub '<', opis)."""
    env = constants(sql)
    found = []
    for args, end in calls(sql, "st_area"):
        tail = sql[end:end + 80]
        match = re.match(r"\s*(?:::\s*\w+)?\s*(?:([*/])\s*([\d.e]+))?\s*(>=|>|<=|<)\s*([\d.e]+(?:\s*[*/]\s*[\d.e]+)*)", tail)
        if match:
            value = eval_num(match[4], env)
            factor = eval_num(match[2]) if match[1] else 1.0
            if value is None or not factor:
                continue
            value = value * factor if match[1] == "/" else value / factor if match[1] == "*" else value
            found.append((value, ">" if ">" in match[3] else "<", match[0].strip()))
        alias = re.match(r"\s*(?:::\s*\w+)?\s*(?:([*/])\s*([\d.e]+))?\s*\)?\s*(?:::\s*\w+)?\s*(?:as\s+)(\w+)", tail, flags=re.I)
        if alias:
            factor = eval_num(alias[2]) if alias[1] else 1.0
            for cmp in re.finditer(rf"(?<![\w])(?:\w+\.)?{re.escape(alias[3])}\s*(>=|>|<=|<)\s*([\d.e]+(?:\s*[*/]\s*[\d.e]+)*)", sql, flags=re.I):
                value = eval_num(cmp[2], env)
                if value is None or not factor:
                    continue
                value = value * factor if alias[1] == "/" else value / factor if alias[1] == "*" else value
                found.append((value, ">" if ">" in cmp[1] else "<", cmp[0]))
    return found


# --------------------------------------------------------------- ujawnienie


def discloses(uwagi: str) -> bool:
    text = uwagi.lower()
    if not text.strip():
        return False
    return bool(
        re.search(r"\d[\d\s.,]*\s*(m\b|km|metr|ha\b|hektar|m²|m2|minut|km/h)", text)
        or re.search(r"promie|przyj|założ|zakład|interpret|uznaj|rozumiem|top\s*\d|najwięks|najmniejsz", text)
    )


# ------------------------------------------------------------------ odczyt


def read(answer: dict, execution: dict | None) -> dict:
    sql = normalize(answer["sql"])
    base = {
        "variant": answer["variant"],
        "rep": answer["rep"],
        "part": answer["part"],
        "sql_sha": sql_sha(answer["sql"]),
        "ujawnienie": discloses(answer.get("uwagi", "")),
        "uwagi_puste": not answer.get("uwagi", "").strip(),
        "wiersze": execution["row_count"] if execution else None,
        "wykonane": bool(execution and execution["executed"]),
        "blad": execution["error"][:200] if execution and execution["error"] else "",
        "zrodlo": "auto",
    }
    if not sql:
        return {**base, "rodzaj": "BRAK_SQL", "wartosc": None, "jednostka": "", "opis": answer.get("uwagi", "")[:200]}

    part = answer["part"]
    variant = answer["variant"]
    if part in {"2e", "2g", "2h"} and variant not in {"22b", "22c"}:
        return {**base, **read_result(variant, execution, sql)}
    if part == "2d":
        return {**base, **read_size(sql)}
    if part == "2c":
        reading = read_distance(sql)
        area = area_reading(sql)
        if area and reading["rodzaj"] != "PROMIEŃ":
            return {**base, "rodzaj": "OBSZAR", "wartosc": round(area[0]), "jednostka": "m²", "opis": area[1], "stopnie": False}
        if reading["rodzaj"] == "PROMIEŃ":
            r = reading["wartosc"]
            return {**base, **reading, "rodzaj": "PROMIEŃ", "obszar_m2": round(math.pi * r * r)}
        return {**base, **reading}
    reading = {**base, **read_distance(sql)}
    if reading["rodzaj"] == "PROMIEŃ" and base["wykonane"] and base["wiersze"] == 0:
        found = anchor_found(sql)
        reading["punkt_odniesienia"] = {True: "znaleziony", False: "NIE znaleziony", None: "?"}[found]
    return reading


@cache
def anchor_found(sql: str) -> bool | None:
    """Pusty wynik: czy to wina promienia, czy nieznalezionego punktu odniesienia?

    Podmieniamy promień w ST_DWithin na 1e8 m. Jeśli dalej nie ma wierszy,
    zapytanie nie znalazło punktu odniesienia (np. zły fclass stacji).
    """
    from experiment.database import execute

    probe = sql
    for args, _ in calls(sql, "st_dwithin"):
        if len(args) >= 3:
            probe = probe.replace(f", {args[2]})", ", 1e8)").replace(f",{args[2]})", ",1e8)")
    if probe == sql:
        return None
    result = execute(probe)
    if not result.executed:
        return None
    return result.row_count > 0


def read_distance(sql: str) -> dict:
    radii = radius_candidates(sql)
    ks = [k for k in limits(sql) if k > 1]
    if radii:
        values = sorted({round(r, 1) for r, _, _ in radii})
        main = max(radii, key=lambda item: item[0])
        return {
            "rodzaj": "PROMIEŃ",
            "wartosc": round(main[0], 1),
            "jednostka": "m",
            "opis": "; ".join(dict.fromkeys(d for _, d, _ in radii)),
            "stopnie": any(d for _, _, d in radii),
            "limit": max(ks) if ks else None,
            "wiele_wartosci": len(values) > 1,
            "wartosci": values,
        }
    if ks:
        return {"rodzaj": "K_NAJBLIŻSZYCH", "wartosc": max(ks), "jednostka": "szt.", "opis": f"LIMIT {max(ks)}", "stopnie": False}
    return {"rodzaj": "INNY", "wartosc": None, "jednostka": "", "opis": "nie odczytano promienia ani LIMIT", "stopnie": False}


def read_size(sql: str) -> dict:
    thresholds = area_thresholds(sql)
    lower = sql.lower()
    if thresholds:
        value, direction, description = thresholds[0]
        return {"rodzaj": "PRÓG", "wartosc": round(value), "jednostka": "m²", "kierunek": direction, "opis": "; ".join(d for _, _, d in thresholds)}
    if re.search(r"percent|ntile|avg\s*\(|percentile|median|stddev", lower):
        return {"rodzaj": "WZGLĘDNY", "wartosc": None, "jednostka": "", "opis": "próg względny (średnia/percentyl/ntile)"}
    ks = [k for k in limits(sql) if k > 1]
    if ks and "st_area" in lower:
        return {"rodzaj": "K_SKRAJNYCH", "wartosc": max(ks), "jednostka": "szt.", "opis": f"ORDER BY powierzchnia LIMIT {max(ks)}"}
    return {"rodzaj": "INNY", "wartosc": None, "jednostka": "", "opis": "nie odczytano progu"}


def subqueries(sql: str) -> list[str]:
    """Podzapytania w FROM i CTE: `(SELECT ...) alias` oraz `nazwa AS (SELECT ...)`."""
    found = []
    for match in re.finditer(r"\(\s*select\b", sql, flags=re.I):
        depth, i = 0, match.start()
        while i < len(sql):
            if sql[i] == "(":
                depth += 1
            elif sql[i] == ")":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        inner = sql[match.start() + 1:i]
        before = sql[:match.start()].rstrip().lower()
        after = sql[i + 1:i + 40]
        is_cte = re.search(r"\b\w+\s+as$", before) is not None
        is_derived = re.match(r"\s*(as\s+)?\w+\s*(,|$|where|cross|join|\))", after, flags=re.I) and re.search(r"(from|,|join)$", before)
        is_scalar = after.lstrip().startswith("::") or re.search(r"st_distance\($", before) is not None
        if (is_cte or is_derived or is_scalar):
            found.append(inner)
    return found


def diagnose_empty(sql: str) -> str:
    """Które podzapytanie nic nie znajduje: obiekt z pytania czy PKiN?"""
    parts = []
    for inner in subqueries(sql):
        # podzapytania zależne od innych CTE pomijamy
        result = execute(f"SELECT count(*) FROM ({inner}) AS diag")
        if not result.executed:
            continue
        count = result.rows[0][0]
        if count == 0:
            what = "PKiN" if re.search(r"kultury|pa.ac", inner, flags=re.I) else "obiekt z pytania"
            fclass = re.findall(r"fclass\s*(?:=|in)\s*\(?([^)]*?)\)?\s*(?:and|order|limit|$)", inner, flags=re.I)
            table = re.search(r"from\s+(gis_osm_\w+)", inner, flags=re.I)
            name = re.search(r"name\s+i?like\s+'([^']+)'", inner, flags=re.I)
            parts.append(
                f"0 wierszy: {what} ({table[1] if table else '?'}"
                f"{', fclass ' + fclass[0].strip() if fclass else ''}{', name ' + name[1] if name else ''})"
            )
    return "; ".join(parts) or "nie ustalono"


def read_result(variant: str, execution: dict | None, sql: str = "") -> dict:
    if not execution or not execution["executed"]:
        return {"rodzaj": "BŁĄD_WYKONANIA", "wartosc": None, "jednostka": "", "opis": (execution or {}).get("error", "")[:200]}
    rows = execution["rows"]
    if not rows:
        return {"rodzaj": "PUSTY_WYNIK", "wartosc": None, "jednostka": "", "opis": diagnose_empty(sql) if sql else "0 wierszy", **classify_result(variant, None, [])}
    numbers = [cell for cell in rows[0] if isinstance(cell, (int, float)) and not isinstance(cell, bool)]
    texts = [cell for cell in rows[0] if isinstance(cell, str)]
    value = numbers[0] if numbers else None
    kind = "LICZBA" if variant == "22a" else "ODLEGŁOŚĆ"
    if value is None and all(cell is None for cell in rows[0]):
        return {"rodzaj": "PUSTY_WYNIK", "wartosc": None, "jednostka": "", "opis": "wynik NULL; " + (diagnose_empty(sql) if sql else ""), **classify_result(variant, None, [])}
    if value is None:
        return {"rodzaj": "INNY", "wartosc": None, "jednostka": "", "opis": f"brak liczby w wyniku: {rows[0]}"[:200], **classify_result(variant, None, texts)}
    # odległość podana w km zamiast w m
    if kind == "ODLEGŁOŚĆ" and 0 < value < 200 and any("km" in c.lower() for c in execution["columns"]):
        value = value * 1000
    return {
        "rodzaj": kind,
        "wartosc": round(float(value), 1),
        "jednostka": "szt." if kind == "LICZBA" else "m",
        "opis": f"pierwszy wiersz: {rows[0]}"[:200],
        "wiele_wierszy": len(rows) > 1,
        **classify_result(variant, float(value), texts),
        # Identyfikacja konkretnego obiektu (identify.py) ma pierwszeństwo przed
        # dopasowaniem do listy kandydatów; gdy nic nie pasuje, zostaje lista.
        **(identify(variant, float(value)) or {"identyfikacja": "lista kandydatów"}),
    }


# ----------------------------------------------------------------- całość


def load_corrections(path: Path = CORRECTIONS_PATH) -> dict[str, dict]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {key: value for key, value in data.items() if not key.startswith("_")}


def extract_all() -> list[dict]:
    answers = AnswerStore().good()
    executions = ExecutionStore().by_key()
    corrections = load_corrections()
    rows = []
    for answer in sorted(answers, key=lambda a: (_order(a["variant"]), a["rep"])):
        execution = executions.get((answer["variant"], answer["rep"], sql_sha(answer["sql"])))
        row = read(answer, execution)
        key = f"{answer['variant']}#{answer['rep']}"
        if key in corrections:
            fix = corrections[key]
            if fix.get("sql_sha") and fix["sql_sha"] != row["sql_sha"]:
                raise ValueError(f"Korekta {key} dotyczy innego SQL (sql_sha się nie zgadza)")
            row = {**row, **{k: v for k, v in fix.items() if k != "sql_sha"}, "zrodlo": "korekta"}
        rows.append(row)
    EXTRACTED_PATH.parent.mkdir(parents=True, exist_ok=True)
    EXTRACTED_PATH.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8"
    )
    return rows


def load_extracted() -> list[dict]:
    if not EXTRACTED_PATH.exists():
        return []
    return [json.loads(line) for line in EXTRACTED_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]


def _order(code: str) -> tuple[int, str]:
    number = re.match(r"\d+", code)[0]
    return (int(number), code[len(number):])
