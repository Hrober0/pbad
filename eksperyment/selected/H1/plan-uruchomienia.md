# Plan uruchomienia eksperymentu 1 (H1)

Plan krok po kroku: od postawionej bazy do tabeli trafności. Hipoteza i metoda:
[informacje-ogolne.md](../../../informacje-ogolne.md). Pytania:
[pytania.md](pytania.md). Konteksty: [konteksty/README.md](konteksty/README.md).

Zakres: 20 pytań × 4 poziomy (K0–K3) × 3 powtórzenia = **240 wywołań**.

## Stan na dziś (21.11.2026)

| Element | Stan |
|---|---|
| Kontener `pbad-postgres` | ✅ działa, PostgreSQL 18.3, PostGIS 3.6.3 (`docker/docker-compose.yml`) |
| Dane OSM w bazie | ✅ zrzut z 2026-11-20, 20 tabel `gis_osm_*`, SRID 4326, indeksy GiST, `ANALYZE` zrobiony |
| Konteksty K0–K3 | ✅ zweryfikowane wobec bazy i poprawione 21.11 ([README](konteksty/README.md)) |
| Pytania testowe | ✅ 20 wybranych, niejasności rozstrzygnięte w [pytania.md](pytania.md) |
| Zapytania wzorcowe | ⬜ 0/20 — **to jest wąskie gardło** |
| Skrypt uruchamiający serię | ✅ `python/console/run_h1.py run` (JSONL, wznawianie, równoległość) |
| Wykonywanie SQL na bazie | ✅ `python/console/run_h1.py exec` (rola `pbad_ro`, osobny plik wyników) |
| Porównanie z wzorcami | ⬜ czeka na wzorce |
| Rola `pbad_ro` | ✅ założona, sprawdzona (SELECT działa, DROP odrzucony) |

---

## Krok 1: dane w bazie (ok. 30 min, z czego 25 min to czekanie)

### 1.1. Wersja danych — rozstrzygnięte

Obowiązuje zrzut Geofabrik z **2026-11-20** (`mazowieckie-261120-free.gpkg.zip`,
562 MB). Zrzut z 29.10, na którym powstały pierwsze wersje kontekstów i pilotaż,
jest już niedostępny u Geofabrika (404 — serwer trzyma tylko najnowszy plik).

Konteksty K0–K3 zostały zweryfikowane wobec świeżo zaimportowanej bazy i
poprawione; co dokładnie się zgadzało, a co zmieniono, opisuje
[konteksty/README.md](konteksty/README.md) razem z sumami SHA-256 plików.
Pilotaż z 13.11 zostaje jako ilustracja, ale nie jako pomiar — liczby tokenów
dotyczą tam starszych kontekstów.

**Wszyscy w zespole muszą liczyć na tym samym pliku**, bo inaczej zapytania
wzorcowe i odpowiedzi modelu będą oceniane na różnych danych. Plik warto odłożyć
na dysk współdzielony i sprawdzać sumę SHA-256 przed pracą.

### 1.2. Import

Baza już działa. Jeśli trzeba ją postawić od nowa:

```bash
cd docker && docker compose up -d
```

Import (Git Bash, w folderze z plikiem `mazowieckie.gpkg`, ok. 2–5 min):

```bash
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd):/data:ro" ghcr.io/osgeo/gdal:ubuntu-small-latest \
  ogr2ogr -f PostgreSQL PG:"host=host.docker.internal port=5432 dbname=pbad user=pbad password=pbad" \
  /data/mazowieckie.gpkg -a_srs EPSG:4326 -lco GEOMETRY_NAME=geom -progress
```

### 1.3. Weryfikacja po imporcie

```sql
-- 1. 20 tabel gis_osm_*
SELECT count(*) FROM information_schema.tables
WHERE table_schema = 'public' AND table_name LIKE 'gis_osm_%';

-- 2. SRID wszędzie 4326
SELECT f_table_name, srid, type FROM geometry_columns ORDER BY 1;

-- 3. indeksy GiST (ogr2ogr zakłada je sam — bez nich zapytania będą wolne)
SELECT tablename, indexname FROM pg_indexes
WHERE schemaname = 'public' AND indexdef LIKE '%gist%' ORDER BY 1;

-- 4. statystyki dla plannera
ANALYZE;
```

### 1.4. Rola tylko do odczytu (dla zapytań modelu)

Zapytania generowane przez model wykonujemy na osobnej roli bez prawa zapisu i
z twardym limitem czasu. To zabezpieczenie przed `DROP`em (model ma zwracać
`SELECT`, ale nie ma gwarancji) i przed zapytaniem, które zawiesi bazę na
godzinę.

```sql
CREATE ROLE pbad_ro LOGIN PASSWORD 'pbad_ro';
GRANT CONNECT ON DATABASE pbad TO pbad_ro;
GRANT USAGE ON SCHEMA public TO pbad_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO pbad_ro;
ALTER ROLE pbad_ro SET statement_timeout = '120s';
ALTER ROLE pbad_ro SET default_transaction_read_only = on;
```

---

## Krok 2: zapytania wzorcowe (20 sztuk — największa praca, ok. 1–2 dni)

Bez wzorców nie da się ocenić ani jednej odpowiedzi modelu, więc to jest
krytyczna ścieżka. Dla każdego z 20 pytań potrzebujemy: zapytania SQL, jego
wyniku i notatki, co uznajemy za kolumny kluczowe.

Proponowana organizacja:

- Plik `eksperyment/selected/H1/wzorce/<kod>.sql` z zapytaniem, a wynik
  w `wzorce/<kod>.out` (lub jedna tabela w [pytania.md](pytania.md)).
- Kolejność od najprostszych (M03, M07, Z01) do najtrudniejszych (J03, A08, M05).
- **Wymóg z metody: każdy wzorzec sprawdza druga osoba** i ogląda wynik na mapie
  (DataGrip/QGIS). Przy pytaniach J03 i M05 (Wisła) oraz M02 (Marszałkowska)
  to nie jest formalność — tam łatwo o cichy błąd.
- Zasady rozstrzygające niejasności są już ustalone i sprawdzone na bazie:
  sekcja **„Ustalenia rozstrzygające niejasności"** w [pytania.md](pytania.md)
  (definicja „w Warszawie", dedulikacja po `osm_id`, parki tylko z `landuse`,
  wybór geometrii obiektu odniesienia, remisy w „top k", jednostki). Wzorzec,
  który je łamie, jest błędny — nie odwrotnie.
- Cztery wartości są już policzone i mogą posłużyć za kontrolę przy pisaniu
  wzorców: Z07 = 500 supermarketów, M02 = 5,61 km, M05 = 29,40 km,
  J08 = 9 mostów. Nadal wymagają sprawdzenia przez drugą osobę.

---

## Krok 3: skrypt uruchamiający serię (ok. pół dnia)

Dziś w `python/console` jest tylko interaktywny REPL. Potrzebny jest skrypt
wsadowy, np. `python/runner/run_experiment1.py`, który:

1. czyta listę pytań z pliku (osobny `pytania.json` albo parsowanie tabeli z MD),
2. robi iloczyn kartezjański: pytanie × poziom × powtórzenie (240 zadań),
3. dla każdego zadania woła `SqlGenerator.generate()` — bez historii, dokładnie
   jak w pilotażu (`claude-sonnet-5-5`, `effort: medium`, `json_schema`),
4. **zapisuje do JSONL po każdym wywołaniu** (nie na końcu), jeden rekord =
   jedna próba:

   ```json
   {"ts": "...", "question_id": "Z02", "level": "K2", "rep": 1,
    "model": "claude-sonnet-5-5", "effort": "medium",
    "input_tokens": 8972, "output_tokens": 743,
    "raw": "{\"sql\": \"...\", \"explanation\": \"...\"}"}
   ```

5. umie wznowić przerwaną serię (pomija `(question_id, level, rep)`, które już
   są w pliku),
6. ponawia próbę przy 429 i 5xx z odczekaniem, 2–4 wywołania równolegle,
7. nie dotyka bazy — generowanie i wykonywanie SQL to osobne etapy, żeby dało
   się ocenić ponownie bez płacenia drugi raz.

**`input_tokens` z `usage` jest jednym z mierzonych wyników** (koszt poziomu
kontekstu), więc musi lecieć do pliku przy każdej próbie, a nie być liczony
później szacunkowo.

## Krok 4: skrypt oceniający (ok. pół dnia)

`python/runner/evaluate.py` czyta JSONL z kroku 3 i dla każdej próby:

1. wyciąga `sql` z odpowiedzi (jest już w JSON, więc bez parsowania markdown),
2. wykonuje je na roli `pbad_ro` z `statement_timeout`; błąd wykonania →
   `executed: false`, próba niepoprawna,
3. wykonuje wzorzec i porównuje według zasad z metody:
   - tylko kolumny kluczowe, pozostałe ignorujemy,
   - wiersze jako zbiory (`set`), kolejność tylko w pytaniach „najbliższe"/„top k",
   - liczby zmiennoprzecinkowe z tolerancją 1%,
   - napisy dokładnie,
4. dopisuje klasyfikację błędu. Kody do zliczania wziąć wprost z metody:
   `zla_tabela`, `zla_wartosc_fclass`, `stopnie_zamiast_metrow`,
   `wspolrzedne_z_pamieci`, `zla_funkcja`, `zla_agregacja`, `nie_wykonuje_sie`,
   a dodatkowo `potrojona_granica` (warunek `name='Warszawa'` bez `fclass`, co
   łapie `admin_level6/7/8` i mnoży wynik przez 3) oraz
   **`inna_geometria_odniesienia`** — to ostatnie **nie jest błędem**: oznacza
   odpowiedź policzoną od innego, udokumentowanego wiersza tego samego obiektu
   (patrz tabela obiektów odniesienia w [pytania.md](pytania.md)) i liczy się
   jako poprawna.
   Część da się wykryć automatycznie (np. `ST_DWithin` bez `::geography` z
   progiem > 1 → stopnie; `ST_MakePoint` z literałami → współrzędne z pamięci),
   resztę oznaczamy ręcznie.

Wynik: `wyniki.csv` z kolumnami `question_id, level, rep, executed, correct, error_code,
input_tokens, output_tokens`.

## Krok 5: analiza (ok. 2 h)

Z `wyniki.csv` liczymy to, co jest w „zmienne zależne":

- trafność na każdym poziomie (60 prób na poziom) i przyrosty K0→K1, K1→K2, K2→K3,
- trafność w rozbiciu na kategorie Z/N/J/A/M (12–15 prób na komórkę — tylko opisowo),
- odsetek zapytań wykonujących się,
- rozkład kodów błędów per poziom (tu widać, co znika po dodaniu K3),
- średnia `input_tokens` per poziom → tabela „tokeny vs trafność" w
  [pytania.md](pytania.md).

Przy 60 próbach na poziom przedział ufności jest szeroki (±12 pp), więc wnioski
formułujemy opisowo. Warto policzyć przedziały Wilsona i podać je w tabeli —
wtedy od razu widać, czy różnica K1→K2 jest czymkolwiek więcej niż szumem.

---

## Koszt i czas

Z pilotażu znamy długości promptów: K0 ≈ 1450, K1 ≈ 2778, K2 ≈ 8972, K3 ≈ 11411
tokenów wejściowych.

| Pozycja | Tokeny | Cena (`claude-sonnet-5-5`: $2/MTok wej., $10/MTok wyj.) |
|---|---|---|
| Eksperyment 1 — wejście | 20 × 3 × 24,6 tys. ≈ 1,48 mln | ≈ $2,95 |
| Eksperyment 2 — wejście | 87 × 9,0 tys. ≈ 0,78 mln | ≈ $1,57 |
| Wyjście (327 × ok. 1 tys., z rozumowaniem) | ≈ 0,33 mln | ≈ $3,30 |
| **Razem** | | **≈ $8 (realnie $6–12)** |

Opcje obniżenia, jeśli budżet jest problemem:

- **Batch API: −50%** na wejściu i wyjściu (≈ $4). Nasze wywołania są całkowicie
  niewrażliwe na opóźnienie, więc to naturalny wybór: wrzucamy 240 żądań jednym
  zestawem i odbieramy wyniki, gdy będą gotowe.
- **Prompt caching:** kontekst K2/K3 to stały prefiks systemowy, więc 3 powtórzenia
  tego samego poziomu mogą czytać go z cache po $0,10/MTok zamiast $2/MTok.
  Przy tej skali oszczędza to dolary, nie dziesiątki — nie warto komplikować.
- Nowe konto w API dostaje darmowe kredyty na start; są też zniżki akademickie
  (kontakt przez sales@anthropic.com).

Czas: import 30 min, wzorce 1–2 dni, skrypty 1 dzień, sama seria 240 wywołań
≈ 30–60 min (przy 2–4 równoległych), ocena i analiza pół dnia.

---

## Dlaczego przez API, a nie przez Claude Code / czat

Kuszące jest puszczenie 240 próbek przez subskrypcję Claude Code zamiast płacić
za API. Nie nadaje się to do tego badania i trzeba to zapisać, żeby nie wracało:

1. **Nie znamy promptu.** Claude Code dokłada własny prompt systemowy (opisy
   narzędzi, reguły harnessu, informacje o środowisku, `CLAUDE.md`). To kilka
   tysięcy tokenów, których nie da się usunąć ani policzyć. Zmienna „instrukcja
   zadania stała we wszystkich próbach" przestaje być kontrolowana, a
   **„liczba tokenów w prompcie" — jeden z mierzonych wyników — traci sens.**
2. **Model nie jest ten sam.** Artykuł podaje `claude-sonnet-5-5`; sesja
   Claude Code to inny model (tutaj Opus 5) i nie raportuje identyfikatora
   snapshotu, który obsłużył zapytanie.
3. **Nie ma `effort: medium` ani `json_schema`.** Oba są w metodzie i w kodzie
   pilotażu. W CLI trzeba by parsować swobodny tekst.
4. **Model ma narzędzia.** W Claude Code model może sam zajrzeć do bazy albo do
   plików `konteksty/`. Jedna taka próba unieważnia cały poziom K0/K1, bo model
   dostaje kontekst, którego nie miał dostać.
5. **Izolacja prób.** W jednym czacie każda kolejna odpowiedź widzi poprzednie.
   Trzeba by odpalać 240 osobnych procesów `claude -p`, co i tak nie usuwa
   punktów 1–4.
6. **Limity i przeznaczenie subskrypcji.** 240 wywołań z rozumowaniem i 9–11 tys.
   tokenów kontekstu to nie jest interaktywna praca z kodem, do której
   subskrypcja służy, i szybko trafi na limity.

Koszt zrobienia tego poprawnie (≈ $8, z Batch API ≈ $4) jest niższy niż
miesięczna subskrypcja, więc nie ma czego optymalizować. Sebastian ma już klucz
(zrobił pilotaż 13.11) — najprościej użyć tego samego klucza i rozliczyć
w zespole.

Co natomiast można zrobić modelem w IDE bez wpływu na wyniki: napisać skrypty
z kroków 3–4, zaproponować zapytania wzorcowe (i tak wymagają sprawdzenia przez
drugą osobę), zweryfikować fakty z K2 zapytaniami do bazy i policzyć statystyki.
To wszystko jest poza ścieżką pomiarową.

---

## Kolejność prac (co robić w jakiej kolejności)

1. Ustalić plik z danymi (A czy B z 1.1) i zaimportować go — **blokuje wszystko**.
2. Równolegle: pisanie wzorców (osoba 1) i skryptu runnera (osoba 2).
3. Po imporcie: zweryfikować fakty z K2, jeśli wybrano wariant B.
4. Uruchomić serię 240 wywołań.
5. Ocena i analiza.
6. Na spotkanie 27.11: wyniki co najmniej dla kilku pytań na wszystkich poziomach
   + wstępna wersja artykułu.
