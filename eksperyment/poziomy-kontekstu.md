# Poziomy kontekstu bazy danych (K0–K3)

Opis tego, co model dostaje w prompcie na każdym poziomie kontekstu. Poziom kontekstu to pierwszy czynnik eksperymentu. Drugim jest precyzja pytania (P1–P3), opisana w [pytania-testowe.md](pytania-testowe.md).

## Zasady budowy poziomów

1. **Poziomy są kumulatywne:** każdy zawiera całą treść poprzedniego i dodaje jedną nową rodzajowo porcję informacji. Dzięki temu różnicę wyników między sąsiednimi poziomami można przypisać konkretnej dodanej informacji.
2. **K2 opisuje, K3 instruuje.** K2 zawiera wyłącznie fakty o danych („co jest w bazie”), np. „brak nazwy zapisano jako pusty napis”. K3 dodaje wskazówki, jak pisać zapytania („co z tym zrobić”), np. „aby pominąć obiekty bez nazwy, użyj `name <> ''`”, oraz przykłady. To rozdzielenie pozwala sprawdzić, czy modelowi wystarczy wiedza o danych, czy potrzebuje gotowych wzorców. Ma to znaczenie dla hipotezy H1.
3. **Treść jest generowana z bazy, jeśli się da.** Nazwy kolumn, typy, DDL i listy wartości `fclass` pobieramy zapytaniami do bazy. Ręcznie piszemy tylko opisy (K2) oraz wskazówki i przykłady (K3). Dzięki temu łatwo odtworzyć eksperyment na innym regionie.
4. **Kontekst obejmuje 20 tabel `public.gis_osm_*`.** Tabele rozszerzenia `tiger`, które dodaje obraz `postgis/postgis`, pomijamy na każdym poziomie.
5. **Prompt jest jednym wywołaniem bez historii.** Model ma jedną próbę: nie dostaje błędów wykonania i nie poprawia zapytania. Pętla poprawek to osobny temat (prace 2 i 4 w przeglądzie literatury) i świadomie go nie badamy.

## Część wspólna dla wszystkich poziomów

Każdy prompt zaczyna się tą samą instrukcją zadania. Zawiera ona konwencje oceny, a nie wiedzę o danych, więc nie może się zmieniać między poziomami. Inaczej pytanie P2 typu „ile aptek…” miałoby ukryte kryterium, którego model nie mógłby znać.

```text
Jesteś asystentem, który tłumaczy pytania w języku polskim na zapytania SQL
dla bazy PostgreSQL 18 z rozszerzeniem PostGIS 3.6.

Zwróć dokładnie jedno zapytanie SELECT w bloku ```sql ... ```, bez dodatkowych wyjaśnień.
Nie modyfikuj danych.

Obowiązujące konwencje:
1. Obiekt należy do obszaru, jeśli się z nim przecina. W pytaniach o długość lub
   powierzchnię „w granicach” obszaru licz tylko część leżącą wewnątrz obszaru.
2. Każdy obiekt licz tylko raz.
3. Pomijaj obiekty bez nazwy, zarówno w wynikach, jak i przy liczeniu.
4. Odległości podawaj w metrach, długości w metrach lub kilometrach, powierzchnie
   w metrach kwadratowych lub hektarach, zgodnie z pytaniem.

Opis bazy danych:
<KONTEKST K0 / K1 / K2 / K3>

Pytanie: <PYTANIE>
```

Konwencja 4 też jest wspólna, bo jednostka wyniku wynika z pytania. Sposób jej uzyskania, czyli rzutowanie na `geography`, pojawia się dopiero w K3.

---

## K0: same nazwy tabel i kolumn

**Co zawiera:** listę 20 tabel z nazwami kolumn. Bez typów, bez opisów, bez wartości.

**Przykład (fragment):**

```text
gis_osm_pois_free(fid, osm_id, code, fclass, name, geom)
gis_osm_pois_a_free(fid, osm_id, code, fclass, name, geom)
gis_osm_transport_free(fid, osm_id, code, fclass, name, geom)
gis_osm_roads_free(fid, osm_id, code, fclass, name, ref, oneway, maxspeed, layer, bridge, tunnel, geom)
gis_osm_adminareas_a_free(fid, osm_id, code, fclass, name, geom)
...
```

**Czego model nie wie:**
- jakiego typu jest `geom` (punkt, linia, poligon), w jakim jest układzie współrzędnych i jakie wartości przyjmuje `fclass`,
- że `_a` w nazwie tabeli oznacza poligony.

Model musi to zgadywać z nazw i wiedzy ogólnej o OSM/Geofabrik. Nazwy tabel Geofabrik są dość popularne, więc część modeli może je znać.

**Rola w eksperymencie:** punkt odniesienia, który odpowiada minimalnemu opisowi schematu w literaturze, czyli reprezentacji „Basic Prompt” u DAIL-SQL (praca 9).

**Rozmiar:** ok. 0,5 tys. tokenów.

---

## K1: DDL z typami

**Co zawiera:** K0 zapisane jako `CREATE TABLE` z typami kolumn, kluczem głównym i typem geometrii z SRID. DDL generujemy z bazy. Bez indeksów i bez komentarzy.

**Przykład (fragment):**

```sql
CREATE TABLE gis_osm_pois_free (
    fid integer PRIMARY KEY,
    osm_id varchar(12),
    code integer,
    fclass varchar(28),
    name varchar(100),
    geom geometry(Point, 4326)
);

CREATE TABLE gis_osm_pois_a_free (
    fid integer PRIMARY KEY,
    osm_id varchar(12),
    code integer,
    fclass varchar(28),
    name varchar(100),
    geom geometry(MultiPolygon, 4326)
);
```

**Co model zyskuje względem K0:**
- wie, które tabele zawierają punkty, linie i poligony,
- widzi SRID 4326, więc może się domyślić, że odległość w metrach wymaga przeliczenia.

**Czego nadal nie wie:** jakie wartości przyjmuje `fclass`, że ten sam typ obiektu bywa w dwóch tabelach, gdzie jest granica Warszawy i że brak nazwy to `''`.

**Rola w eksperymencie:** format, który w DAIL-SQL dawał najlepsze wyniki („Code Representation”). W naszej bazie nie ma kluczy obcych, więc ta część przewagi DDL odpada.

**Rozmiar:** ok. 1,5 tys. tokenów.

### Wariant opcjonalny K1-md: schemat jako tabela markdown

Ta sama informacja co w K1, ale zapisana jako tabele markdown. Ten wariant porównujemy tylko z K1, aby osobno sprawdzić, czy wynik zależy od formatu zapisu schematu (pierwsza część H1). Jeśli zabraknie czasu, można go pominąć bez szkody dla reszty eksperymentu.

```markdown
### gis_osm_pois_free
| kolumna | typ |
|---|---|
| fid | integer (klucz główny) |
| osm_id | varchar(12) |
| fclass | varchar(28) |
| name | varchar(100) |
| geom | geometry(Point, 4326) |
```

---

## K2: K1 + wiedza o danych

**Co zawiera:** K1 oraz trzy rodzaje informacji. Wszystkie mają charakter opisowy: mówią, co jest w bazie, ale nie mówią, jak pisać zapytania.

### 1. Opis tabel i kolumn

Opis piszemy ręcznie na podstawie dokumentacji Geofabrik. Jedno zdanie na tabelę i jedno na każdą kolumnę, która nie jest oczywista. Fragment:

```text
gis_osm_pois_free: punkty usług i obiektów użyteczności (sklepy, gastronomia, szkoły, ...).
gis_osm_pois_a_free: te same rodzaje obiektów, ale zapisane jako poligony (np. budynek szkoły).
gis_osm_adminareas_a_free: granice administracyjne; fclass określa poziom (admin_level4 = województwo,
    admin_level6 = powiat / miasto na prawach powiatu, admin_level9 = dzielnica Warszawy, ...).
gis_osm_landuse_a_free: użytkowanie terenu (parki, lasy, cmentarze, tereny mieszkaniowe, ...).

Kolumny wspólne:
- osm_id: identyfikator obiektu w OpenStreetMap,
- code: liczbowy kod typu obiektu (odpowiada fclass),
- fclass: typ obiektu (np. 'pharmacy', 'tram_stop', 'park'),
- name: nazwa obiektu.
```

### 2. Lista wartości `fclass` dla każdej tabeli

Listę generujemy z bazy (`SELECT DISTINCT fclass`). W bazie jest ok. 440 wartości, najwięcej w `pois` i `pois_a` (po ok. 135). Fragment:

```text
gis_osm_transport_free.fclass: airfield, airport, bus_station, bus_stop, ferry_terminal,
    helipad, railway_halt, railway_station, taxi, tram_stop
gis_osm_pofw_free.fclass: buddhist, christian, christian_catholic, christian_evangelical, ...
gis_osm_pois_free.fclass: archaeological, arts_centre, artwork, atm, attraction, bakery, bank, ...
```

### 3. Fakty o danych

Fakty pochodzą z „Ustaleń dotyczących danych” w [pytania-testowe.md](pytania-testowe.md):

```text
- Dane obejmują całe województwo mazowieckie, a nie tylko Warszawę.
- Granica Warszawy: gis_osm_adminareas_a_free, fclass = 'admin_level6', name = 'Warszawa'.
  Dzielnice Warszawy mają fclass = 'admin_level9'.
- Ten sam typ obiektu (np. szpital, szkoła, plac zabaw) występuje zarówno jako punkt
  w gis_osm_pois_free, jak i jako poligon w gis_osm_pois_a_free.
- Parki są zapisane w gis_osm_landuse_a_free i powtórzone (z tym samym osm_id)
  w gis_osm_pois_a_free.
- Obiekty bez nazwy mają w kolumnie name pusty napis '', a nie NULL.
- Nazwy ulic i obiektów nie są unikalne w województwie (np. ulica Marszałkowska
  występuje w kilku miejscowościach).
- Dworzec Centralny jest zapisany jako 'Warszawa Centralna' (fclass = 'railway_station').
  Stadion Narodowy jest zapisany jako 'PGE Narodowy' (gis_osm_pois_a_free, fclass = 'stadium').
- Większość kościołów ma fclass = 'christian', a nie 'christian_catholic'.
```

**Uwaga do dwóch ostatnich faktów:** podają one nazwy z bazy dla dwóch obiektów z pytań testowych. To uczciwe, bo prawdziwy system też miałby słownik takich nazw, ale ułatwia znane obiekty w porównaniu z [MZ]. Do decyzji: można je usunąć i zostawić modelowi dopasowanie nazwy, np. przez `ILIKE`.

**Co model zyskuje względem K1:**
- zna wartości `fclass`, więc wie, że apteka to `'pharmacy'`, a kościół to `'christian'`,
- wie o rozdzieleniu punktów i poligonów, o granicy Warszawy i o pustych nazwach,
- wie o obiektach, których nazwy w bazie różnią się od potocznych.

**Rola w eksperymencie:** główny poziom dla hipotezy H1. Jeśli skok K1→K2 jest większy niż różnica K1 vs K1-md, to wiedza o danych waży więcej niż format schematu.

**Rozmiar:** ok. 4–5 tys. tokenów, z czego większość to lista `fclass`.

---

## K3: K2 + wskazówki i przykłady

**Co zawiera:** K2 oraz dwa elementy, które mówią modelowi, jak pisać zapytania: wskazówki przestrzenne i przykłady pytanie→SQL.

### 1. Wskazówki przestrzenne

```text
- Dane są w EPSG:4326 (stopnie). Aby liczyć odległości, długości i powierzchnie w metrach,
  rzutuj geometrie na geography, np. ST_Distance(a.geom::geography, b.geom::geography).
- Do wyszukiwania w promieniu używaj ST_DWithin(a.geom::geography, b.geom::geography, <metry>).
- Do sprawdzania, czy obiekt należy do obszaru, używaj ST_Intersects.
- Do liczenia długości lub powierzchni w granicach obszaru użyj ST_Intersection.
- Gdy pytanie dotyczy typu obiektu z pois, połącz gis_osm_pois_free i gis_osm_pois_a_free
  przez UNION.
- Aby pominąć obiekty bez nazwy, użyj warunku name <> ''.
- Aby liczyć każdy obiekt raz, użyj COUNT(DISTINCT osm_id).
- Obiekty referencyjne wybieraj z bazy po nazwie. Nie wpisuj współrzędnych ręcznie.
- Zawężaj wyniki do Warszawy przez przecięcie z jej granicą, bo dane obejmują całe województwo.
```

### 2. Przykłady pytanie→SQL (few-shot)

Mamy 5 przykładów, po jednym z każdej kategorii (Z, N, A, J, M). Wszystkie wykonano na bazie i zwracają sensowne wyniki.

**Przykłady celowo nie używają żadnego obiektu referencyjnego ani wartości `fclass` z pytań testowych.** Mają wspólną z nimi tylko strukturę zapytania, co w DAIL-SQL (praca 9) było źródłem zysku z przykładów.

Inaczej niż w DAIL-SQL przykłady są stałe, a nie dobierane do pytania. Dzięki temu nie potrzeba wyszukiwania (RAG), a wszystkie pytania dostają ten sam kontekst.

```sql
-- Pytanie: Ile piekarni jest w promieniu 400 m od stacji Warszawa Gdańska?
WITH ref AS (SELECT geom FROM gis_osm_transport_free
             WHERE fclass = 'railway_station' AND name = 'Warszawa Gdańska'),
poi AS (SELECT osm_id, geom FROM gis_osm_pois_free WHERE fclass = 'bakery' AND name <> ''
        UNION SELECT osm_id, geom FROM gis_osm_pois_a_free WHERE fclass = 'bakery' AND name <> '')
SELECT count(DISTINCT poi.osm_id)
FROM poi, ref
WHERE ST_DWithin(poi.geom::geography, ref.geom::geography, 400);
-- wynik: 6

-- Pytanie: Jakie są 3 banki najbliższe Ogrodu Saskiego i jak daleko są w metrach?
WITH ref AS (SELECT geom FROM gis_osm_landuse_a_free WHERE fclass = 'park' AND name = 'Ogród Saski'),
poi AS (SELECT osm_id, name, geom FROM gis_osm_pois_free WHERE fclass = 'bank' AND name <> ''
        UNION SELECT osm_id, name, geom FROM gis_osm_pois_a_free WHERE fclass = 'bank' AND name <> '')
SELECT poi.name, round(ST_Distance(poi.geom::geography, ref.geom::geography)) AS distance_m
FROM poi, ref
ORDER BY distance_m
LIMIT 3;
-- wynik: mBank 57, Bank Pekao 60, Bank Pekao 187

-- Pytanie: Które 3 dzielnice Warszawy mają najwięcej księgarń?
WITH waw AS (SELECT geom FROM gis_osm_adminareas_a_free WHERE fclass = 'admin_level6' AND name = 'Warszawa'),
d AS (SELECT a.name, a.geom FROM gis_osm_adminareas_a_free a, waw
      WHERE a.fclass = 'admin_level9' AND a.name <> '' AND ST_Intersects(a.geom, waw.geom)),
poi AS (SELECT osm_id, geom FROM gis_osm_pois_free WHERE fclass = 'bookshop' AND name <> ''
        UNION SELECT osm_id, geom FROM gis_osm_pois_a_free WHERE fclass = 'bookshop' AND name <> '')
SELECT d.name, count(DISTINCT poi.osm_id) AS bookshops
FROM d JOIN poi ON ST_Intersects(poi.geom, d.geom)
GROUP BY d.name
ORDER BY bookshops DESC
LIMIT 3;
-- wynik: Śródmieście 67, Mokotów 23, Praga-Południe 14

-- Pytanie: Ile kościołów w Warszawie ma przystanek autobusowy w promieniu 100 m?
WITH waw AS (SELECT geom FROM gis_osm_adminareas_a_free WHERE fclass = 'admin_level6' AND name = 'Warszawa'),
ch AS (SELECT osm_id, geom FROM gis_osm_pofw_free WHERE fclass LIKE 'christian%' AND name <> ''
       UNION SELECT osm_id, geom FROM gis_osm_pofw_a_free WHERE fclass LIKE 'christian%' AND name <> '')
SELECT count(DISTINCT ch.osm_id)
FROM ch, waw
WHERE ST_Intersects(ch.geom, waw.geom)
  AND EXISTS (SELECT 1 FROM gis_osm_transport_free t
              WHERE t.fclass = 'bus_stop' AND t.name <> ''
                AND ST_DWithin(ch.geom::geography, t.geom::geography, 100));
-- wynik: 151

-- Pytanie: Ile hektarów zajmują wody na Żoliborzu?
WITH zol AS (SELECT geom FROM gis_osm_adminareas_a_free WHERE fclass = 'admin_level9' AND name = 'Żoliborz')
SELECT round((sum(ST_Area(ST_Intersection(w.geom, zol.geom)::geography)) / 10000)::numeric, 2) AS area_ha
FROM (SELECT DISTINCT ON (osm_id) osm_id, geom FROM gis_osm_water_a_free WHERE name <> '') w, zol
WHERE ST_Intersects(w.geom, zol.geom);
-- wynik: 3.69
```

W prompcie przykłady podajemy bez komentarzy `-- wynik`. Wyniki zapisaliśmy tu tylko po to, żeby było widać, że zapytania zostały sprawdzone.

**Co model zyskuje względem K2:** gotowe wzorce rozwiązań typowych pułapek: `geography`, `UNION` obu tabel `pois`, `name <> ''`, `COUNT(DISTINCT osm_id)`, `ST_Intersection`, pobieranie obiektu referencyjnego z bazy.

**Rola w eksperymencie:** górna granica tego, co da się osiągnąć samym kontekstem przy prostej architekturze. Porównanie K2→K3 pokazuje, czy model sam przekłada fakty o danych na poprawny SQL, czy potrzebuje wzorców.

**Rozmiar:** ok. 6–7 tys. tokenów.

**Ryzyko:** przykład E5 (powierzchnia wód na Żoliborzu) ma tę samą strukturę co M08 (powierzchnia parków na Mokotowie). Wynik M08 na K3 będzie przez to zawyżony. Jest to zgodne z ideą few-shot, ale warto o tym napisać w artykule. Można też zamienić E5 na pytanie o długość, np. długość odcinków rzeki w dzielnicy.

---

## Podsumowanie: która pułapka w danych jest rozwiązana na którym poziomie

| Pułapka | K0 | K1 | K2 | K3 |
|---|---|---|---|---|
| Typ geometrii (punkt / poligon) | – | ✓ | ✓ | ✓ |
| SRID 4326, więc odległość w stopniach | – | widać SRID | widać SRID | ✓ wskazówka |
| Wartości `fclass` (np. `'pharmacy'`, `'christian'`) | – | – | ✓ | ✓ |
| Ten sam typ obiektu w `pois` i `pois_a` | – | – | ✓ fakt | ✓ wskazówka + przykład |
| Granica Warszawy w `adminareas` | – | – | ✓ | ✓ + przykład |
| Pusta nazwa to `''`, a nie NULL | – | – | ✓ fakt | ✓ wskazówka + przykład |
| Nazwy w bazie inne niż potoczne | – | – | ✓ (2 obiekty) | ✓ |
| Nazwy nieunikalne w województwie | – | – | ✓ fakt | ✓ wskazówka |
| Pobieranie obiektu z bazy zamiast wpisanych współrzędnych | – | – | – | ✓ wskazówka + przykład |

Konwencje oceny (przecięcie, liczenie raz, pomijanie obiektów bez nazwy, jednostki) są w części wspólnej na każdym poziomie, więc nie ma ich w tabeli.

## Implementacja

- Kontekst każdego poziomu zapisujemy jako osobny plik tekstowy (`k0.txt` … `k3.txt`, opcjonalnie `k1md.txt`). Prompt składamy z części wspólnej, pliku kontekstu i pytania.
- K0, K1 i listę `fclass` generuje skrypt z `information_schema.columns`, `geometry_columns` i `SELECT DISTINCT fclass`. Opisy, fakty, wskazówki i przykłady wklejamy ręcznie z tego dokumentu.
- Dla każdego poziomu raportujemy liczbę tokenów w prompcie (z odpowiedzi API). Pozwoli to w artykule zestawić zysk jakości z kosztem, tak jak w DAIL-SQL.
