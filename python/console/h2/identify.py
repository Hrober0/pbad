"""Identyfikacja obiektu wybranego przez model w częściach 2e i 2g.

Zamiast dopasowywać wynik do krótkiej listy kandydatów z tolerancją, liczymy
odległość do PKiN dla **każdego** obiektu w bazie, którego nazwa zawiera rdzeń
(np. „chopin”), w każdej kombinacji geometrii:
- obiekt: geometria, środek (`ST_Centroid`), punkt wewnątrz (`ST_PointOnSurface`),
- PKiN: punkt, poligon, środek poligonu, punkt wewnątrz poligonu, obrys budynku, środek budynku.

Wynik modelu przypisujemy do obiektu, dla którego któraś kombinacja daje tę samą
odległość z dokładnością do 2 m. Ocena wynika z tego, który to obiekt (osm_id)
i gdzie leży, a nie z samej liczby.

Wyniki, których nie da się przypisać do jednego obiektu (np. środek ciężkości
wielu obiektów), zostają przy ocenie z references.py.
"""

from functools import cache

import psycopg

from experiment.database import DSN

from .references import base_variant

TOLERANCE_M = 2.0

STEMS = {
    "13": "%azienk%",
    "15": "%chopin%",
    "16": "%syren%",
    "17": "%kopernik%",
    "18": "%zygmunt%",
    "19": "%palm%",
    "20": "%powsta%",
}

# osm_id właściwych obiektów; ocena zależy od wariantu pytania
CORRECT: dict[str, dict[str, str]] = {
    "13a": {"19860651": "poprawny", "1325609735": "dopuszczalny"},
    "13b": {"19860651": "poprawny", "1325609735": "dopuszczalny"},
    "15a": {"1448330230": "poprawny"},
    "15b": {"1448330230": "poprawny"},
    # 16a „Syrenka Warszawska”: obie słynne syreny są dobrą odpowiedzią
    "16a": {"404150162": "poprawny", "432808623": "poprawny"},
    # 16b „pomnik Syrenki nad Wisłą”: tylko syrena na bulwarach; ta z Rynku to inny obiekt
    "16b": {"432808623": "poprawny"},
    "17a": {"282661680": "poprawny"},
    "17b": {"282661680": "poprawny"},
    "18": {"238615551": "poprawny"},
    "19": {"1795659661": "poprawny"},
    "20": {"448025917": "poprawny"},
}

LANDMARK_FCLASS = {
    "monument", "memorial", "artwork", "attraction", "castle", "museum", "park",
    "fountain", "viewpoint", "tourist_info", "bench", "ruins", "archaeological",
}

TABLES = [
    "gis_osm_pois_free", "gis_osm_pois_a_free", "gis_osm_buildings_a_free",
    "gis_osm_landuse_a_free", "gis_osm_transport_free", "gis_osm_transport_a_free",
    "gis_osm_places_free", "gis_osm_places_a_free", "gis_osm_natural_free",
]

PKIN_VARIANTS = """
    SELECT 'punkt' AS pv, geom FROM gis_osm_pois_free WHERE name = 'Pałac Kultury i Nauki'
    UNION ALL SELECT 'poligon', geom FROM gis_osm_pois_a_free WHERE name = 'Pałac Kultury i Nauki' AND fclass = 'attraction'
    UNION ALL SELECT 'środek poligonu', ST_Centroid(geom) FROM gis_osm_pois_a_free WHERE name = 'Pałac Kultury i Nauki' AND fclass = 'attraction'
    UNION ALL SELECT 'punkt w poligonie', ST_PointOnSurface(geom) FROM gis_osm_pois_a_free WHERE name = 'Pałac Kultury i Nauki' AND fclass = 'attraction'
    UNION ALL (SELECT 'budynek', geom FROM gis_osm_buildings_a_free WHERE name ILIKE '%%Pałac Kultury i Nauki%%' ORDER BY ST_Area(geom) DESC LIMIT 1)
    UNION ALL (SELECT 'środek budynku', ST_Centroid(geom) FROM gis_osm_buildings_a_free WHERE name ILIKE '%%Pałac Kultury i Nauki%%' ORDER BY ST_Area(geom) DESC LIMIT 1)
"""


@cache
def distances(stem: str) -> list[tuple]:
    objects = " UNION ALL ".join(
        f"SELECT '{t.replace('gis_osm_', '').replace('_free', '')}' AS tbl, osm_id, fclass, name, geom FROM {t} WHERE name ILIKE %(stem)s"
        for t in TABLES
    )
    sql = f"""
        WITH o AS ({objects}),
        ov AS (
            SELECT tbl, osm_id, fclass, name, 'geometria' AS gv, geom FROM o
            UNION ALL SELECT tbl, osm_id, fclass, name, 'środek', ST_Centroid(geom) FROM o
            UNION ALL SELECT tbl, osm_id, fclass, name, 'punkt wewnątrz', ST_PointOnSurface(geom) FROM o
        ),
        pk AS ({PKIN_VARIANTS})
        SELECT ov.tbl, ov.osm_id, ov.fclass, ov.name, ov.gv, pk.pv,
               ST_Distance(ov.geom::geography, pk.geom::geography) AS d,
               (SELECT a.name FROM gis_osm_adminareas_a_free a
                 WHERE a.fclass = 'admin_level6' AND ST_Intersects(a.geom, ST_PointOnSurface(ov.geom)) LIMIT 1) AS powiat
        FROM ov CROSS JOIN pk
    """
    with psycopg.connect(DSN) as connection, connection.cursor() as cursor:
        cursor.execute(sql, {"stem": stem})
        return cursor.fetchall()


def identify(variant: str, value: float) -> dict | None:
    base = base_variant(variant)
    stem = STEMS.get(base.rstrip("ab"))
    if stem is None or value is None:
        return None
    matches = [row for row in distances(stem) if abs(row[6] - value) <= TOLERANCE_M]
    if not matches:
        return None
    # Decyduje najbliższe dopasowanie. Inne obiekty w granicy 2 m to zwykle obiekty
    # stojące tuż obok (np. tablica informacyjna przy pomniku) albo przypadkowo
    # leżące w tej samej odległości od PKiN; zapisujemy je tylko w opisie.
    correct = CORRECT.get(base, {})
    best_diff = min(abs(m[6] - value) for m in matches)
    best = [m for m in matches if abs(m[6] - value) - best_diff < 0.01]
    best.sort(key=lambda m: m[1] not in correct)  # przy idealnym remisie wygrywa właściwy obiekt
    tbl, osm_id, fclass, name, gv, pv, d, powiat = best[0]
    objects = {(m[1], m[3]) for m in matches}
    if osm_id in correct:
        verdict = correct[osm_id]
    elif powiat != "Warszawa":
        verdict = "duża_pomyłka"
    elif fclass in LANDMARK_FCLASS:
        verdict = "pomyłka"
    else:
        verdict = "duża_pomyłka"  # zupełnie inny rodzaj obiektu, np. apteka
    other_names = sorted({n for oid, n in objects if oid != osm_id})
    others = f" (w granicy 2 m także: {', '.join(other_names)[:80]})" if other_names else ""
    return {
        "kandydat": f"{name} [{tbl}, {fclass}, {powiat}] {gv} → PKiN {pv}{others}",
        "ocena_obiektu": verdict,
        "osm_id": osm_id,
        "roznica_m": round(abs(d - value), 1),
        "identyfikacja": "obiekt",
    }
