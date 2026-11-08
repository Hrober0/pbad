# Poziomy kontekstu bazy danych (K0–K3)

Opis tego, co model dostaje w prompcie na każdym poziomie kontekstu. Poziom kontekstu to pierwszy czynnik eksperymentu. Drugim jest precyzja pytania (P1–P3), opisana w [pytania-testowe.md](pytania-testowe.md).

## Zasady budowy poziomów

1. **Poziomy są kumulatywne:** każdy zawiera całą treść poprzedniego i dodaje jedną nową rodzajowo porcję informacji. Dzięki temu różnicę wyników między sąsiednimi poziomami można przypisać konkretnej dodanej informacji.
2. **K2 opisuje, K3 instruuje.** K2 zawiera wyłącznie fakty o danych („co jest w bazie”), np. „brak nazwy zapisano jako pusty napis”. K3 dodaje wskazówki, jak pisać zapytania („co z tym zrobić”), np. „aby pominąć obiekty bez nazwy, użyj `name <> ''`”, oraz przykłady. To rozdzielenie pozwala sprawdzić, czy modelowi wystarczy wiedza o danych, czy potrzebuje gotowych wzorców. Ma to znaczenie dla hipotezy H1.
3. **Treść jest generowana z bazy, jeśli się da.** Nazwy kolumn, typy, DDL i listy wartości `fclass` pobieramy zapytaniami do bazy. Ręcznie piszemy tylko opisy (K2) oraz wskazówki i przykłady (K3). Dzięki temu łatwo odtworzyć eksperyment na innym regionie.
4. **Kontekst obejmuje 20 tabel `public.gis_osm_*`.** Tabele rozszerzenia `tiger`, które dodaje obraz `postgis/postgis`, pomijamy na każdym poziomie.
5. **Prompt jest jednym wywołaniem bez historii.** Model ma jedną próbę: nie dostaje błędów wykonania i nie poprawia zapytania. Pętla poprawek to osobny temat (prace 2 i 4 w przeglądzie literatury) i świadomie go nie badamy.

## Część wspólna dla wszystkich poziomów

Każdy prompt zaczyna się tą samą instrukcją zadania. Opisuje ona samo zadanie, a nie dane, więc nie zmienia się między poziomami. Cała wiedza o bazie jest w kontekście, bo to ona jest badanym czynnikiem.

```text
Jesteś asystentem, który na podstawie pytania użytkownika buduje zapytanie SQL
dla bazy PostgreSQL 18 z rozszerzeniem PostGIS 3.6.

Zbuduj jedno zapytanie SELECT, które odpowiada na zadane pytanie.
Nie modyfikuj danych.

Poniżej znajdziesz dodatkowe informacje o bazie danych, które mogą pomóc
w zbudowaniu zapytania.

<KONTEKST K0 / K1 / K2 / K3>

Pytanie: <PYTANIE>
```

Instrukcja jest celowo krótka. Formatu odpowiedzi nie opisujemy słowami, bo wymusza
go schemat JSON przekazany w `output_config.format`: model zwraca obiekt z polami
`sql` i `explanation`. Pole `sql` jest w schemacie pierwsze, więc powstaje przed
wyjaśnieniem — `explanation` opisuje gotowe zapytanie, a nie rozumowanie, które
mogłoby na nie wpłynąć.

Instrukcja nie narzuca też żadnych konwencji liczenia ani jednostek. Wcześniejsza
wersja je zawierała, ale to szczegóły danych, a nie opis zadania, więc ich miejsce
jest w kontekście: fakty w K2, wskazówki w K3. Dzięki temu instrukcja nie podpowiada
niczego, co miałoby odróżniać poziomy. Ceną jest to, że przy pytaniach o jednostkę
albo o przynależność do obszaru model może przyjąć własne założenie — zapisuje je
w polu `explanation` i bierzemy je pod uwagę przy ocenie.

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
- osm_id: identyfikator obiektu w OpenStreetMap, nie zawsze unikalny,
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
- Sześć warstw ma po dwie tabele: bez _a dla obiektów narysowanych jako punkt i z _a dla
  narysowanych jako poligon. Są to pois, pofw, traffic, transport, natural i places. Ten sam
  typ obiektu występuje w obu tabelach, a bywa, że prawie wyłącznie w jednej z nich.
- Parki są zapisane w gis_osm_landuse_a_free i powtórzone (z tym samym osm_id)
  w gis_osm_pois_a_free.
- Obiekty bez nazwy mają w kolumnie name pusty napis '', a nie NULL.
- Nazwy ulic i obiektów nie są unikalne w województwie (np. ulica Marszałkowska
  występuje w kilku miejscowościach).
- Nazwy w kolumnie name pochodzą z OpenStreetMap i mogą różnić się od nazw potocznych,
  używanych w pytaniach.
- Większość kościołów ma fclass = 'christian', a nie 'christian_catholic'.
```

Fakty opisują dane jako całość i żaden z nich nie podaje nazwy obiektu, o który pytamy w pytaniach testowych. Inaczej K2 dawałoby gotową odpowiedź na część pytań, a przyrost trafności K1 → K2 byłby zawyżony. Samo dopasowanie nazwy jest czynnością przy pisaniu zapytania, więc wskazówka o tym jest dopiero w K3.

**Co model zyskuje względem K1:**
- zna wartości `fclass`, więc wie, że apteka to `'pharmacy'`, a kościół to `'christian'`,
- wie o rozdzieleniu punktów i poligonów, o granicy Warszawy i o pustych nazwach,
- wie, że nazwy w bazie mogą różnić się od potocznych, ale nie dostaje gotowej nazwy żadnego obiektu z pytań.

**Rola w eksperymencie:** główny poziom dla hipotezy H1. Przyrost trafności K1 → K2 mierzy wpływ opisu zawartości danych. Według H1 ma być większy niż przyrost K0 → K1 (opis struktury) i K2 → K3 (wskazówki i przykłady). K2 jest też stałym poziomem kontekstu w eksperymencie 2 (H2), bo w prompcie nie ma wtedy żadnej gotowej wartości promienia.

**Rozmiar:** ok. 4–5 tys. tokenów, z czego większość to lista `fclass`.

---

## K3: K2 + wskazówki i przykłady

**Co zawiera:** K2 oraz dwa elementy, które mówią modelowi, jak pisać zapytania: wskazówki przestrzenne i przykłady pytanie→SQL.

### 1. Wskazówki przestrzenne

```text
- Dane są w EPSG:4326 (stopnie). Aby liczyć odległości, długości i powierzchnie w metrach,
  rzutuj geometrie na geography, np. ST_Distance(a.geom::geography, b.geom::geography).
- Do wyszukiwania w promieniu używaj ST_DWithin(a.geom::geography, b.geom::geography, <metry>).
- Do sprawdzania, czy obiekt należy do obszaru, używaj ST_Intersects. Gdy obiekt sam jest
  obszarem i ma leżeć w całości wewnątrz, użyj ST_Within.
- Do liczenia długości lub powierzchni w granicach obszaru użyj ST_Intersection. Gdy poligony
  mogą na siebie nachodzić, scal je wcześniej przez ST_Union.
- Gdy pytanie dotyczy typu obiektu z warstwy mającej tabelę _a, połącz obie tabele przez
  UNION, np. gis_osm_pois_free z gis_osm_pois_a_free. Dotyczy to tak samo obiektów szukanych,
  obiektów odniesienia i tych, które występują tylko w warunku.
- Gdy pytanie prosi o nazwy obiektów, pomijaj obiekty bez nazwy warunkiem name <> ''.
  Brak nazwy zapisano jako pusty napis, więc name IS NOT NULL niczego nie odfiltruje.
  Przy zliczaniu i mierzeniu nie filtruj po nazwie.
- Aby liczyć każdy obiekt raz, użyj COUNT(DISTINCT osm_id).
- Obiekty referencyjne wybieraj z bazy po nazwie. Nie wpisuj współrzędnych ręcznie.
- Nazwa w bazie może różnić się od nazwy z pytania, więc dopasowuj po fragmencie,
  np. name ILIKE '%Centralna%', a nie przez równość.
- Zawężaj wyniki do Warszawy przez przecięcie z jej granicą, bo dane obejmują całe województwo.
```

### 2. Przykłady pytanie→SQL (few-shot)

Mamy 5 przykładów, po jednym z każdej kategorii (Z, N, A, J, M). Wszystkie wykonano na bazie i zwracają sensowne wyniki.

**Przykłady celowo nie używają żadnego obiektu referencyjnego ani wartości `fclass` z pytań testowych.** Mają wspólną z nimi tylko strukturę zapytania, co w DAIL-SQL (praca 9) było źródłem zysku z przykładów.

Inaczej niż w DAIL-SQL przykłady są stałe, a nie dobierane do pytania. Dzięki temu nie potrzeba wyszukiwania (RAG), a wszystkie pytania dostają ten sam kontekst.

```sql
-- Pytanie: Ile piekarni jest w promieniu 400 m od Muzeum Narodowego w Warszawie?
WITH ref AS (SELECT geom FROM gis_osm_pois_free
             WHERE fclass = 'museum' AND name ILIKE '%Muzeum Narodowe%'
             UNION SELECT geom FROM gis_osm_pois_a_free
             WHERE fclass = 'museum' AND name ILIKE '%Muzeum Narodowe%'),
poi AS (SELECT osm_id, geom FROM gis_osm_pois_free WHERE fclass = 'bakery'
        UNION SELECT osm_id, geom FROM gis_osm_pois_a_free WHERE fclass = 'bakery')
SELECT count(DISTINCT poi.osm_id)
FROM poi, ref
WHERE ST_DWithin(poi.geom::geography, ref.geom::geography, 400);
-- wynik: 2

-- Pytanie: Jakie są 3 banki najbliższe Cmentarzowi Powązkowskiemu i jak daleko są w metrach?
WITH ref AS (SELECT geom FROM gis_osm_landuse_a_free
             WHERE fclass = 'cemetery' AND name ILIKE '%Powązkowski%'),
poi AS (SELECT osm_id, name, geom FROM gis_osm_pois_free WHERE fclass = 'bank' AND name <> ''
        UNION SELECT osm_id, name, geom FROM gis_osm_pois_a_free WHERE fclass = 'bank' AND name <> '')
SELECT poi.name, round(ST_Distance(poi.geom::geography, ref.geom::geography)) AS distance_m
FROM poi, ref
ORDER BY distance_m
LIMIT 3;
-- wynik: Bank Pekao 270, Millennium Bank 480, Millennium Bank 501

-- Pytanie: Które 3 dzielnice Warszawy mają najwięcej księgarń?
WITH waw AS (SELECT geom FROM gis_osm_adminareas_a_free WHERE fclass = 'admin_level6' AND name = 'Warszawa'),
d AS (SELECT a.name, a.geom FROM gis_osm_adminareas_a_free a, waw
      WHERE a.fclass = 'admin_level9' AND a.name <> '' AND ST_Within(a.geom, waw.geom)),
poi AS (SELECT osm_id, geom FROM gis_osm_pois_free WHERE fclass = 'bookshop'
        UNION SELECT osm_id, geom FROM gis_osm_pois_a_free WHERE fclass = 'bookshop')
SELECT d.name, count(DISTINCT poi.osm_id) AS bookshops
FROM d JOIN poi ON ST_Intersects(poi.geom, d.geom)
GROUP BY d.name
ORDER BY bookshops DESC
LIMIT 3;
-- wynik: Śródmieście 73, Mokotów 23, Praga-Południe 14

-- Pytanie: Ile kościołów w Warszawie ma stację paliw w promieniu 300 m?
WITH waw AS (SELECT geom FROM gis_osm_adminareas_a_free WHERE fclass = 'admin_level6' AND name = 'Warszawa'),
ch AS (SELECT osm_id, geom FROM gis_osm_pofw_free WHERE fclass LIKE 'christian%'
       UNION SELECT osm_id, geom FROM gis_osm_pofw_a_free WHERE fclass LIKE 'christian%'),
fuel AS (SELECT geom FROM gis_osm_traffic_free WHERE fclass = 'fuel'
         UNION SELECT geom FROM gis_osm_traffic_a_free WHERE fclass = 'fuel')
SELECT count(DISTINCT ch.osm_id)
FROM ch, waw
WHERE ST_Intersects(ch.geom, waw.geom)
  AND EXISTS (SELECT 1 FROM fuel f
              WHERE ST_DWithin(ch.geom::geography, f.geom::geography, 300));
-- wynik: 39

-- Pytanie: Ile hektarów zajmują zbiorniki wodne i koryta rzek na Żoliborzu?
WITH zol AS (SELECT geom FROM gis_osm_adminareas_a_free WHERE fclass = 'admin_level9' AND name = 'Żoliborz')
SELECT round((ST_Area(ST_Union(ST_Intersection(w.geom, zol.geom))::geography) / 10000)::numeric, 2) AS area_ha
FROM gis_osm_water_a_free w, zol
WHERE w.fclass IN ('water', 'reservoir', 'riverbank')
  AND ST_Intersects(w.geom, zol.geom);
-- wynik: 52.72
```

W prompcie przykłady podajemy bez komentarzy `-- wynik`. Wyniki zapisaliśmy tu tylko po to, żeby było widać, że zapytania zostały sprawdzone.

**Co model zyskuje względem K2:** gotowe wzorce rozwiązań typowych pułapek: `geography`, `UNION` obu tabel `pois`, `name <> ''`, `COUNT(DISTINCT osm_id)`, `ST_Intersection`, pobieranie obiektu referencyjnego z bazy.

**Rola w eksperymencie:**
- Przyrost trafności K2 → K3 mierzy wpływ wskazówek i przykładów zapytań. Jest jednym z dwóch przyrostów, z którymi H1 porównuje przyrost K1 → K2.
- Pokazuje, czy model sam przekłada fakty o danych na poprawny SQL, czy potrzebuje wzorców.
- K3 to też górna granica tego, co da się osiągnąć samym kontekstem przy prostej architekturze.

**Rozmiar:** ok. 6–7 tys. tokenów.

**Ryzyko:** przykład E5 (powierzchnia wód na Żoliborzu) ma tę samą strukturę co M08 (powierzchnia parków na Mokotowie). Wynik M08 na K3 będzie przez to zawyżony. Jest to zgodne z ideą few-shot, ale warto o tym napisać w artykule. Można też zamienić E5 na pytanie o długość, np. długość odcinków rzeki w dzielnicy.

---

## Podsumowanie: która pułapka w danych jest rozwiązana na którym poziomie

| Pułapka | K0 | K1 | K2 | K3 |
|---|---|---|---|---|
| Typ geometrii (punkt / poligon) | – | ✓ | ✓ | ✓ |
| SRID 4326, więc odległość w stopniach | – | widać SRID | widać SRID | ✓ wskazówka |
| Wartości `fclass` (np. `'pharmacy'`, `'christian'`) | – | – | ✓ | ✓ |
| Ten sam typ obiektu w tabeli bez `_a` i z `_a` | – | – | ✓ fakt | ✓ wskazówka + przykład |
| Granica Warszawy w `adminareas` | – | – | ✓ | ✓ + przykład |
| Pusta nazwa to `''`, a nie NULL | – | – | ✓ fakt | ✓ wskazówka + przykład |
| Nazwy w bazie inne niż potoczne | – | – | ✓ fakt | ✓ + wskazówka (ILIKE) |
| Nazwy nieunikalne w województwie | – | – | ✓ fakt | ✓ wskazówka |
| Pobieranie obiektu z bazy zamiast wpisanych współrzędnych | – | – | – | ✓ wskazówka + przykład |

Instrukcja wspólna nie zawiera żadnych konwencji, więc nie ma czego dopisywać do tabeli.

## Implementacja

- Kontekst każdego poziomu zapisujemy jako osobny plik tekstowy (`k0.txt` … `k3.txt`, opcjonalnie `k1md.txt`). Prompt składamy z części wspólnej, pliku kontekstu i pytania.
- K0, K1 i listę `fclass` generuje skrypt z `information_schema.columns`, `geometry_columns` i `SELECT DISTINCT fclass`. Opisy, fakty, wskazówki i przykłady wklejamy ręcznie z tego dokumentu.
- Dla każdego poziomu raportujemy liczbę tokenów w prompcie (z odpowiedzi API). Pozwoli to w artykule zestawić zysk jakości z kosztem, tak jak w DAIL-SQL.
