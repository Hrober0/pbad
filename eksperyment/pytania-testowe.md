# Pytania testowe

Zestaw pytań do eksperymentu: wpływ kontekstu bazy danych (K0–K3) i precyzji pytania (P1–P3) na jakość generowanego przestrzennego SQL.

Obszar: Warszawa. Dane: OSM z Geofabrik (województwo mazowieckie, plik z 2026-10-29), EPSG:4326, kolumna geometrii `geom`.


## Klasy kontektu bazy danych
Poziom	Co dostaje model
K0	Same nazwy tabel i kolumn
K1	DDL z typami, w tym geometry(Point,4326)
K2	K1 + opis tabel i kolumn + lista wartości fclass
K3	K2 + wskazówki przestrzenne (np. „dla metrów rzutuj na ::geography”) + 3–5 przykładów pytanie→SQL


## Zasady

### Kategorie zapytań

Kategorie Z, N, J, A pochodzą z NALSpatial (praca 6 w przeglądzie literatury). Kategorię M dodaliśmy na podstawie GS-SQL (praca 5), bo funkcje pomiarowe są osobną, łatwiejszą grupą.

| Kod | Kategoria | Typowe funkcje PostGIS |
|---|---|---|
| Z | Zakresowe (obiekty w odległości / wewnątrz obszaru) | `ST_DWithin`, `ST_Intersects` |
| N | Najbliżsi sąsiedzi | `ORDER BY geom <-> ...`, `ST_Distance` |
| J | Złączenia przestrzenne (relacje między dwiema warstwami) | `JOIN ... ON ST_DWithin / ST_Intersects` |
| A | Agregacje przestrzenne | `COUNT`, `GROUP BY`, `HAVING` + funkcje przestrzenne |
| M | Pomiary geometrii | `ST_Area`, `ST_Length`, `ST_Perimeter`, `ST_Distance` |

### Wersje pytania

Wszystkie trzy wersje pytania mają **tę samą intencję i to samo zapytanie wzorcowe**. Różnią się wyłącznie sformułowaniem.

- **P1, precyzyjna:** pytanie używa nazw z bazy (tabele, wartości `fclass`, kolumna `name`) i podaje dokładne parametry z jednostkami.
- **P2, naturalna:** pytanie jest napisane zwykłym językiem, bez terminów z bazy, ale z dokładnymi parametrami.
- **P3, potoczna:** pytanie używa skrótów, synonimów i kolokwializmów, a intencja nie jest powiedziana wprost. Parametry da się jednoznacznie odtworzyć, np. „pół kilometra” albo „na Mokotowie”, ale nie podajemy ich formalnie. P3 nie wprowadza celowej niejednoznaczności. Gdyby to robiło, nie dałoby się porównać wyniku z jednym zapytaniem wzorcowym.

### Znane i mało znane obiekty referencyjne

Pytania oznaczone **[MZ]** odnoszą się do obiektu mało znanego (mały skwer, pomnik na peryferiach). Model nie zna jego położenia z danych treningowych, więc musi pobrać geometrię z bazy.

Przy znanych obiektach (PKiN, Stadion Narodowy) model może zamiast tego wpisać współrzędne z pamięci, np. `ST_MakePoint(21.006, 52.231)`. Takie zapytanie bywa „prawie dobre”. Porównanie wyników [MZ] z pozostałymi pokaże, jak często model tak robi i ile to kosztuje. Przy klasyfikacji błędów warto osobno oznaczać zapytania z wpisanymi na stałe współrzędnymi.

### Reguły obowiązujące we wszystkich pytaniach

Reguły 1–3 zawiera instrukcja zadania na **każdym** poziomie kontekstu (K0–K3), bo to konwencje oceny, a nie wiedza o danych.

1. **Obiekt należy do obszaru, gdy się z nim przecina** (`ST_Intersects`). Dotyczy to też obiektów na granicy obszaru. W pytaniach o długość lub powierzchnię „w granicach” obszaru (M02, M05, M08) liczymy tylko część wewnątrz, czyli `ST_Intersection`.
2. **Każdy obiekt liczymy raz,** z deduplikacją po `osm_id`.
3. **Obiekty bez nazwy pomijamy,** zarówno w wynikach, jak i przy liczeniu. Dotyczy to też obiektów, względem których coś sprawdzamy, np. parków w J02.

### Ustalenia dotyczące danych (zweryfikowane w bazie)

Poniższe ustalenia obowiązują przy pisaniu zapytań wzorcowych. Są też kandydatami do wiedzy o danych w kontekście K2.

1. **Granica Warszawy:** `gis_osm_adminareas_a_free` z `fclass = 'admin_level6'` i `name = 'Warszawa'`. Ta sama geometria występuje też jako `admin_level7` i `admin_level8`. Dzielnice to `admin_level9` (18 dzielnic).
2. **Ten sam typ obiektu bywa zapisany jako punkt albo jako poligon.** Na przykład szpitali w Warszawie jest 7 jako punkty w `gis_osm_pois_free` i 37 jako poligony w `gis_osm_pois_a_free`, a wypożyczalni rowerów odpowiednio 129 i 223. Dlatego **„obiekty typu X” oznaczają rekordy z obu tabel:** `gis_osm_pois_free` ∪ `gis_osm_pois_a_free`. Wyjątkiem są pytania, które wprost wskazują jedną tabelę. Dla poligonów odległość liczymy od geometrii, a nie od centroidu. Te dwie tabele nie mają wspólnych `osm_id`.
3. **Parki są zdublowane:** 1491 obiektów występuje z tym samym `osm_id` w `gis_osm_landuse_a_free` i w `gis_osm_pois_a_free` (oba z `fclass = 'park'`). W pytaniach o parki używamy tylko `gis_osm_landuse_a_free`.
4. **Brak nazwy to pusty napis, a nie NULL:** `name = ''`. Warunek `name IS NOT NULL` nic nie odfiltruje, poprawny warunek to `name <> ''`.
5. **Odległości i powierzchnie w metrach** liczymy przez rzutowanie na `geography`, np. `ST_DWithin(a.geom::geography, b.geom::geography, 500)`. Samo `geometry` w EPSG:4326 daje stopnie.
6. **Nazwy ulic nie są unikalne w województwie.** Na przykład `name = 'Marszałkowska'` daje 9,9 km dróg, bo obejmuje też ulice o tej nazwie w innych miejscowościach. Pytania o konkretną ulicę trzeba zawężać do Warszawy.
7. **W bazie są też tabele rozszerzenia `tiger`** (amerykański geokoder z obrazu `postgis/postgis`). Do kontekstu bierzemy tylko tabele `public.gis_osm_*`.
8. **„Stacja kolejowa”** to `fclass = 'railway_station'` w `gis_osm_transport_free`. Przystanki osobowe (`railway_halt`) do niej nie należą.

### Obiekty referencyjne

| Obiekt w pytaniu | Znany? | Tabela | Warunek | Uwaga (pułapka dla modelu) |
|---|---|---|---|---|
| Pałac Kultury i Nauki (PKiN) | tak | `gis_osm_buildings_a_free` | `name = 'Pałac Kultury i Nauki'` | ta sama nazwa jest też w `pois_free` (`viewpoint`) i `pois_a_free` (`attraction`) |
| Dworzec Centralny | tak | `gis_osm_transport_free` | `fclass = 'railway_station' AND name = 'Warszawa Centralna'` | w bazie nazwa to „Warszawa Centralna”, a nie „Dworzec Centralny” |
| Stadion Narodowy | tak | `gis_osm_pois_a_free` | `fclass = 'stadium' AND name = 'PGE Narodowy'` | w `gis_osm_transport_free` jest też stacja kolejowa o nazwie „Stadion Narodowy” |
| Zamek Królewski | tak | `gis_osm_pois_a_free` | `fclass = 'castle' AND name = 'Zamek Królewski'` | |
| Łazienki Królewskie | tak | `gis_osm_landuse_a_free` | `fclass = 'park' AND name = 'Łazienki Królewskie'` | ten sam obiekt jest też w `pois_a_free` |
| Pole Mokotowskie | tak | `gis_osm_landuse_a_free` | `fclass = 'park' AND name = 'Pole Mokotowskie'` | ten sam obiekt jest też w `pois_a_free` |
| Wisła | tak | `gis_osm_waterways_free` | `fclass = 'river' AND name = 'Wisła'` | rzeka jest podzielona na wiele odcinków |
| Skwer Jolanty Brzeskiej (Mokotów) | **nie** | `gis_osm_landuse_a_free` | `fclass = 'park' AND name = 'Skwer Jolanty Brzeskiej'` | ok. 0,56 ha |
| Park Planeta Ursus (Ursus) | **nie** | `gis_osm_landuse_a_free` | `fclass = 'park' AND name = 'Park Planeta Ursus'` | ok. 0,49 ha |
| Plac Bociani Zakątek (Białołęka) | **nie** | `gis_osm_landuse_a_free` | `fclass = 'park' AND name = 'Plac Bociani Zakątek'` | ok. 1,1 ha |
| Pomnik pamięci Konstantego Juliana Ordona (Rembertów) | **nie** | `gis_osm_pois_free` | `fclass = 'memorial' AND name = 'Pamięci Konstantego Juliana Ordona'` | |

---

## Z: Zapytania zakresowe

### Z01
- **P1:** Ile obiektów z `gis_osm_pois_free` i `gis_osm_pois_a_free` o `fclass = 'pharmacy'` znajduje się w odległości do 500 m od obiektu z `gis_osm_buildings_a_free` o `name = 'Pałac Kultury i Nauki'`?
- **P2:** Ile aptek jest w promieniu 500 metrów od Pałacu Kultury i Nauki?
- **P3:** Ile aptek mam w zasięgu pół kilometra od PKiN?

### Z02
- **P1:** Podaj nazwy obiektów z `gis_osm_pois_free` i `gis_osm_pois_a_free` o `fclass = 'cafe'` w odległości do 300 m od obiektu z `gis_osm_transport_free` o `fclass = 'railway_station'` i `name = 'Warszawa Centralna'`.
- **P2:** Wymień nazwy kawiarni w promieniu 300 metrów od Dworca Centralnego.
- **P3:** Gdzie wyskoczyć na kawę w okolicy 300 m od Centralnego?

### Z03
- **P1:** Ile obiektów z `gis_osm_transport_free` o `fclass = 'tram_stop'` leży w odległości do 1 km od obiektu z `gis_osm_pois_a_free` o `fclass = 'stadium'` i `name = 'PGE Narodowy'`?
- **P2:** Ile przystanków tramwajowych jest w promieniu kilometra od Stadionu Narodowego?
- **P3:** Ile mam przystanków tramwaju w ciągu kilometra od Narodowego?

### Z04
- **P1:** Wypisz nazwy obiektów z `gis_osm_pois_free` i `gis_osm_pois_a_free` o `fclass` równym `'restaurant'` lub `'cafe'`, które przecinają się z obiektem z `gis_osm_landuse_a_free` o `name = 'Łazienki Królewskie'`.
- **P2:** Jakie restauracje i kawiarnie znajdują się na terenie Łazienek Królewskich?
- **P3:** Gdzie można coś zjeść albo wypić kawę w Łazienkach?

### Z05 [MZ]
- **P1:** Ile obiektów z `gis_osm_pois_free` i `gis_osm_pois_a_free` o `fclass = 'pharmacy'` znajduje się w odległości do 1 km od obiektu z `gis_osm_landuse_a_free` o `name = 'Skwer Jolanty Brzeskiej'`?
- **P2:** Ile aptek jest w promieniu kilometra od Skweru Jolanty Brzeskiej?
- **P3:** Ile aptek mam w kilometrze od skweru Brzeskiej?

### Z06
- **P1:** Podaj nazwy obiektów z `gis_osm_pois_free` i `gis_osm_pois_a_free` o `fclass = 'museum'` w odległości do 1 km od obiektu z `gis_osm_pois_a_free` o `fclass = 'castle'` i `name = 'Zamek Królewski'`.
- **P2:** Wymień muzea w promieniu kilometra od Zamku Królewskiego.
- **P3:** Jakie muzea mogę obejść pieszo z Zamku, maks. kilometr?

### Z07
- **P1:** Ile obiektów z `gis_osm_pois_free` i `gis_osm_pois_a_free` o `fclass = 'supermarket'` przecina się z obiektem z `gis_osm_adminareas_a_free` o `fclass = 'admin_level6'` i `name = 'Warszawa'`?
- **P2:** Ile supermarketów jest w Warszawie?
- **P3:** Ile w Warszawie jest marketów spożywczych?

### Z08 [MZ]
- **P1:** Ile obiektów z `gis_osm_transport_free` o `fclass = 'bus_stop'` leży w odległości do 500 m od obiektu z `gis_osm_landuse_a_free` o `name = 'Plac Bociani Zakątek'`?
- **P2:** Ile przystanków autobusowych jest w promieniu 500 metrów od Placu Bociani Zakątek?
- **P3:** Ile mam przystanków autobusu w zasięgu pół kilometra od Bocianiego Zakątka?

---

## N: Najbliżsi sąsiedzi

### N01
- **P1:** Podaj nazwę obiektu z `gis_osm_pois_free` lub `gis_osm_pois_a_free` o `fclass = 'hospital'` położonego najbliżej obiektu z `gis_osm_buildings_a_free` o `name = 'Pałac Kultury i Nauki'`.
- **P2:** Jaki szpital jest najbliżej Pałacu Kultury i Nauki?
- **P3:** Który szpital najbliżej PKiN?

### N02
- **P1:** Podaj nazwy 3 obiektów z `gis_osm_transport_free` o `fclass = 'railway_station'` najbliższych obiektowi z `gis_osm_pois_a_free` o `fclass = 'stadium'` i `name = 'PGE Narodowy'`.
- **P2:** Wymień 3 stacje kolejowe najbliższe Stadionowi Narodowemu.
- **P3:** Jakie są trzy najbliższe stacje pociągowe od Narodowego?

### N03
- **P1:** Podaj nazwę i odległość w metrach najbliższego obiektu z `gis_osm_pois_free` lub `gis_osm_pois_a_free` o `fclass = 'post_office'` od obiektu z `gis_osm_transport_free` o `fclass = 'railway_station'` i `name = 'Warszawa Centralna'`.
- **P2:** Jak daleko w metrach jest najbliższy urząd pocztowy od Dworca Centralnego i jak się nazywa?
- **P3:** Gdzie najbliższa poczta od Centralnego i ile to metrów?

### N04
- **P1:** Podaj nazwy 5 obiektów z `gis_osm_pois_free` lub `gis_osm_pois_a_free` o `fclass = 'pharmacy'` najbliższych obiektowi z `gis_osm_pois_a_free` o `fclass = 'castle'` i `name = 'Zamek Królewski'`.
- **P2:** Wymień 5 aptek położonych najbliżej Zamku Królewskiego.
- **P3:** Daj pięć najbliższych aptek przy Zamku.

### N05 [MZ]
- **P1:** Podaj nazwę i odległość w metrach najbliższego obiektu z `gis_osm_pois_free` lub `gis_osm_pois_a_free` o `fclass = 'police'` od obiektu z `gis_osm_landuse_a_free` o `name = 'Park Planeta Ursus'`.
- **P2:** Jaki komisariat policji jest najbliżej Parku Planeta Ursus i jak daleko w metrach?
- **P3:** Gdzie najbliższe psy od parku Planeta na Ursusie i ile metrów?

### N06
- **P1:** Podaj nazwę obiektu z `gis_osm_pois_free` lub `gis_osm_pois_a_free` o `fclass = 'cinema'` najbliższego obiektowi z `gis_osm_landuse_a_free` o `name = 'Łazienki Królewskie'`.
- **P2:** Jakie kino jest najbliżej Łazienek Królewskich?
- **P3:** Najbliższe kino od Łazienek?

### N07 [MZ]
- **P1:** Podaj nazwy 3 obiektów z `gis_osm_transport_free` o `fclass = 'bus_stop'` najbliższych obiektowi z `gis_osm_pois_free` o `fclass = 'memorial'` i `name = 'Pamięci Konstantego Juliana Ordona'` wraz z odległością w metrach.
- **P2:** Wymień 3 przystanki autobusowe najbliższe pomnikowi pamięci Konstantego Juliana Ordona i podaj, jak daleko są w metrach.
- **P3:** Trzy najbliższe przystanki autobusu od pomnika Ordona w Rembertowie, ile metrów do każdego?

### N08
- **P1:** Podaj nazwę obiektu z `gis_osm_pois_free` lub `gis_osm_pois_a_free` o `fclass` równym `'swimming_pool'` lub `'sports_centre'` najbliższego obiektowi z `gis_osm_pois_a_free` o `fclass = 'stadium'` i `name = 'PGE Narodowy'`.
- **P2:** Jaki basen lub centrum sportowe jest najbliżej Stadionu Narodowego?
- **P3:** Gdzie najbliżej Narodowego popływam albo poćwiczę?

---

## J: Złączenia przestrzenne

### J01
- **P1:** Podaj nazwy obiektów z `gis_osm_pois_free` i `gis_osm_pois_a_free` o `fclass = 'school'`, które przecinają się z obiektem z `gis_osm_adminareas_a_free` o `fclass = 'admin_level6'` i `name = 'Warszawa'` i w odległości do 300 m od których znajduje się co najmniej jeden obiekt z `gis_osm_pois_free` lub `gis_osm_pois_a_free` o `fclass = 'fast_food'`.
- **P2:** Które szkoły w Warszawie mają w promieniu 300 metrów co najmniej jeden fast food?
- **P3:** Przy których warszawskich szkołach jest jakiś fast food bliżej niż 300 m?

### J02
- **P1:** Ile obiektów z `gis_osm_pois_free` i `gis_osm_pois_a_free` o `fclass = 'kindergarten'`, które przecinają się z obiektem z `gis_osm_adminareas_a_free` o `fclass = 'admin_level6'` i `name = 'Warszawa'`, nie ma w odległości do 500 m żadnego obiektu z `gis_osm_landuse_a_free` o `fclass = 'park'`?
- **P2:** Ile przedszkoli w Warszawie nie ma żadnego parku w promieniu 500 metrów?
- **P3:** Ile warszawskich przedszkoli nie ma parku w zasięgu pół kilometra?

### J03
- **P1:** Podaj nazwy obiektów z `gis_osm_landuse_a_free` o `fclass = 'park'`, które przecinają się z obiektem z `gis_osm_adminareas_a_free` o `fclass = 'admin_level6'` i `name = 'Warszawa'` oraz z obiektem z `gis_osm_waterways_free` o `fclass = 'river'` i `name = 'Wisła'`.
- **P2:** Przez które parki w Warszawie przepływa Wisła albo które parki do niej przylegają?
- **P3:** Jakie warszawskie parki są nad samą Wisłą?

### J04
- **P1:** Podaj nazwy obiektów z `gis_osm_pois_free` i `gis_osm_pois_a_free` o `fclass = 'hotel'`, które przecinają się z obiektem z `gis_osm_adminareas_a_free` o `fclass = 'admin_level6'` i `name = 'Warszawa'` i w odległości do 200 m od których znajduje się obiekt z `gis_osm_transport_free` o `fclass = 'tram_stop'`.
- **P2:** Które hotele w Warszawie mają przystanek tramwajowy w promieniu 200 metrów?
- **P3:** Hotele w Wawie z tramwajem pod nosem, do 200 m?

### J05
- **P1:** Podaj nazwy obiektów z `gis_osm_buildings_a_free`, które przecinają się z obiektem z `gis_osm_landuse_a_free` o `name = 'Łazienki Królewskie'`.
- **P2:** Wymień nazwy budynków stojących na terenie Łazienek Królewskich.
- **P3:** Jakie budynki są w Łazienkach?

### J06
- **P1:** Podaj nazwy obiektów z `gis_osm_pois_free` i `gis_osm_pois_a_free` o `fclass = 'library'`, które przecinają się z obiektem z `gis_osm_adminareas_a_free` o `fclass = 'admin_level6'` i `name = 'Warszawa'` i w odległości do 100 m od których znajduje się obiekt z `gis_osm_pois_free` lub `gis_osm_pois_a_free` o `fclass = 'cafe'`.
- **P2:** Które biblioteki w Warszawie mają kawiarnię w promieniu 100 metrów?
- **P3:** Przy jakich bibliotekach w Warszawie jest kawiarnia tuż obok, do 100 m?

### J07
- **P1:** Ile obiektów z `gis_osm_transport_free` o `fclass = 'railway_station'`, które przecinają się z obiektem z `gis_osm_adminareas_a_free` o `fclass = 'admin_level6'` i `name = 'Warszawa'`, leży w odległości do 500 m od obiektu z `gis_osm_pois_free` lub `gis_osm_pois_a_free` o `fclass = 'hospital'`?
- **P2:** Ile stacji kolejowych w Warszawie ma szpital w promieniu 500 metrów?
- **P3:** Przy ilu warszawskich stacjach pociągu jest szpital w zasięgu pół kilometra?

### J08
- **P1:** Podaj unikalne nazwy obiektów z `gis_osm_roads_free` o `fclass` z listy (`'motorway'`, `'trunk'`, `'primary'`, `'secondary'`, `'tertiary'`), które przecinają się z obiektem z `gis_osm_waterways_free` o `fclass = 'river'` i `name = 'Wisła'` oraz z obiektem z `gis_osm_adminareas_a_free` o `fclass = 'admin_level6'` i `name = 'Warszawa'`.
- **P2:** Wymień nazwy mostów samochodowych na Wiśle w Warszawie.
- **P3:** Którymi mostami przejadę autem przez Wisłę w Wawie?

---

## A: Agregacje przestrzenne

### A01
- **P1:** Dla każdej wartości `fclass` z listy (`'restaurant'`, `'cafe'`, `'fast_food'`, `'pub'`, `'bar'`) podaj liczbę obiektów z `gis_osm_pois_free` i `gis_osm_pois_a_free` w odległości do 1 km od obiektu z `gis_osm_buildings_a_free` o `name = 'Pałac Kultury i Nauki'`.
- **P2:** Ile jest restauracji, kawiarni, fast foodów, pubów i barów w promieniu kilometra od Pałacu Kultury i Nauki? Podaj liczbę dla każdego typu osobno.
- **P3:** Ile knajp różnego typu jest w kilometrze od PKiN? Rozbij na restauracje, kawiarnie, fast foody, puby i bary.

### A02
- **P1:** Podaj 5 wartości `fclass` o największej łącznej liczbie obiektów z `gis_osm_pois_free` i `gis_osm_pois_a_free`, które przecinają się z obiektem z `gis_osm_adminareas_a_free` o `fclass = 'admin_level6'` i `name = 'Warszawa'`, razem z liczbą obiektów.
- **P2:** Jakie 5 rodzajów punktów usługowych występuje w Warszawie najczęściej i ile ich jest?
- **P3:** Czego w Warszawie jest najwięcej? Top 5 rodzajów miejsc z liczbą.

### A03
- **P1:** Dla każdego obiektu z `gis_osm_transport_free` o `fclass = 'railway_station'`, który przecina się z obiektem z `gis_osm_adminareas_a_free` o `fclass = 'admin_level6'` i `name = 'Warszawa'`, podaj liczbę obiektów z `gis_osm_pois_free` i `gis_osm_pois_a_free` o `fclass = 'restaurant'` w odległości do 500 m. Posortuj malejąco i zwróć 5 pierwszych.
- **P2:** Które 5 stacji kolejowych w Warszawie ma najwięcej restauracji w promieniu 500 metrów i ile ich jest?
- **P3:** Przy których stacjach pociągów w Wawie jest najwięcej restauracji w zasięgu pół kilometra? Top 5.

### A04
- **P1:** Podaj nazwy obiektów z `gis_osm_landuse_a_free` o `fclass = 'park'`, które przecinają się z obiektem z `gis_osm_adminareas_a_free` o `fclass = 'admin_level6'` i `name = 'Warszawa'` i z którymi przecinają się co najmniej 3 obiekty z `gis_osm_pois_free` lub `gis_osm_pois_a_free` o `fclass` z listy (`'restaurant'`, `'cafe'`, `'fast_food'`).
- **P2:** Które parki w Warszawie mają na swoim terenie co najmniej 3 lokale gastronomiczne (restauracje, kawiarnie lub fast foody)?
- **P3:** W których warszawskich parkach są przynajmniej trzy miejsca, gdzie można coś zjeść albo wypić kawę?

### A05
- **P1:** Podaj średnią odległość w metrach od każdego obiektu z `gis_osm_pois_free` i `gis_osm_pois_a_free` o `fclass = 'school'`, który przecina się z obiektem z `gis_osm_adminareas_a_free` o `fclass = 'admin_level6'` i `name = 'Warszawa'`, do najbliższego obiektu z `gis_osm_transport_free` o `fclass = 'bus_stop'`.
- **P2:** Jaka jest średnia odległość w metrach od szkoły w Warszawie do najbliższego przystanku autobusowego?
- **P3:** Ile średnio metrów ma warszawska szkoła do najbliższego przystanku autobusu?

### A06
- **P1:** Dla każdego obiektu z `gis_osm_adminareas_a_free` o `fclass = 'admin_level9'`, który przecina się z obiektem o `fclass = 'admin_level6'` i `name = 'Warszawa'`, podaj liczbę obiektów z `gis_osm_pois_free` i `gis_osm_pois_a_free` o `fclass = 'pharmacy'`. Zwróć 5 obiektów z największą liczbą.
- **P2:** Które 5 dzielnic Warszawy ma najwięcej aptek i ile ich jest?
- **P3:** Na których dzielnicach w Wawie jest najwięcej aptek? Top 5.

### A07 [MZ]
- **P1:** Dla każdej wartości `fclass` z listy (`'school'`, `'kindergarten'`) podaj liczbę obiektów z `gis_osm_pois_free` i `gis_osm_pois_a_free` w odległości do 1 km od obiektu z `gis_osm_landuse_a_free` o `name = 'Plac Bociani Zakątek'`.
- **P2:** Ile szkół, a ile przedszkoli jest w promieniu kilometra od Placu Bociani Zakątek?
- **P3:** Ile szkół i przedszkoli osobno jest w kilometrze od Bocianiego Zakątka?

### A08
- **P1:** Ile obiektów z `gis_osm_pois_free` i `gis_osm_pois_a_free` o `fclass = 'bicycle_rental'`, które przecinają się z obiektem z `gis_osm_adminareas_a_free` o `fclass = 'admin_level6'` i `name = 'Warszawa'`, znajduje się w odległości do 300 m od obiektu z `gis_osm_transport_free` o `fclass = 'railway_station'`, a ile dalej niż 300 m?
- **P2:** Ile wypożyczalni rowerów w Warszawie jest w promieniu 300 metrów od stacji kolejowej, a ile dalej?
- **P3:** Ile stacji Veturilo w Wawie stoi przy dworcach, do 300 m, a ile nie?

---

## M: Pomiary geometrii

### M01
- **P1:** Podaj powierzchnię w hektarach obiektu z `gis_osm_landuse_a_free` o `name = 'Łazienki Królewskie'`.
- **P2:** Jaką powierzchnię w hektarach mają Łazienki Królewskie?
- **P3:** Ile hektarów mają Łazienki?

### M02
- **P1:** Podaj łączną długość w kilometrach tych części obiektów z `gis_osm_roads_free` o `name = 'Marszałkowska'`, które leżą w granicach obiektu z `gis_osm_adminareas_a_free` o `fclass = 'admin_level6'` i `name = 'Warszawa'`.
- **P2:** Ile kilometrów ma ulica Marszałkowska w Warszawie?
- **P3:** Jak długa jest Marszałkowska, w km?

### M03
- **P1:** Podaj odległość w metrach między obiektem z `gis_osm_buildings_a_free` o `name = 'Pałac Kultury i Nauki'` a obiektem z `gis_osm_pois_a_free` o `fclass = 'stadium'` i `name = 'PGE Narodowy'`.
- **P2:** Jaka jest odległość w linii prostej w metrach między Pałacem Kultury i Nauki a Stadionem Narodowym?
- **P3:** Ile metrów w linii prostej z PKiN na Narodowy?

### M04
- **P1:** Podaj nazwy 5 obiektów z `gis_osm_landuse_a_free` o `fclass = 'park'`, które przecinają się z obiektem z `gis_osm_adminareas_a_free` o `fclass = 'admin_level6'` i `name = 'Warszawa'`, o największej powierzchni, wraz z powierzchnią w hektarach.
- **P2:** Wymień 5 największych parków w Warszawie i podaj ich powierzchnię w hektarach.
- **P3:** Top 5 największych parków w Warszawie, ile mają hektarów?

### M05
- **P1:** Podaj łączną długość w kilometrach tych części obiektów z `gis_osm_waterways_free` o `fclass = 'river'` i `name = 'Wisła'`, które leżą w granicach obiektu z `gis_osm_adminareas_a_free` o `fclass = 'admin_level6'` i `name = 'Warszawa'`.
- **P2:** Ile kilometrów długości ma Wisła na odcinku w granicach Warszawy?
- **P3:** Ile km Wisły przepływa przez Warszawę?

### M06
- **P1:** Podaj powierzchnię w metrach kwadratowych obiektu z `gis_osm_buildings_a_free` o `name = 'Pałac Kultury i Nauki'`.
- **P2:** Jaką powierzchnię zabudowy w metrach kwadratowych zajmuje Pałac Kultury i Nauki?
- **P3:** Ile metrów kwadratowych zajmuje PKiN?

### M07 [MZ]
- **P1:** Podaj odległość w kilometrach między obiektem z `gis_osm_landuse_a_free` o `name = 'Park Planeta Ursus'` a obiektem z `gis_osm_landuse_a_free` o `name = 'Plac Bociani Zakątek'`.
- **P2:** Jaka jest odległość w linii prostej w kilometrach między Parkiem Planeta Ursus a Placem Bociani Zakątek?
- **P3:** Ile km w linii prostej z parku Planeta na Ursusie do Bocianiego Zakątka?

### M08
- **P1:** Podaj łączną powierzchnię w hektarach tych części obiektów z `gis_osm_landuse_a_free` o `fclass = 'park'`, które leżą w granicach obiektu z `gis_osm_adminareas_a_free` o `fclass = 'admin_level9'` i `name = 'Mokotów'`.
- **P2:** Ile hektarów parków jest na Mokotowie?
- **P3:** Ile hektarów zieleni parkowej ma Mokotów?

---

## Podsumowanie

| Kategoria | Liczba pytań | W tym [MZ] | Liczba wariantów (× 3 wersje) |
|---|---|---|---|
| Z: zakresowe | 8 | 2 | 24 |
| N: najbliżsi sąsiedzi | 8 | 2 | 24 |
| J: złączenia przestrzenne | 8 | 0 | 24 |
| A: agregacje | 8 | 1 | 24 |
| M: pomiary | 8 | 1 | 24 |
| **Razem** | **40** | **6** | **120** |

W kategorii J nie ma pytań [MZ], bo złączenia dotyczą całych warstw, a nie pojedynczego obiektu.

Do porównania znanych i mało znanych obiektów służą pary pytań o tej samej strukturze:

| Pytanie ze znanym obiektem | Odpowiednik [MZ] |
|---|---|
| Z01 (apteki przy PKiN) | Z05 (apteki przy Skwerze Jolanty Brzeskiej) |
| Z03 (przystanki tramwajowe przy Stadionie Narodowym) | Z08 (przystanki autobusowe przy Placu Bociani Zakątek) |
| N03 (najbliższa poczta i odległość) | N05 (najbliższy komisariat i odległość) |
| N02 / N04 (k najbliższych) | N07 (3 najbliższe przystanki z odległością) |
| A01 (liczba według typów w promieniu) | A07 (liczba według typów w promieniu) |
| M03 (odległość między dwoma obiektami) | M07 (odległość między dwoma obiektami) |
