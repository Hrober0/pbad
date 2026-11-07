# H2: pytania

Sprawdzamy, czy zmiana kontekstu pytania, bez zmiany jego formy ani samego niejasnego określenia, wpływa na to, jak model je zinterpretuje. Każda część bierze inne określenie, a kolumny w tabelach pokazują, co w niej zmieniamy.

**Numeracja:**
- **Numer** oznacza jedno pytanie bazowe, np. „apteki w pobliżu Dworca Centralnego”.
- **Litera** oznacza wariant tego pytania. Znaczenie liter jest podane w każdej części.

Wyniki porównujemy przede wszystkim między wariantami tego samego numeru, np. 1a, 1b i 1c. Porównania między numerami są wypisane pod tabelą każdej części.

37 wariantów × 3 powtórzenia = 111 wywołań, wszystkie przy kontekście K2. Model odpowiada w ustrukturyzowanej formie: zapytanie SQL i miejsce na uwagi.

## Część 2a: „w pobliżu” — 22 warianty, 66 wywołań

Odczytujemy przyjęty promień w metrach oraz rodzaj interpretacji: promień, k najbliższych (`ORDER BY ... LIMIT`), obszar administracyjny albo inny.

**Warianty:**

| Litera | Wariant |
|---|---|
| a | brak informacji o sposobie poruszania się |
| b | „Idę pieszo.” |
| c | „Jadę samochodem.” |
| d | „niedaleko” zamiast „w pobliżu”, bez informacji o sposobie poruszania się |

| # | Szukane | Punkt odniesienia | Wariant | Pytanie |
|---|---|---|---|---|
| 1a | apteki | Dworzec Centralny (centrum Warszawy) | brak | Wymień apteki w pobliżu Dworca Centralnego. |
| 1b | | | pieszo | Idę pieszo. Wymień apteki w pobliżu Dworca Centralnego. |
| 1c | | | samochodem | Jadę samochodem. Wymień apteki w pobliżu Dworca Centralnego. |
| 1d | | | „niedaleko” | Wymień apteki niedaleko Dworca Centralnego. |
| 2a | szpitale | Dworzec Centralny (centrum Warszawy) | brak | Wymień szpitale w pobliżu Dworca Centralnego. |
| 2b | | | pieszo | Idę pieszo. Wymień szpitale w pobliżu Dworca Centralnego. |
| 2c | | | samochodem | Jadę samochodem. Wymień szpitale w pobliżu Dworca Centralnego. |
| 3a | apteki | stacja Warszawa Płudy (peryferie Warszawy) | brak | Wymień apteki w pobliżu stacji Warszawa Płudy. |
| 3b | | | pieszo | Idę pieszo. Wymień apteki w pobliżu stacji Warszawa Płudy. |
| 3c | | | samochodem | Jadę samochodem. Wymień apteki w pobliżu stacji Warszawa Płudy. |
| 4a | szpitale | stacja Warszawa Płudy (peryferie Warszawy) | brak | Wymień szpitale w pobliżu stacji Warszawa Płudy. |
| 4b | | | pieszo | Idę pieszo. Wymień szpitale w pobliżu stacji Warszawa Płudy. |
| 4c | | | samochodem | Jadę samochodem. Wymień szpitale w pobliżu stacji Warszawa Płudy. |
| 5a | apteki | stacja Tłuszcz (małe miasto pod Warszawą) | brak | Wymień apteki w pobliżu stacji Tłuszcz. |
| 5b | | | pieszo | Idę pieszo. Wymień apteki w pobliżu stacji Tłuszcz. |
| 5c | | | samochodem | Jadę samochodem. Wymień apteki w pobliżu stacji Tłuszcz. |
| 6a | przystanki autobusowe | kiosk Ciasteczkowo (mały obiekt) | brak | Wymień przystanki autobusowe w pobliżu kiosku Ciasteczkowo. |
| 6b | | | pieszo | Idę pieszo. Wymień przystanki autobusowe w pobliżu kiosku Ciasteczkowo. |
| 6c | | | samochodem | Jadę samochodem. Wymień przystanki autobusowe w pobliżu kiosku Ciasteczkowo. |
| 7a | przystanki autobusowe | Lotnisko Chopina (duży obiekt) | brak | Wymień przystanki autobusowe w pobliżu Lotniska Chopina. |
| 7b | | | pieszo | Idę pieszo. Wymień przystanki autobusowe w pobliżu Lotniska Chopina. |
| 7c | | | samochodem | Jadę samochodem. Wymień przystanki autobusowe w pobliżu Lotniska Chopina. |

**Porównania:**

| Co sprawdzamy | Porównujemy |
|---|---|
| sposób poruszania się | warianty a, b i c w obrębie każdego numeru |
| określenie „niedaleko” zamiast „w pobliżu” | 1a i 1d |
| rodzaj szukanego obiektu | 1 i 2, 3 i 4 |
| wielkość miejscowości | 1, 3 i 5 (centrum Warszawy, peryferie Warszawy, małe miasto) |
| wielkość punktu odniesienia | 6 i 7 (mały kiosk, duże lotnisko) |

### Pytania 1, 3 i 5: wielkość miejscowości

Sprawdzamy, czy „w pobliżu” znaczy dla modelu co innego w dużym mieście niż w małej miejscowości. Na przykład w Warszawie „w pobliżu” może znaczyć 500 m, a w małym mieście mniej albo więcej. Szukamy zawsze aptek wokół stacji kolejowej, a zmienia się tylko miejscowość.

**Tłuszcz** to miasto liczące ok. 8 tys. mieszkańców, ok. 37 km od Warszawy (`gis_osm_transport_free`, `fclass = 'railway_station'`, `name = 'Tłuszcz'`). Nazwa stacji jest w bazie unikalna.

Liczba nazwanych aptek w zależności od promienia:

| Promień | Dworzec Centralny | Warszawa Płudy | Tłuszcz |
|---|---|---|---|
| 300 m | 3 | 0 | 1 |
| 500 m | 6 | 0 | 2 |
| 1 km | 26 | 1 | 2 |
| 2 km | 60 | 4 | 2 |

W Tłuszczu liczba aptek przestaje rosnąć już od 500 m, więc z samego wyniku nie odróżnimy promienia 500 m od 2 km. Promień odczytujemy więc z SQL, a liczba wyników jest tylko pomocnicza.

### Pytania 6 i 7: wielkość punktu odniesienia

Sprawdzamy, czy promień zależy od wielkości obiektu, **wokół którego** szukamy. Szukamy zawsze tego samego, czyli przystanków autobusowych, a zmieniamy punkt odniesienia: mały kiosk albo duże lotnisko. Oba są w Warszawie.

Szukamy przystanków autobusowych, a nie kiosków. Kiosków z nazwą jest w całej bazie tylko 126, więc w okolicy punktu odniesienia jest ich kilka, a ich liczba rośnie skokowo. Wtedy z wyniku nie widać, jaki promień przyjął model. Przystanków z nazwą jest ok. 17,7 tys., są rozmieszczone gęsto i równomiernie, a ich liczba rośnie płynnie z promieniem. Każda zmiana promienia jest więc widoczna w wyniku.

Liczba przystanków autobusowych w zależności od promienia:

| Promień | od kiosku Ciasteczkowo | od granicy Lotniska Chopina | od środka Lotniska Chopina |
|---|---|---|---|
| 300 m | 11 | 40 | 0 |
| 500 m | 37 | 65 | 0 |
| 1 km | 88 | 109 | 6 |
| 2 km | 276 | 278 | 68 |
| 5 km | 1111 | 1127 | 599 |

- **Kiosk Ciasteczkowo** (Śródmieście, `gis_osm_pois_free`, `fclass = 'kiosk'`) to punkt, a jego nazwa w bazie jest unikalna.
- **Lotnisko Chopina** (`gis_osm_transport_a_free`, `fclass = 'airport'`) to poligon o powierzchni ok. 568 ha, czyli w przybliżeniu kwadrat o boku 2,4 km.
- Przy tym samym promieniu liczony od granicy lotniska daje podobną liczbę przystanków co od kiosku. Promień liczony od środka lotniska daje dużo mniej, bo środek leży na płycie lotniska.
- **Na co patrzymy:**
  - czy dla lotniska model przyjmuje większy promień niż dla kiosku,
  - czy liczy odległość od granicy lotniska, czy od jego środka, np. przez `ST_Centroid`. Rozpoznamy to po liczbie wyników z tabeli powyżej,
  - czy wpływ sposobu poruszania się jest taki sam przy obu punktach odniesienia.

## Część 2b: czas dojazdu — 4 warianty, 12 wywołań

Odczytujemy przyjęty promień oraz wynikającą z niego prędkość. Litery a, b i c znaczą to samo co w części 2a, a d oznacza jazdę rowerem.

| # | Wariant | Pytanie |
|---|---|---|
| 8a | brak | Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |
| 8b | pieszo | Idę pieszo. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |
| 8c | samochodem | Jadę samochodem. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |
| 8d | rowerem | Jadę rowerem. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |

## Część 2c: „w centrum” — 5 wariantów, 15 wywołań

Odczytujemy, czym model zastąpił „centrum”: granicą dzielnicy, promieniem wokół jakiegoś obiektu czy prostokątem współrzędnych, i jaką to daje powierzchnię. Litera oznacza miasto: a = Warszawa, b = Płock, c = bez nazwy miasta.

| # | Szukane | Wariant | Pytanie |
|---|---|---|---|
| 9a | kawiarnie | Warszawa | Wymień kawiarnie w centrum Warszawy. |
| 9b | | Płock | Wymień kawiarnie w centrum Płocka. |
| 9c | | bez miasta | Wymień kawiarnie w centrum. |
| 10a | apteki | Warszawa | Wymień apteki w centrum Warszawy. |
| 10b | | Płock | Wymień apteki w centrum Płocka. |

W wariancie 9c nie ma nazwy miasta. Sprawdzamy, czy model zakłada Warszawę.

## Część 2d: „duże” i „małe” — 6 wariantów, 18 wywołań

Odczytujemy, jak model rozumie „duży” i „mały”: czy przyjmuje próg powierzchni, zwraca kilka skrajnych obiektów, czy robi to inaczej. Litera oznacza miasto: a = Warszawa, b = Radom, c = Płock.

| # | Cecha | Wariant | Pytanie |
|---|---|---|---|
| 11a | duże | Warszawa | Wymień duże parki w Warszawie. |
| 11b | | Radom | Wymień duże parki w Radomiu. |
| 11c | | Płock | Wymień duże parki w Płocku. |
| 12a | małe | Warszawa | Wymień małe parki w Warszawie. |
| 12b | | Radom | Wymień małe parki w Radomiu. |
| 12c | | Płock | Wymień małe parki w Płocku. |

Pary 11 i 12 pokazują, czy model trzyma jeden spójny próg, czy dla każdego przypadku wymyśla go osobno. Trzy miasta różnej wielkości pokazują, czy próg skaluje się z miastem.

## Do uzupełnienia

Jeden wiersz na wariant. „Przyjęta wartość” to promień w metrach w częściach 2a i 2b, użyty obszar w części 2c i próg w części 2d. W „Opisie” wpisujemy luźne spostrzeżenia: co model napisał w uwagach, czy odpowiedzi w powtórzeniach się różniły, co zwróciło uwagę.

| # | Przyjęta wartość | Rodzaj interpretacji | Liczba wyników | Opis |
|---|---|---|---|---|
| 1a | — | — | — | — |
| 1b | — | — | — | — |
| 1c | — | — | — | — |
| 1d | — | — | — | — |
| 2a | — | — | — | — |
| 2b | — | — | — | — |
| 2c | — | — | — | — |
| 3a | — | — | — | — |
| 3b | — | — | — | — |
| 3c | — | — | — | — |
| 4a | — | — | — | — |
| 4b | — | — | — | — |
| 4c | — | — | — | — |
| 5a | — | — | — | — |
| 5b | — | — | — | — |
| 5c | — | — | — | — |
| 6a | — | — | — | — |
| 6b | — | — | — | — |
| 6c | — | — | — | — |
| 7a | — | — | — | — |
| 7b | — | — | — | — |
| 7c | — | — | — | — |
| 8a | — | — | — | — |
| 8b | — | — | — | — |
| 8c | — | — | — | — |
| 8d | — | — | — | — |
| 9a | — | — | — | — |
| 9b | — | — | — | — |
| 9c | — | — | — | — |
| 10a | — | — | — | — |
| 10b | — | — | — | — |
| 11a | — | — | — | — |
| 11b | — | — | — | — |
| 11c | — | — | — | — |
| 12a | — | — | — | — |
| 12b | — | — | — | — |
| 12c | — | — | — | — |
