"""Kandydaci i wartości wzorcowe dla części 2e i 2g (pytania.md, "Kandydaci w bazie").

Wynik pytania o odległość przypisujemy do najbliższego kandydata, jeśli różni
się od niego najwyżej o max(40 m, 4%). Inaczej "nierozpoznany" i ręczny przegląd.

Ocena:
    poprawny      właściwy obiekt
    dopuszczalny  obiekt, który też można uznać za odpowiedź (np. inna syrena)
    pomyłka       inny obiekt, ale w pobliżu (do kilku km)
    duża_pomyłka  obiekt w innym mieście albo zupełnie inny (np. rzeźba przy PKiN)
"""

# (etykieta, wartość, ocena)
Candidate = tuple[str, float, str]

CANDIDATES: dict[str, list[Candidate]] = {
    "13": [
        ("obrys Łazienek → punkt PKiN", 2194, "poprawny"),
        ("obrys Łazienek → poligon PKiN", 2041, "poprawny"),
        ("środek Łazienek → PKiN", 2775, "poprawny"),
        ("środek Łazienek → obrys poligonu PKiN", 2619, "poprawny"),
        ("Pałac na Wyspie → PKiN", 2707, "dopuszczalny"),
        ("przysiółek Łazienki (pow. przysuski)", 98697, "duża_pomyłka"),
    ],
    "14": [
        ("między obrysami parków", 754, "poprawny"),
        ("między środkami parków", 2195, "poprawny"),
        ("środek Pola Mokotowskiego → obrys Łazienek", 1734, "poprawny"),
    ],
    "15": [
        ("pomnik Chopina w Łazienkach → punkt PKiN", 2416, "poprawny"),
        ("pomnik Chopina w Łazienkach → poligon PKiN", 2264, "poprawny"),
        ("„Pomnik Fryderyka Chopina” w Radomiu → punkt PKiN", 93225, "duża_pomyłka"),
        ("„Pomnik Fryderyka Chopina” w Radomiu → poligon PKiN", 93072, "duża_pomyłka"),
        ("„Pomnik Fryderka Chopina” (pow. sochaczewski)", 51727, "duża_pomyłka"),
        ("„Pomnik Fryderka Chopina” → poligon PKiN", 51582, "duża_pomyłka"),
        ("„Fortepian Chopina” (memorial, ok. 1 km od PKiN) → środek poligonu PKiN", 1032, "pomyłka"),
    ],
    "16": [
        ("Syrenka na Rynku Starego Miasta → punkt PKiN", 2039, "poprawny"),
        ("Syrenka na Rynku → poligon PKiN", 1893, "poprawny"),
        ("Syrena nad Wisłą → punkt PKiN", 1997, "poprawny"),
        ("Syrena nad Wisłą → poligon PKiN", 1900, "poprawny"),
        ("rzeźba „Syrenka” (artwork, 0,8 km od PKiN)", 837, "pomyłka"),
        ("rzeźba „Syrenka” → poligon PKiN", 706, "pomyłka"),
        ("„Syrenska Warzawska” (Wola)", 3980, "pomyłka"),
        ("„Syrena” (artwork, poza Warszawą)", 57513, "duża_pomyłka"),
        ("„Syrenka Białobrzeska”", 64318, "duża_pomyłka"),
        ("apteka „Syrenka” (pierwszy punkt o nazwie %Syrenk% bez warunku na fclass)", 1935, "duża_pomyłka"),
        ("środek wszystkich obiektów %Syrenk% w województwie (ST_Collect)", 31755, "duża_pomyłka"),
    ],
    "17": [
        ("pomnik Kopernika, Krakowskie Przedmieście → punkt PKiN", 1067, "poprawny"),
        ("pomnik Kopernika → poligon PKiN", 949, "poprawny"),
        ("pomnik Kopernika → środek budynku PKiN", 1090, "poprawny"),
        ("rzeźba Kopernika przy PKiN → punkt PKiN", 52, "duża_pomyłka"),
        ("rzeźba Kopernika przy PKiN → poligon PKiN", 4, "duża_pomyłka"),
        ("rzeźba Kopernika przy PKiN (0 m, wewnątrz poligonu)", 0, "duża_pomyłka"),
        ("Centrum Nauki Kopernik → punkt PKiN", 1860, "pomyłka"),
        ("Centrum Nauki Kopernik → poligon PKiN", 1746, "pomyłka"),
    ],
    "18": [
        ("Kolumna Zygmunta → punkt PKiN", 1781, "poprawny"),
        ("Kolumna Zygmunta → poligon PKiN", 1636, "poprawny"),
    ],
    "19": [
        ("palma → punkt PKiN", 998, "poprawny"),
        ("palma → poligon PKiN", 881, "poprawny"),
        ("palma → środek poligonu PKiN", 1018, "poprawny"),
        ("środek wszystkich punktów %palma% (ST_Collect)", 3889, "duża_pomyłka"),
    ],
    "20": [
        ("Mały Powstaniec → punkt PKiN", 1956, "poprawny"),
        ("Mały Powstaniec → poligon PKiN", 1809, "poprawny"),
        ("Mały Powstaniec → środek poligonu PKiN", 1969, "poprawny"),
    ],
    "21a": [
        ("Centrum → punkt PKiN", 283, "poprawny"),
        ("Centrum → poligon PKiN", 147, "poprawny"),
        ("Centrum → punkt wewnątrz poligonu PKiN", 311, "poprawny"),
    ],
    "21b": [
        ("Politechnika ← obrys Łazienek", 797, "poprawny"),
        ("Politechnika ← środek Łazienek", 1387, "poprawny"),
    ],
    "22a": [
        ("stacje metra (tory subway)", 72, "poprawny"),
        ("wszystkie railway_station w Warszawie", 111, "pomyłka"),
        ("wszystkie railway_station w województwie", 115, "pomyłka"),
    ],
}

# Nazwy stacji, które w 21a/21b oznaczają trafienie albo pomyłkę.
STATION_NAMES = {
    "21a": {"Centrum": "poprawny", "Warszawa Śródmieście": "pomyłka", "Świętokrzyska": "pomyłka"},
    "21b": {"Politechnika": "poprawny"},
}


# Część 2g: te same pytania co w 2e, inny kontekst. Wariant 2g → odpowiednik w 2e.
BASE_2G = {
    "30": "15a", "31": "15b", "32": "16a", "33": "16b", "34": "17a",
    "35": "18", "36": "19", "37": "20", "38": "13a", "39": "21a",
}


def base_variant(variant: str) -> str:
    return BASE_2G.get(variant, variant)


def _key(variant: str) -> str:
    variant = base_variant(variant)
    return variant if variant in CANDIDATES else variant.rstrip("abc")


def classify_result(variant: str, value: float | None, texts: list[str]) -> dict:
    key = _key(variant)
    if key not in CANDIDATES:
        return {}
    if value is None:
        return {"kandydat": "brak wyniku", "ocena_obiektu": "pusty"}

    variant = base_variant(variant)
    if variant in STATION_NAMES:
        for text in texts:
            for name, verdict in STATION_NAMES[variant].items():
                if text.strip().lower() == name.lower():
                    match = _nearest(key, value)
                    label = match[0] if match else f"{value:.0f} m"
                    return {"kandydat": f"{name} ({label})", "ocena_obiektu": verdict}
        if texts:
            return {"kandydat": f"stacja {texts[0]}", "ocena_obiektu": "pomyłka"}

    match = _nearest(key, value)
    if match is None:
        return {"kandydat": "nierozpoznany", "ocena_obiektu": "nierozpoznany"}
    return {"kandydat": match[0], "ocena_obiektu": match[2], "roznica_m": round(abs(match[1] - value), 1)}


def _nearest(key: str, value: float) -> Candidate | None:
    best = min(CANDIDATES[key], key=lambda c: abs(c[1] - value))
    tolerance = 3 if key == "22a" else max(40.0, 0.04 * best[1])
    return best if abs(best[1] - value) <= tolerance else None
