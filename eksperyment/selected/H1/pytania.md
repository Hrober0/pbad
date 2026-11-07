# H1

## Kategorie zapytań

Kategorie Z, N, J, A pochodzą z NALSpatial (praca 6 w przeglądzie literatury). Kategorię M dodaliśmy na podstawie GS-SQL (praca 5), bo funkcje pomiarowe są osobną, łatwiejszą grupą.

| Kod | Kategoria | Typowe funkcje PostGIS |
|---|---|---|
| Z | Zakresowe (obiekty w odległości / wewnątrz obszaru) | `ST_DWithin`, `ST_Intersects` |
| N | Najbliżsi sąsiedzi | `ORDER BY geom <-> ...`, `ST_Distance` |
| J | Złączenia przestrzenne (relacje między dwiema warstwami) | `JOIN ... ON ST_DWithin / ST_Intersects` |
| A | Agregacje przestrzenne | `COUNT`, `GROUP BY`, `HAVING` + funkcje przestrzenne |
| M | Pomiary geometrii | `ST_Area`, `ST_Length`, `ST_Perimeter`, `ST_Distance` |

## Pytania

20 pytań × 4 poziomy kontekstu (K0–K3) × 3 powtórzenia = 240 wywołań.

**Przy każdej próbie zapisujemy:** czy zapytanie się wykonało, czy wynik zgadza się z wzorcem, rodzaj błędu.

| Kod | Pytanie | Kolumny kluczowe | Na co patrzeć w SQL |
|---|---|---|---|
| Z01 | Ile aptek jest w promieniu 500 metrów od Pałacu Kultury i Nauki? | liczba | współrzędne z pamięci; obie tabele `pois` |
| Z02 | Wymień nazwy kawiarni w promieniu 300 metrów od Dworca Centralnego. | `name` | nazwa „Warszawa Centralna” |
| Z05 | Ile aptek jest w promieniu kilometra od Skweru Jolanty Brzeskiej? | liczba | czy znalazł obiekt w bazie |
| Z07 | Ile supermarketów jest w Warszawie? | liczba | zawężenie do granicy Warszawy; `name <> ''` |
| N01 | Jaki szpital jest najbliżej Pałacu Kultury i Nauki? | `name` | obie tabele `pois` (7 punktów, 37 poligonów) |
| N03 | Jak daleko w metrach jest najbliższy urząd pocztowy od Dworca Centralnego i jak się nazywa? | `name`, odległość | `::geography`, nie stopnie |
| N04 | Wymień 5 aptek położonych najbliżej Zamku Królewskiego. | `name` w kolejności | kolejność; obie tabele `pois` |
| N07 | Wymień 3 przystanki autobusowe najbliższe pomnikowi pamięci Konstantego Juliana Ordona i podaj, jak daleko są w metrach. | `name` w kolejności, odległość | nazwa w bazie: „Pamięci Konstantego Juliana Ordona” |
| J01 | Które szkoły w Warszawie mają w promieniu 300 metrów co najmniej jeden fast food? | `name` | obie tabele dla obu warstw; `name <> ''` |
| J02 | Ile przedszkoli w Warszawie nie ma żadnego parku w promieniu 500 metrów? | liczba | `NOT EXISTS`; parki tylko z `landuse` |
| J03 | Przez które parki w Warszawie przepływa Wisła albo które parki do niej przylegają? | `name` | Wisła jako wiele odcinków; parki tylko z `landuse` |
| J08 | Wymień nazwy mostów samochodowych na Wiśle w Warszawie. | `name` | wartość `fclass` dla mostu |
| A01 | Ile jest restauracji, kawiarni, fast foodów, pubów i barów w promieniu kilometra od Pałacu Kultury i Nauki? Podaj liczbę dla każdego typu osobno. | typ, liczba | wszystkie 5 wartości `fclass`; `GROUP BY` |
| A03 | Które 5 stacji kolejowych w Warszawie ma najwięcej restauracji w promieniu 500 metrów i ile ich jest? | `name` w kolejności, liczba | `railway_station`, nie `railway_halt` |
| A07 | Ile szkół, a ile przedszkoli jest w promieniu kilometra od Placu Bociani Zakątek? | typ, liczba | czy znalazł obiekt w bazie |
| A08 | Ile wypożyczalni rowerów w Warszawie jest w promieniu 300 metrów od stacji kolejowej, a ile dalej? | kategoria, liczba | obie tabele (129 punktów, 223 poligony) |
| M02 | Ile kilometrów ma ulica Marszałkowska w Warszawie? | długość | zawężenie do Warszawy (bez niego 9,9 km); `ST_Intersection` |
| M03 | Jaka jest odległość w linii prostej w metrach między Pałacem Kultury i Nauki a Stadionem Narodowym? | odległość | nazwa „PGE Narodowy”; nie stacja o tej nazwie |
| M05 | Ile kilometrów długości ma Wisła na odcinku w granicach Warszawy? | długość | suma odcinków; `ST_Intersection` |
| M07 | Jaka jest odległość w linii prostej w kilometrach między Parkiem Planeta Ursus a Placem Bociani Zakątek? | odległość | oba obiekty z bazy |

## Do uzupełnienia: tokeny i trafność

Liczbę tokenów bierzemy z `usage.input_tokens` w odpowiedzi API. Obejmuje ona cały prompt: instrukcję, kontekst i pytanie. Zapisujemy ją przy każdym wywołaniu, a tu wpisujemy średnią dla poziomu. Między pytaniami różni się tylko długość samego pytania, czyli kilkadziesiąt tokenów.

| Poziom | Tokeny promptu (średnia) | Trafność |
|---|---|---|
| K0 | — | — |
| K1 | — | — |
| K2 | — | — |
| K3 | — | — |

## Do uzupełnienia: zapytania wzorcowe

Dla każdego pytania potrzebujemy zapytania wzorcowego i jego wyniku z bazy. Bez tego nie ma z czym porównać odpowiedzi modelu.

| Kod | Wzorzec | Wynik | Uwagi |
|---|---|---|---|
| Z01 | — | — | |
| Z02 | — | — | |
| Z05 | — | — | |
| Z07 | — | — | |
| N01 | — | — | |
| N03 | — | — | |
| N04 | — | — | |
| N07 | — | — | |
| J01 | — | — | |
| J02 | — | — | |
| J03 | — | — | |
| J08 | — | — | |
| A01 | — | — | |
| A03 | — | — | |
| A07 | — | — | |
| A08 | — | — | |
| M02 | — | — | |
| M03 | — | — | |
| M05 | — | — | |
| M07 | — | — | |
