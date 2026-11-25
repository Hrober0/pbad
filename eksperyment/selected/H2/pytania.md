# PB2: pytania

**Pytanie badawcze PB2:** jak model interpretuje niejasne określenia przestrzenne i nazwy potoczne oraz czy kontekst pytania zmienia wartość, którą przyjmuje? (Na spotkaniu 20.11 hipotezę H2 zamieniliśmy na pytanie badawcze. Zmienne zostały te same, zmienił się sposób oceny: opisujemy efekty i nie rozstrzygamy hipotezy, patrz [ocena.md](ocena.md).)

Sprawdzamy, czy zmiana kontekstu pytania, bez zmiany jego formy ani samego niejasnego określenia, wpływa na to, jak model je zinterpretuje. Każda część dotyczy innego określenia, a kolumny w tabelach pokazują, co w niej zmieniamy. Część 2e dochodzi po spotkaniu 20.11. Sprawdzamy w niej, czy model dobrze rozpoznaje miejsca podane nazwą potoczną, i szukamy dużych pomyłek. Część 2f (eksploracja) dodaliśmy po pierwszej serii, żeby sprawdzić, czy na wsi albo w małym mieście „w pobliżu” oznacza większy promień niż w Warszawie. Przy okazji sprawdza też siłę samego określenia, sytuacje do wywnioskowania i język pytania. Część 2g sprawdza, czy błędy z 2e da się usunąć jedną ogólną wskazówką w kontekście.

**Numeracja:**
- **Numer** oznacza jedno pytanie bazowe, np. „apteki w pobliżu Dworca Centralnego”.
- **Litera** oznacza wariant tego pytania. Znaczenie liter jest podane w każdej części.

Wyniki porównujemy przede wszystkim między wariantami tego samego numeru, np. 1a, 1b i 1c. Porównania między numerami są wypisane pod tabelą każdej części.

**84 warianty × 10 powtórzeń = 840 wywołań,** wszystkie przy kontekście K2 (w części 2g K2 z dopisaną jedną wskazówką). Model odpowiada w ustrukturyzowanej formie: zapytanie SQL i pole na uwagi. Uruchomienie: `python/console/run_h2.py`. Wyniki i ich opracowanie: [opracowanie.md](opracowanie.md).

Powtórzeń jest 10. Pierwsza seria z 24.11 miała 5, ale przy 5 próbach mediana bywała przypadkowa (5 z 56 wariantów z przyjętą wartością zmieniło medianę po dołożeniu prób 6–10) i nie było widać rzadkich dużych pomyłek. Szczegóły w [opracowanie.md](opracowanie.md).

## Część 2a: „w pobliżu” — 23 warianty

Odczytujemy przyjęty promień w metrach oraz rodzaj interpretacji: promień, k najbliższych (`ORDER BY ... LIMIT`), obszar administracyjny albo inny.

**Warianty:**

| Litera | Wariant |
|---|---|
| a | brak informacji o sposobie poruszania się |
| b | „Idę pieszo.” |
| c | „Jadę samochodem.” |
| d | „niedaleko” zamiast „w pobliżu”, bez informacji o sposobie poruszania się |
| e | sytuacja, z której trzeba wywnioskować pośpiech: „Mam 10 minut do odjazdu pociągu.” (rozszerzenie z planu) |

| # | Szukane | Punkt odniesienia | Wariant | Pytanie |
|---|---|---|---|---|
| 1a | apteki | Dworzec Centralny (centrum Warszawy) | brak | Wymień apteki w pobliżu Dworca Centralnego. |
| 1b | | | pieszo | Idę pieszo. Wymień apteki w pobliżu Dworca Centralnego. |
| 1c | | | samochodem | Jadę samochodem. Wymień apteki w pobliżu Dworca Centralnego. |
| 1d | | | „niedaleko” | Wymień apteki niedaleko Dworca Centralnego. |
| 1e | | | pośpiech | Mam 10 minut do odjazdu pociągu. Wymień apteki w pobliżu Dworca Centralnego. |
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

## Część 2b: czas dojazdu — 4 warianty

Odczytujemy przyjęty promień oraz wynikającą z niego prędkość. Litery a, b i c znaczą to samo co w części 2a, a d oznacza jazdę rowerem.

| # | Wariant | Pytanie |
|---|---|---|
| 8a | brak | Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |
| 8b | pieszo | Idę pieszo. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |
| 8c | samochodem | Jadę samochodem. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |
| 8d | rowerem | Jadę rowerem. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |

## Część 2c: „w centrum” — 5 wariantów

Odczytujemy, czym model zastąpił „centrum”: granicą dzielnicy, promieniem wokół jakiegoś obiektu czy prostokątem współrzędnych, i jaką to daje powierzchnię. Litera oznacza miasto: a = Warszawa, b = Płock, c = bez nazwy miasta.

| # | Szukane | Wariant | Pytanie |
|---|---|---|---|
| 9a | kawiarnie | Warszawa | Wymień kawiarnie w centrum Warszawy. |
| 9b | | Płock | Wymień kawiarnie w centrum Płocka. |
| 9c | | bez miasta | Wymień kawiarnie w centrum. |
| 10a | apteki | Warszawa | Wymień apteki w centrum Warszawy. |
| 10b | | Płock | Wymień apteki w centrum Płocka. |

W wariancie 9c nie ma nazwy miasta. Sprawdzamy, czy model zakłada Warszawę.

## Część 2d: „duże” i „małe” — 6 wariantów

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

## Część 2e: miejsca podane nazwą potoczną — 18 wariantów

Pomysły ze spotkania 20.11: „Łazienki” i „Łazienki Królewskie”, stacja metra bez podanej nazwy, pomnik Chopina, Syrenka. Pytania są tak ułożone, żeby wynik był liczbą (odległością albo liczbą obiektów). Z samej liczby da się wtedy odczytać, który obiekt model wybrał, i porównać ją z tabelą kandydatów poniżej. Interesują nas przede wszystkim **duże pomyłki**, czyli wybór innego obiektu, a nie różnice rzędu kilkudziesięciu metrów.

Litera a oznacza wersję potoczną, a litera b wersję doprecyzowaną. Pytania 18–20 mają tylko jedną wersję i służą jako kontrola: to obiekty, których nazwa w bazie jest taka sama jak potoczna.

| # | Obiekt | Wariant | Pytanie |
|---|---|---|---|
| 13a | Łazienki → PKiN | potocznie | Jak daleko w linii prostej w metrach jest z Łazienek do Pałacu Kultury i Nauki? |
| 13b | | pełna nazwa | Jak daleko w linii prostej w metrach jest z Łazienek Królewskich do Pałacu Kultury i Nauki? |
| 14a | Łazienki → Pole Mokotowskie | potocznie | Jak daleko w linii prostej w metrach jest z Łazienek do Pola Mokotowskiego? |
| 14b | | pełna nazwa | Jak daleko w linii prostej w metrach jest z Łazienek Królewskich do Pola Mokotowskiego? |
| 15a | pomnik Chopina → PKiN | potocznie | Jak daleko w linii prostej w metrach jest od pomnika Chopina do Pałacu Kultury i Nauki? |
| 15b | | z miejscem | Jak daleko w linii prostej w metrach jest od pomnika Chopina w Łazienkach do Pałacu Kultury i Nauki? |
| 16a | Syrenka → PKiN | potocznie | Jak daleko w linii prostej w metrach jest od Syrenki Warszawskiej do Pałacu Kultury i Nauki? |
| 16b | | z miejscem | Jak daleko w linii prostej w metrach jest od pomnika Syrenki nad Wisłą do Pałacu Kultury i Nauki? |
| 17a | pomnik Kopernika → PKiN | potocznie | Jak daleko w linii prostej w metrach jest od pomnika Kopernika do Pałacu Kultury i Nauki? |
| 17b | | z miejscem | Jak daleko w linii prostej w metrach jest od pomnika Mikołaja Kopernika na Krakowskim Przedmieściu do Pałacu Kultury i Nauki? |
| 18 | Kolumna Zygmunta → PKiN | kontrola | Jak daleko w linii prostej w metrach jest od Kolumny Zygmunta do Pałacu Kultury i Nauki? |
| 19 | palma → PKiN | kontrola | Jak daleko w linii prostej w metrach jest od palmy na rondzie de Gaulle'a do Pałacu Kultury i Nauki? |
| 20 | Mały Powstaniec → PKiN | kontrola | Jak daleko w linii prostej w metrach jest od pomnika Małego Powstańca do Pałacu Kultury i Nauki? |
| 21a | najbliższa stacja metra | od PKiN | Jak daleko w metrach jest od Pałacu Kultury i Nauki do najbliższej stacji metra i jak się ona nazywa? |
| 21b | | od Łazienek | Jak daleko w metrach jest od Łazienek Królewskich do najbliższej stacji metra i jak się ona nazywa? |
| 22a | stacja metra bez nazwy | liczba | Ile kawiarni w Warszawie jest w odległości do 200 metrów od stacji metra? |
| 22b | | „w pobliżu” | Wymień kawiarnie w pobliżu stacji metra. |
| 22c | | z nazwą stacji | Wymień kawiarnie w pobliżu stacji metra Centrum. |

### Kandydaci w bazie i odległości wzorcowe

Wszystkie odległości policzone na zrzucie z 2026-11-20, w metrach, na typie `geography`. PKiN występuje w bazie jako punkt (`pois`, `viewpoint`) i jako poligon (`pois_a`, `attraction`). Podajemy obie odległości, bo model może wybrać jedno albo drugie i obie odpowiedzi są dopuszczalne.

| # | Kandydat w bazie | Tabela, `fclass`, `name` | do PKiN (punkt / poligon) | Ocena |
|---|---|---|---|---|
| 13 | Łazienki Królewskie (obrys parku) | `landuse`/`pois_a`, `park`, „Łazienki Królewskie” | 2194 / 2041 od obrysu; 2773 / 2778 od środka | **poprawny** |
| 13 | Pałac na Wyspie | `pois_a`, `castle`, „Pałac na Wyspie” | 2707 | dopuszczalny |
| 13 | przysiółek Łazienki (gmina Gielniów, powiat przysuski) | `places`, `hamlet`, „Łazienki” | ok. 98 700 | **duża pomyłka** |
| 14 | Łazienki ↔ Pole Mokotowskie (dwa parki) | `landuse`, `park` | 754 między obrysami; 2195 między środkami | obie poprawne, to różnica interpretacji |
| 15 | pomnik Chopina w Łazienkach | `pois_a`, `memorial`, „Fryderyk Chopin” | 2416 / 2264 | **poprawny** |
| 15 | „Pomnik Fryderyka Chopina” | `pois`, `memorial`, **w Radomiu** | 93 225 | **duża pomyłka** |
| 15 | „Pomnik Fryderka Chopina” (literówka w OSM) | `pois`, `memorial`, powiat sochaczewski | 51 727 | **duża pomyłka** |
| 15 | ławeczki Chopina, inne „Fryderyk Chopin” | `pois`, `bench`/`attraction`/`memorial` | 0,7–8 km w Warszawie, 49–54 km pod Sochaczewem | pomyłka |
| 16 | Syrenka na Rynku Starego Miasta | `pois_a`, `memorial`, „Syrenka Warszawska” | 2039 / 1893 | poprawny dla 16a |
| 16 | Syrena nad Wisłą (Bulwary) | `pois_a`, `memorial`, „Syrena” | 1997 / 1900 | **poprawny dla 16b**, dopuszczalny dla 16a |
| 16 | inne „Syrenka”/„Syrena” | `pois`, `artwork` | 837; 3980; 57 513; 64 318 | pomyłka |
| 17 | pomnik Kopernika na Krakowskim Przedmieściu | `pois`, `memorial`, „Mikołaj Kopernik” | 1067 / 949 | **poprawny** |
| 17 | rzeźba Kopernika przy wejściu do PKiN | `pois`, `artwork`, „Mikołaj Kopernik” | 52 / 4 | **duża pomyłka** (obiekt przy samym PKiN) |
| 17 | Centrum Nauki Kopernik | `pois_a`, `museum` | 1860 / 1746 | pomyłka |
| 18 | Kolumna Zygmunta | `pois_a`, `monument`/`attraction` | 1781 / 1636 | poprawny |
| 19 | palma | `pois`, `artwork`, „Palma” | 998 / 881 | poprawny |
| 20 | Mały Powstaniec | `pois`, `memorial`, „Mały Powstaniec” | 1956 / 1809 | poprawny |
| 21a | Centrum (metro) | `transport`, `railway_station` | 283 / 147 | **poprawny** |
| 21a | Warszawa Śródmieście (kolej, nie metro) | `transport`, `railway_station` | 284 | pomyłka (to nie metro) |
| 21b | Politechnika (metro) | `transport`, `railway_station` | 797 od obrysu parku; 1387 od środka | **poprawny** |
| 22a | 39 stacji metra w Warszawie (stacje przy torach `subway`) | `transport`, `railway_station` | **72** kawiarnie | **poprawny** |
| 22a | wszystkie `railway_station` w Warszawie (metro + kolej) | | 111 | pomyłka: to nie tylko metro |
| 22a | wszystkie `railway_station` w województwie | | 115 | pomyłka |
| 22c | stacja Centrum | `transport`, `railway_station`, „Centrum” | 15 kawiarni w 300 m, 44 w 500 m | – |

**Kandydaci dopisani przy przeglądzie wyników** (każdy wynik model sprawdzaliśmy w SQL; pełna lista: `python/console/h2/references.py`):

| # | Kandydat | Odległość | Ocena |
|---|---|---|---|
| 13 | środek Łazienek → obrys poligonu PKiN | 2619 | poprawny |
| 14 | środek Pola Mokotowskiego → obrys Łazienek | 1734 | poprawny |
| 15 | „Fortepian Chopina” (`memorial`, ok. 1 km od PKiN) → środek poligonu PKiN (punkt PKiN: 1009, punkt w poligonie: 1038) | 1032 | pomyłka |
| 16 | apteka „Syrenka” (pierwszy punkt `%Syrenk%` bez warunku na `fclass`) | 1935 | duża pomyłka |
| 16 | środek ciężkości wszystkich obiektów `%Syrenk%` w województwie (`ST_Centroid(ST_Collect(...))`) | 31 755 | duża pomyłka |
| 17 | pomnik Kopernika → środek budynku PKiN | 1090 | poprawny |
| 19 | palma → środek poligonu PKiN | 1018 | poprawny |
| 19 | środek ciężkości wszystkich punktów `%palma%` | 3889 | duża pomyłka |
| 20 | Mały Powstaniec → środek poligonu PKiN | 1969 | poprawny |
| 21a | Centrum → punkt wewnątrz poligonu PKiN | 311 | poprawny |

**Co sprawdzamy w części 2e:**
- **13a i 13b:** czy samo „Łazienki” trafia w przysiółek pod Przysuchą (`name = 'Łazienki'`) i czy model liczy odległość od obrysu parku, czy od jego środka,
- **14a i 14b:** jak model rozumie odległość między dwoma obszarami: między obrysami (754 m) czy między środkami (2195 m),
- **15a:** pod nazwą „Pomnik Fryderyka Chopina” w bazie jest tylko pomnik w Radomiu, a pomnik w Łazienkach nazywa się „Fryderyk Chopin”. Wyszukiwanie po słowie „pomnik” daje błąd o 90 km,
- **16a i 16b:** która z dwóch syren jest „Syrenką Warszawską”,
- **17a:** czy model zna pomnik na Krakowskim Przedmieściu, czy trafi w rzeźbę przy PKiN, co da odległość ok. 50 m,
- **18–20:** kontrola na obiektach, których nazwa w bazie jest taka sama jak potoczna, więc tu spodziewamy się samych trafień,
- **21–22:** jak model rozpoznaje stację metra. W danych metro i kolej mają ten sam `fclass = 'railway_station'`, a K2 mówi, że stację metra rozpoznaje się po bliskości torów `subway`. Sprawdzamy, czy model z tego korzysta i co robi, gdy nie podano nazwy stacji.

## Część 2f: dodatkowe kontrasty (eksploracja) — 18 wariantów

Część dodana po pierwszej serii (24.11). Pytania dobraliśmy tak, żeby sprawdzić zachowania, które pierwsza seria tylko zasygnalizowała. Nie ma tu kierunków oczekiwanych z góry, wyniki opisujemy. Forma zdania jest taka jak w 2a („Wymień apteki w pobliżu …”), żeby wartości dało się zestawić z 1a, 3a i 5a.

**Gradient wielkości miejscowości (23).** Ten sam rodzaj punktu odniesienia (stacja kolejowa, `railway_station`) w miejscowościach od dużego miasta po wieś. Pytamy, czy promień rośnie, gdy miejscowość jest mniejsza, i czy rośnie wystarczająco. Pary z 1a (Warszawa, Dworzec Centralny) i 5a (Tłuszcz).

| # | Miejscowość | Wariant | Pytanie |
|---|---|---|---|
| 23a | Radom (ok. 200 tys.) | duże miasto | Wymień apteki w pobliżu stacji Radom Główny. |
| 23b | Siedlce (ok. 76 tys.) | średnie miasto | Wymień apteki w pobliżu stacji Siedlce. |
| 23c | Celestynów (wieś, ok. 5 tys.) | wieś z aptekami przy stacji | Wymień apteki w pobliżu stacji Celestynów. |
| 23d | Krusze (wieś) | wieś bez apteki w promieniu 5 km | Wymień apteki w pobliżu stacji Krusze. |
| 24 | Krusze | wieś, samochodem | Jadę samochodem. Wymień apteki w pobliżu stacji Krusze. |

Apteki wokół stacji (punkty i poligony, zrzut z 2026-11-20):

| Stacja | w 500 m | w 1 km | w 2 km | w 5 km | najbliższa |
|---|---|---|---|---|---|
| Warszawa Centralna | 7 | 27 | 63 | 236 | 45 m |
| Radom Główny | 6 | 15 | 39 | 66 | 187 m |
| Siedlce | 2 | 12 | 25 | 29 | 316 m |
| Tłuszcz | 5 | 5 | 5 | 5 | 194 m |
| Celestynów | 2 | 3 | 3 | 3 | 158 m |
| Krusze | 0 | 0 | 0 | 0 | 5407 m |

**Siła określenia (25).** Czy inne słowo niż „w pobliżu” zmienia promień? W pierwszej serii „niedaleko” dało to samo co „w pobliżu”.

| # | Określenie | Pytanie |
|---|---|---|
| 25a | bardzo blisko | Wymień apteki bardzo blisko Dworca Centralnego. |
| 25b | w okolicy | Wymień apteki w okolicy Dworca Centralnego. |
| 25c | w zasięgu krótkiego spaceru | Wymień apteki w zasięgu krótkiego spaceru od Dworca Centralnego. |
| 25d | rzut beretem | Wymień apteki rzut beretem od Dworca Centralnego. |
| 26 | „najbliższe” bez liczby | Wymień najbliższe apteki od Dworca Centralnego. |

W 26 nie ma promienia ani liczby, więc sprawdzamy, czy model wybierze `LIMIT k` i jakie k.

**Sytuacja do wywnioskowania (27).** Rozszerzenie 1e: czy model wyciąga wniosek o zasięgu z sytuacji, w której nie pada słowo o środku transportu?

| # | Sytuacja | Pytanie |
|---|---|---|
| 27a | wózek inwalidzki | Poruszam się na wózku inwalidzkim. Wymień apteki w pobliżu Dworca Centralnego. |
| 27b | małe dziecko | Jestem z małym dzieckiem. Wymień apteki w pobliżu Dworca Centralnego. |
| 27c | rower | Jestem na rowerze. Wymień apteki w pobliżu Dworca Centralnego. |
| 27d | pilna potrzeba | Pilnie potrzebuję leków. Wymień apteki w pobliżu Dworca Centralnego. |

**Kontrola sformułowania w gradiencie (29).** W 23 Warszawę reprezentuje „Dworzec Centralny”, a inne miejscowości „stacja X”. Tu pytamy o Warszawę tak samo jak o resztę, żeby oddzielić wpływ sformułowania od wpływu miasta.

| # | Wariant | Pytanie |
|---|---|---|
| 29a | „stacja Warszawa Centralna” | Wymień apteki w pobliżu stacji Warszawa Centralna. |
| 29b | jw., samochodem | Jadę samochodem. Wymień apteki w pobliżu stacji Warszawa Centralna. |

**Język pytania (28).** Ten sam kontekst bazy po polsku, a pytanie po angielsku. Czy zmienia się promień, np. na „pół mili” = 805 m?

| # | Wariant | Pytanie |
|---|---|---|
| 28a | angielski, bez kontekstu | List pharmacies near Warsaw Central railway station. |
| 28b | angielski, samochodem | I'm driving. List pharmacies near Warsaw Central railway station. |

## Część 2g: próba naprawy wyszukiwania po nazwie — 10 wariantów

Sprawdzamy, czy błędy z części 2e da się usunąć jedną ogólną wskazówką w kontekście. Pytania są dokładnie takie same jak ich odpowiedniki w 2e. Zmienia się tylko kontekst: K2 plus jeden akapit dopisany na końcu, który nie wymienia żadnego obiektu z pytań:

> Wskazówka do wyszukiwania obiektów po nazwie: nie zakładaj z góry, w której tabeli i z jakim fclass zapisano dany obiekt. Szukaj go jednocześnie w tabelach punktowych i poligonowych (UNION ALL), bez warunku na fclass. W warunku na nazwę używaj rdzenia nazwy (np. ILIKE '%rdzeń%'), bo nazwy w bazie są zwykle w mianowniku i mogą się różnić od formy użytej w pytaniu. Jeśli nazwie odpowiada kilka obiektów, wybierz jeden konkretny obiekt, który najlepiej pasuje do pytania, i opisz wybór w polu uwagi.

Oceniamy tak samo jak w 2e, tymi samymi kandydatami. Patrzymy na trzy rzeczy:
- czy znikają puste wyniki,
- czy nie przybywa złych obiektów, bo luźniejsze wyszukiwanie może trafiać w aptekę „Syrenka” albo w Radom,
- czy nie psują się pytania, które w 2e szły dobrze (Łazienki, metro).

| # | Odpowiednik w 2e | Pytanie |
|---|---|---|
| 30 | 15a | Jak daleko w linii prostej w metrach jest od pomnika Chopina do Pałacu Kultury i Nauki? |
| 31 | 15b | Jak daleko w linii prostej w metrach jest od pomnika Chopina w Łazienkach do Pałacu Kultury i Nauki? |
| 32 | 16a | Jak daleko w linii prostej w metrach jest od Syrenki Warszawskiej do Pałacu Kultury i Nauki? |
| 33 | 16b | Jak daleko w linii prostej w metrach jest od pomnika Syrenki nad Wisłą do Pałacu Kultury i Nauki? |
| 34 | 17a | Jak daleko w linii prostej w metrach jest od pomnika Kopernika do Pałacu Kultury i Nauki? |
| 35 | 18 | Jak daleko w linii prostej w metrach jest od Kolumny Zygmunta do Pałacu Kultury i Nauki? |
| 36 | 19 | Jak daleko w linii prostej w metrach jest od palmy na rondzie de Gaulle'a do Pałacu Kultury i Nauki? |
| 37 | 20 | Jak daleko w linii prostej w metrach jest od pomnika Małego Powstańca do Pałacu Kultury i Nauki? |
| 38 | 13a | Jak daleko w linii prostej w metrach jest z Łazienek do Pałacu Kultury i Nauki? |
| 39 | 21a | Jak daleko w metrach jest od Pałacu Kultury i Nauki do najbliższej stacji metra i jak się ona nazywa? |

## Część 2h: co model uzna za „metro” — 1 wariant

Pytanie dodane po dyskusji wyników, poza główną serią 840 wywołań (10 prób, kontekst K2 bez wskazówki). Słowo „metro” nie wskazuje stacji. W bazie przy Politechnice są:
- stacja metra „Politechnika” (`transport`, `railway_station`),
- przystanki autobusowe i tramwajowe „Metro Politechnika 01–14” (`bus_stop`, `tram_stop`): słowo „metro” w nazwie, ale to nie metro,
- budynek „Gmach Główny PW” (`buildings`, nazwa skrócona), punkt `tourist_info` „Gmach Główny Politechniki Warszawskiej” i budynek „Gmach Główny SGH”.

Ocena: czytamy SQL i sprawdzamy, który obiekt model wziął jako metro (stacja metra czy przystanek) i który jako Gmach Główny. Odległość sama nie rozstrzyga, bo przystanki „Metro Politechnika” leżą 280–437 m od Gmachu, a stacja 364 m (od obrysu budynku; 424 m od jego środka; 367 m do punktu `tourist_info`).

| # | Wariant | Pytanie |
|---|---|---|
| 40 | „metro” bez nazwy stacji | Jak daleko w linii prostej w metrach jest od metra do Gmachu Głównego Politechniki Warszawskiej? |

## Wyniki

Wyniki dla każdego wariantu (przyjęta wartość, rodzaj interpretacji, liczba wyników, uwagi) są w [opracowanie.md](opracowanie.md), a tabela generowana automatycznie w [wyniki/tabele.md](wyniki/tabele.md).
