# H2: pytania

Sprawdzamy, czy zmiana kontekstu pytania, bez zmiany jego formy ani samego niejasnego określenia, wpływa na to, jak model je zinterpretuje. Każda część bierze inne określenie, a kolumny w tabelach pokazują, co w niej zmieniamy.

29 pytań × 3 powtórzenia = 87 wywołań, wszystkie przy kontekście K2. Model odpowiada w ustrukturyzowanej formie: zapytanie SQL i miejsce na uwagi.

## Część 2a: „w pobliżu” — 13 pytań, 39 wywołań

Odczytujemy przyjęty promień w metrach oraz rodzaj interpretacji: promień, k najbliższych (`ORDER BY ... LIMIT`), obszar administracyjny albo inny.

| # | Miejsce | Obiekt | Sytuacja | Pytanie |
|---|---|---|---|---|
| 1 | centrum | apteki | brak | Wymień apteki w pobliżu Dworca Centralnego. |
| 2 | centrum | apteki | pieszo | Idę pieszo. Wymień apteki w pobliżu Dworca Centralnego. |
| 3 | centrum | apteki | samochodem | Jadę samochodem. Wymień apteki w pobliżu Dworca Centralnego. |
| 4 | centrum | szpitale | brak | Wymień szpitale w pobliżu Dworca Centralnego. |
| 5 | centrum | szpitale | pieszo | Idę pieszo. Wymień szpitale w pobliżu Dworca Centralnego. |
| 6 | centrum | szpitale | samochodem | Jadę samochodem. Wymień szpitale w pobliżu Dworca Centralnego. |
| 7 | peryferie | apteki | brak | Wymień apteki w pobliżu stacji Warszawa Płudy. |
| 8 | peryferie | apteki | pieszo | Idę pieszo. Wymień apteki w pobliżu stacji Warszawa Płudy. |
| 9 | peryferie | apteki | samochodem | Jadę samochodem. Wymień apteki w pobliżu stacji Warszawa Płudy. |
| 10 | peryferie | szpitale | brak | Wymień szpitale w pobliżu stacji Warszawa Płudy. |
| 11 | peryferie | szpitale | pieszo | Idę pieszo. Wymień szpitale w pobliżu stacji Warszawa Płudy. |
| 12 | peryferie | szpitale | samochodem | Jadę samochodem. Wymień szpitale w pobliżu stacji Warszawa Płudy. |
| 13 | centrum | apteki | brak | Wymień apteki niedaleko Dworca Centralnego. |

Pytanie 13 to kontrola: to samo co pytanie 1, ale z określeniem „niedaleko”.

## Część 2b: czas dojazdu — 5 pytań, 15 wywołań

Odczytujemy przyjęty promień oraz wynikającą z niego prędkość.

| # | Sytuacja | Pytanie |
|---|---|---|
| 14 | brak | Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |
| 15 | pieszo | Idę pieszo. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |
| 16 | rowerem | Jadę rowerem. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |
| 17 | samochodem | Jadę samochodem. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |
| 18 | poza miasto | Wymień jeziora, do których dojadę z Warszawy w godzinę. |

Pytanie 18 jest w innej skali: promień idzie w dziesiątki kilometrów, a punktem odniesienia jest całe miasto, a nie jeden obiekt. Dane obejmują tylko mazowieckie, więc wynik może być ucięty granicą województwa.

## Część 2c: „w centrum” — 5 pytań, 15 wywołań

Odczytujemy, czym model zastąpił „centrum”: granicą dzielnicy, promieniem wokół jakiegoś obiektu czy prostokątem współrzędnych, i jaką to daje powierzchnię.

| # | Miasto | Pytanie |
|---|---|---|
| 19 | Warszawa | Wymień kawiarnie w centrum Warszawy. |
| 20 | Płock | Wymień kawiarnie w centrum Płocka. |
| 21 | Warszawa | Wymień apteki w centrum Warszawy. |
| 22 | Płock | Wymień apteki w centrum Płocka. |
| 23 | brak | Wymień kawiarnie w centrum. |

W pytaniu 23 nie ma nazwy miasta. Sprawdzamy, czy model zakłada Warszawę.

## Część 2d: „duże” i „małe” — 6 pytań, 18 wywołań

Odczytujemy, jak model rozumie „duży” i „mały”: czy przyjmuje próg powierzchni, zwraca kilka skrajnych obiektów, czy robi to inaczej.

| # | Cecha | Miasto | Pytanie |
|---|---|---|---|
| 24 | duże | Warszawa | Wymień duże parki w Warszawie. |
| 25 | duże | Radom | Wymień duże parki w Radomiu. |
| 26 | duże | Płock | Wymień duże parki w Płocku. |
| 27 | małe | Warszawa | Wymień małe parki w Warszawie. |
| 28 | małe | Radom | Wymień małe parki w Radomiu. |
| 29 | małe | Płock | Wymień małe parki w Płocku. |

Pary „duże” i „małe” pokazują, czy model trzyma jeden spójny próg, czy dla każdego przypadku wymyśla go osobno. Trzy miasta różnej wielkości pokazują, czy próg skaluje się z miastem.

## Do uzupełnienia

Jeden wiersz na pytanie. „Przyjęta wartość” to promień w metrach w częściach 2a i 2b, użyty obszar w części 2c i próg w części 2d. W „Opisie” wpisujemy luźne spostrzeżenia: co model napisał w uwagach, czy odpowiedzi w powtórzeniach się różniły, co zwróciło uwagę.

| # | Przyjęta wartość | Rodzaj interpretacji | Liczba wyników | Opis |
|---|---|---|---|---|
| 1 | — | — | — | — |
| 2 | — | — | — | — |
| 3 | — | — | — | — |
| 4 | — | — | — | — |
| 5 | — | — | — | — |
| 6 | — | — | — | — |
| 7 | — | — | — | — |
| 8 | — | — | — | — |
| 9 | — | — | — | — |
| 10 | — | — | — | — |
| 11 | — | — | — | — |
| 12 | — | — | — | — |
| 13 | — | — | — | — |
| 14 | — | — | — | — |
| 15 | — | — | — | — |
| 16 | — | — | — | — |
| 17 | — | — | — | — |
| 18 | — | — | — | — |
| 19 | — | — | — | — |
| 20 | — | — | — | — |
| 21 | — | — | — | — |
| 22 | — | — | — | — |
| 23 | — | — | — | — |
| 24 | — | — | — | — |
| 25 | — | — | — | — |
| 26 | — | — | — | — |
| 27 | — | — | — | — |
| 28 | — | — | — | — |
| 29 | — | — | — | — |
