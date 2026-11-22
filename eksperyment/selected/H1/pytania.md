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
| Z07 | Ile supermarketów jest w Warszawie? | liczba | zawężenie do granicy Warszawy; obie tabele `pois`; bez filtra po nazwie |
| N01 | Jaki szpital jest najbliżej Pałacu Kultury i Nauki? | `name` | obie tabele `pois` (7 punktów, 37 poligonów) |
| N03 | Jak daleko w metrach jest najbliższy urząd pocztowy od Dworca Centralnego i jak się nazywa? | `name`, odległość | `::geography`, nie stopnie |
| N04 | Wymień 5 aptek położonych najbliżej Zamku Królewskiego. | `name` w kolejności | kolejność; obie tabele `pois` |
| N07 | Wymień 3 przystanki autobusowe najbliższe pomnikowi pamięci Konstantego Juliana Ordona i podaj, jak daleko są w metrach. | `name` w kolejności, odległość | nazwa w bazie: „Pamięci Konstantego Juliana Ordona” |
| J01 | Które szkoły w Warszawie mają w promieniu 300 metrów co najmniej jeden fast food? | `name` | obie tabele dla obu warstw; `name <> ''` tylko dla szkół, bo to one są wynikiem |
| J02 | Ile przedszkoli w Warszawie nie ma żadnego parku w promieniu 500 metrów? | liczba | `NOT EXISTS`; parki tylko z `landuse` |
| J05 | Wymień nazwy budynków stojących na terenie Łazienek Królewskich. | `name` | `name <> ''` — na terenie parku stoi 118 budynków, nazwanych jest 23; park jest w `landuse` i w `pois_a` |
| J08 | Wymień nazwy mostów samochodowych na Wiśle w Warszawie. | `name` | wartość `fclass` dla mostu |
| A01 | Ile jest restauracji, kawiarni, fast foodów, pubów i barów w promieniu kilometra od Pałacu Kultury i Nauki? Podaj liczbę dla każdego typu osobno. | typ, liczba | wszystkie 5 wartości `fclass`; `GROUP BY` |
| A03 | Które 5 stacji kolejowych i metra w Warszawie ma najwięcej restauracji w promieniu 500 metrów i ile ich jest? | `name` w kolejności, liczba | `railway_station`, nie `railway_halt`; remis na 5. miejscu — patrz [ustalenia](#ustalenia-rozstrzygające-niejasności) |
| A07 | Ile szkół, a ile przedszkoli jest w promieniu kilometra od Placu Bociani Zakątek? | typ, liczba | czy znalazł obiekt w bazie |
| A08 | Ile wypożyczalni rowerów w Warszawie jest w promieniu 300 metrów od stacji kolejowej lub metra, a ile dalej? | kategoria, liczba | obie tabele (129 punktów, 223 poligony) |
| M02 | Ile kilometrów ma ulica Marszałkowska w Warszawie? | długość | zawężenie do Warszawy (bez niego 9,9 km); `ST_Intersection` |
| M03 | Jaka jest odległość w linii prostej w metrach między Pałacem Kultury i Nauki a Stadionem Narodowym? | odległość | nazwa „PGE Narodowy”; nie stacja o tej nazwie |
| M05 | Ile kilometrów długości ma Wisła na odcinku w granicach Warszawy? | długość | suma odcinków; `ST_Intersection` |
| M07 | Jaka jest odległość w linii prostej w kilometrach między Parkiem Planeta Ursus a Placem Bociani Zakątek? | odległość | oba obiekty z bazy |

## Ustalenia rozstrzygające niejasności

Wszystkie liczby niżej sprawdzone na zrzucie Geofabrik z 2026-11-20
(patrz [konteksty/README.md](konteksty/README.md)). Te ustalenia obowiązują przy
pisaniu zapytań wzorcowych i przy ocenie odpowiedzi modelu. Nie trafiają do
promptu — model ma dojść do nich sam albo polec, bo właśnie to mierzymy.

### A. Zasady wspólne dla wszystkich pytań

1. **„w Warszawie"** = przecięcie (`ST_Intersects`) z `gis_osm_adminareas_a_free`,
   `fclass = 'admin_level6'`, `name = 'Warszawa'`. Ta sama geometria leży w bazie
   również jako `admin_level7` i `admin_level8` (sprawdzone: `ST_Equals` = true),
   więc warunek `name = 'Warszawa'` bez `fclass` **potraja wynik**. W pilotażu
   dało to 1497 supermarketów zamiast 500 — to jest wzorcowy przykład błędu,
   który ma znikać między K1 a K2.
2. **Przynależność do obszaru** sprawdzamy na pełnej geometrii obiektu
   (`ST_Intersects(obiekt.geom, obszar.geom)`), a nie na punkcie reprezentatywnym.
   Dla Z07 obie metody dają ten sam wynik (500), więc różnica nie wpływa na ocenę,
   ale wzorce mają być jednolite.
3. **Obiekty szukane bierzemy z obu tabel warstwy** (punktowej i poligonowej)
   przez `UNION`, i liczymy `COUNT(DISTINCT osm_id)`. Tabele w parze **nie mają
   wspólnych `osm_id`** (sprawdzone: 0 wspólnych dla `pois` i dla `transport`),
   więc `DISTINCT` nie scala punktu z poligonem — służy do usunięcia duplikatów
   *wewnątrz* tabeli, gdzie ten sam `osm_id` bywa zapisany z kilkoma `fclass`.
4. **Parki zawsze z `gis_osm_landuse_a_free`, `fclass = 'park'`.** Ten zbiór jest
   nadzbiorem parków z `gis_osm_pois_a_free`: 1514 wobec 1494, a wszystkie 1494
   mają ten sam `osm_id` co odpowiednik w `landuse`. Reguła jest więc jednolita
   dla J01, J02, J03 oraz dla obiektów odniesienia w Z05, A07 i M07 — i nie gubi
   żadnego parku.
5. **Filtr `name <> ''`** stosujemy tylko wtedy, gdy nazwy są wynikiem pytania.
   Przy zliczaniu i mierzeniu nie filtrujemy po nazwie. Brak nazwy to pusty napis
   (`name IS NULL` daje 0 wierszy w całej bazie).
6. **Jednostki.** Odległości, długości i powierzchnie liczymy po rzutowaniu na
   `geography`. Długość w granicach obszaru to `ST_Length(ST_Intersection(...))`,
   a przy poligonach mogących na siebie nachodzić — po `ST_Union`.
7. **Remis na granicy „top k".** Wzorzec wypisuje wszystkie obiekty o wartości
   granicznej, a odpowiedź modelu uznajemy za poprawną, jeśli zwrócił *dowolne*
   k obiektów zgodne z porządkiem i z kompletem obiektów powyżej progu. Dotyczy
   to realnie A03 (remis 39–39 na 5. miejscu); w N04 i N07 remisu nie ma.

### B. Obiekty odniesienia: który wiersz jest wzorcem

To największe źródło fałszywych ocen. Ten sam znany obiekt leży w bazie
w kilku tabelach naraz, a wybór geometrii zmienia wynik o kilkadziesiąt procent.
**Żaden poziom kontekstu nie mówi modelowi, który wiersz wybrać**, więc wyniku
policzonego z udokumentowanego wariantu nie wolno liczyć jako błędu — oznaczamy
go kodem `inna_geometria_odniesienia` i uznajemy za poprawny.

| Obiekt | Wzorzec (wariant główny) | Warianty dopuszczalne | Czy zmienia wynik |
|---|---|---|---|
| Pałac Kultury i Nauki | `pois_a_free`, `fclass='attraction'` (poligon) | `buildings_a_free` (poligon) | nie — 12 aptek w 500 m w obu |
| | | `pois_free`, `fclass='viewpoint'` (punkt) | **tak** — 9 aptek zamiast 12 |
| Dworzec Centralny | `transport_free`, `fclass='railway_station'`, `name='Warszawa Centralna'` (punkt) | `buildings_a_free`, `name='Warszawa Centralna'` (poligon) | **tak** — 24 vs 29 kawiarni w 300 m; 267 m vs 193 m do poczty |
| Zamek Królewski | `pois_a_free`, `fclass='castle'` (poligon) | `pois_a_free`, `fclass='attraction'`; `buildings_a_free` | do sprawdzenia przy wzorcu |
| Stadion Narodowy | `pois_a_free`, `fclass='stadium'`, `name='PGE Narodowy'` | — | — |
| Skwer Jolanty Brzeskiej, Plac Bociani Zakątek, Park Planeta Ursus | `landuse_a_free`, `fclass='park'` | `pois_a_free`, `fclass='park'` (ten sam `osm_id`, ta sama geometria) | nie |
| Pomnik pamięci K. J. Ordona | `pois_free`, `fclass='memorial'`, `name='Pamięci Konstantego Juliana Ordona'` (jedyny taki wiersz) | — | — |

Pułapki po nazwie, celowo zostawione w pytaniach:

- **Zamek Królewski:** w `pois_free` są dwa sklepy z pamiątkami o nazwie „Zamek
  Królewski" i muzeum „Zamek Królewski w Warszawie", a `fclass='castle'`
  o nazwie „Zamek królewski" (małą literą) leży **poza Warszawą**. Dopasowanie
  po samej nazwie, bez `fclass`, trafia w sklep.
- **Stadion Narodowy:** w `transport_free` jest `railway_station` o nazwie
  „Stadion Narodowy" i `railway_halt` „Warszawa Stadion". Stadion jako obiekt to
  „PGE Narodowy" w `pois_a_free`.
- **Pomnik Ordona:** w bazie są też trzy obiekty „Reduta Ordona" i przystanki
  „Ordona WSA".
- **Skwer Jolanty Brzeskiej:** osobny POI „Miejsce śmierci Jolanty Brzeskiej"
  (`fclass='memorial'`).

### C. Rozstrzygnięcia przy poszczególnych pytaniach

| Pytanie | Ustalenie |
|---|---|
| Z07 | supermarkety z obu tabel `pois`, `COUNT(DISTINCT osm_id)`, granica `admin_level6`. **Wzorzec: 500.** |
| A03, A08 | **`fclass='railway_station'` obejmuje w tych danych także stacje metra** — w Warszawie 39 z 50 obiektów to metro, a tylko 11 to kolej. Po `fclass` nie da się ich rozdzielić (można tylko po bliskości torów `subway`), więc pytania mówią teraz wprost „stacje kolejowe i metra" i wzorzec bierze wszystkie `railway_station`. `railway_halt` (43 obiekty w Warszawie) zostaje poza wynikiem. |
| A03 | remis na 5. miejscu: „Warszawa Centralna" i „Politechnika" mają po 39 restauracji. Wzorzec wypisuje 6 wierszy; ocena zgodnie z zasadą A7. |
| M02 | wszystkie odcinki `roads_free` o `name = 'Marszałkowska'` (77 w województwie), przycięte do granicy Warszawy i scalone przez `ST_Union`. **Wzorzec: 5,61 km** (bez zawężenia 9,90 km — ta różnica jest celem pytania). |
| M05 | Wisła to 28 linii `waterways_free`, `fclass='river'`, `name='Wisła'` (380,1 km w województwie). Poligonów `riverbank` nie liczymy, bo to obszar, a nie długość. **Wzorzec: 29,40 km** w granicach Warszawy. |
| J08 | most = odcinki `roads_free` z `bridge='T'` przecinające linie Wisły w granicach Warszawy. „Samochodowy" = odrzucamy `cycleway`, `footway`, `path`, `steps`, `pedestrian`, `track`. Uwaga: Most Świętokrzyski ma zarówno odcinek `tertiary`, jak i `cycleway`, więc filtr po `fclass` musi działać na poziomie odcinka, a nazwy trzeba zebrać przez `DISTINCT`. Wychodzi 9 mostów. |
| J01, J02, J03 | parki wyłącznie z `landuse` (zasada A4); `name <> ''` tylko dla obiektu będącego wynikiem (szkoły w J01, parki w J03). |
| N03 | wynik zawiera odległość, więc jest wrażliwy na wybór geometrii dworca (193 m vs 267 m) — oba warianty dopuszczalne, nazwa urzędu („Poczta Polska") jest w obu ta sama. |
| Z01, N01, N04, A01, A07, M03, M07 | obiekt odniesienia zgodnie z tabelą w części B. |

## Do uzupełnienia: tokeny i trafność

Liczymy tokeny całego promptu, czyli instrukcji, kontekstu i pytania razem. Zapisujemy je przy każdym wywołaniu, a tu wpisujemy średnią dla poziomu. Między pytaniami różni się tylko długość samego pytania, czyli kilkadziesiąt tokenów.

Zmierzone w serii z 21.11.2026 (240 wywołań, `claude-sonnet-5-5`, `effort: medium`),
średnia z `usage.input_tokens` po 60 próbach na poziom.

| Poziom | Tokeny promptu (średnia) | Tokeny odpowiedzi (średnia) | Trafność |
|---|---|---|---|
| K0 | 1 500 | 614 | — |
| K1 | 2 828 | 592 | — |
| K2 | 9 524 | 512 | — |
| K3 | 12 160 | 546 | — |

Wejście rośnie 8-krotnie między K0 a K3, a odpowiedzi lekko się skracają wraz
z rosnącym kontekstem — model mniej się waha i krócej uzasadnia.

## Zapytania wzorcowe

Zapytania leżą w [wzorce/](wzorce/), po jednym pliku `.sql` na pytanie. Kolumna
„Wynik" to wartość z bazy (zrzut 2026-11-20). **Każdy wzorzec wymaga jeszcze
sprawdzenia przez drugą osobę** — na razie napisała je jedna.

| Kod | Wzorzec | Wynik | Uwagi |
|---|---|---|---|
| Z01 | [Z01.sql](wzorce/Z01.sql) | **12** | obrys `attraction` i obrys budynku dają tyle samo; punkt `viewpoint` daje 9 |
| Z02 | [Z02.sql](wzorce/Z02.sql) | **19 nazw** ([lista](wzorce/Z02.out)) | od poligonu budynku dworca wychodzą 23 nazwy — wariant dopuszczalny |
| Z05 | [Z05.sql](wzorce/Z05.sql) | **7** | skwer jako park w `landuse` |
| Z07 | [Z07.sql](wzorce/Z07.sql) | **500** | bez `fclass='admin_level6'` wynik rośnie do 1500 |
| N01 | [N01.sql](wzorce/N01.sql) | **Szpital Kliniczny Dzieciątka Jezus**, 555 m | **pytanie nie różnicuje poziomów** — najbliższy szpital jest punktem, więc szukanie w samej tabeli punktowej też daje dobrą odpowiedź (najbliższy poligon to 956 m) |
| N03 | [N03.sql](wzorce/N03.sql) | **Poczta Polska**, 267 m | od poligonu budynku dworca wychodzi 193 m, nazwa ta sama — wariant dopuszczalny |
| N04 | [N04.sql](wzorce/N04.sql) | Apteka na Mariensztacie (190 m), Miejska (193), Hibiskus (810), Franciszkańska (898), Apteka Ojców Bonifratrów (938) | bez remisu na 5. miejscu (szósta jest 999 m); sama nazwa „Zamek Królewski" bez `fclass` trafia w dwa sklepy z pamiątkami |
| N07 | [N07.sql](wzorce/N07.sql) | Oraczy 01 (443 m), Gontarska 01 (497), Oraczy 02 (527) | bez remisu (czwarty 553 m); w bazie są też trzy obiekty „Reduta Ordona" |
| J01 | [J01.sql](wzorce/J01.sql) | **527 nazw szkół** | lista za długa na plik tekstowy — porównujemy wynikiem zapytania |
| J02 | [J02.sql](wzorce/J02.sql) | **324** | parki tylko z `landuse`; bez filtra po nazwie, bo liczymy |
| J05 | [J05.sql](wzorce/J05.sql) | **23 nazwy** ([lista](wzorce/J05.out)) | zastąpiło J03 (21.11); bez `name <> ''` wychodzi 118 wierszy |
| J08 | [J08.sql](wzorce/J08.sql) | **9 mostów**: Anny Jagiellonki, Gdański, Grota-Roweckiego, Ks. J. Poniatowskiego, Łazienkowski, M. Skłodowskiej-Curie, Siekierkowski, Śląsko-Dąbrowski, Świętokrzyski | Most Świętokrzyski ma odcinek `tertiary` i `cycleway` — filtr klas musi działać na odcinku, nie na nazwie |
| A01 | [A01.sql](wzorce/A01.sql) | bar 123, cafe 176, fast_food 218, pub 24, restaurant 286 | wszystkie pięć typów musi się pojawić |
| A03 | [A03.sql](wzorce/A03.sql) | Centrum 71, Nowy Świat-Uniwersytet 70, Rondo ONZ 57, Świętokrzyska 49, **Politechnika 39 = Warszawa Centralna 39** | remis na 5. miejscu — wzorzec ma 6 wierszy, ocena wg zasady A7. Cała piątka to stacje metra |
| A07 | [A07.sql](wzorce/A07.sql) | przedszkola 10, szkoły 1 | |
| A08 | [A08.sql](wzorce/A08.sql) | do 300 m: **62**, dalej: **290** | razem 352 wypożyczalni w Warszawie |
| M02 | [M02.sql](wzorce/M02.sql) | **5,61 km** | bez zawężenia do Warszawy 9,90 km |
| M03 | [M03.sql](wzorce/M03.sql) | **2502 m** | między obrysami; centroid–centroid daje 2861 m, punkt `viewpoint` 2585 m |
| M05 | [M05.sql](wzorce/M05.sql) | **29,40 km** | tylko linie `river`, bez poligonów koryta; w całym województwie Wisła ma 380,1 km |
| M07 | [M07.sql](wzorce/M07.sql) | **19,98 km** | centroid–centroid daje 20,14 km, czyli w granicach 1% tolerancji |
