# PB2: sposób oceny

Na spotkaniu 20.11 hipotezę H2 zamieniliśmy na **pytanie badawcze PB2**: *jak model interpretuje niejasne określenia przestrzenne i nazwy potoczne oraz czy kontekst pytania zmienia wartość, którą przyjmuje?*

Co to zmienia w ocenie:
- **Nie rozstrzygamy hipotezy** i **nie robimy testów statystycznych.** Analizujemy, co wyszło: jakie wartości model przyjął, jak się zmieniają między wariantami i jak bardzo różnią się między powtórzeniami.
- **Zmienne zostały te same:** sytuacja pytającego (S), miejsce (M), rodzaj i skala obiektu (O), miasto. Doszły część 2e (nazwy potoczne, po spotkaniu 20.11), część 2f (dodatkowe kontrasty) i część 2g (próba naprawy błędów z 2e jedną wskazówką w kontekście).
- **10 powtórzeń na wariant.** Dlaczego 10, a nie 5: [opracowanie.md](opracowanie.md#11-5-czy-10-powtórzeń).
- **W części 2e oceniamy trafienie obiektu,** bo tam istnieje dobra odpowiedź. Szukamy dużych pomyłek (uwaga ze spotkania).

Pytania: [pytania.md](pytania.md). Kod: `python/console/run_h2.py` i pakiet `python/console/h2/`. Wyniki: [opracowanie.md](opracowanie.md), tabele generowane automatycznie: [wyniki/tabele.md](wyniki/tabele.md).

## Pojęcia

- **Próba** to jedno wywołanie modelu dla jednego wariantu, bez historii rozmowy.
- **Czynnik** to element kontekstu pytania, który może zmienić wartość przyjętą przez model:
  - **S, sytuacja pytającego:** brak informacji, pieszo, rowerem albo samochodem,
  - **M, miejsce:** centrum Warszawy, peryferie Warszawy albo małe miasto,
  - **O, rodzaj i skala obiektu:** szukany obiekt (apteka albo szpital) albo punkt odniesienia (kiosk albo lotnisko).
- **Przyjęta wartość** to wartość, którą model musiał sam wybrać. Odczytujemy ją z wygenerowanego SQL:

| Rodzaj interpretacji | Przyjęta wartość | Jednostka | Skąd w SQL |
|---|---|---|---|
| `PROMIEŃ` | odległość od punktu odniesienia | m | trzeci argument `ST_DWithin`, warunek `ST_Distance(...) < x` (także przez alias), promień `ST_Buffer`; proste wyrażenia, np. `15 * 5000 / 60`, są wyliczane |
| `K_NAJBLIŻSZYCH` | liczba zwracanych obiektów | szt. | `ORDER BY ... LIMIT k`, gdy nie ma promienia |
| `OBSZAR` | powierzchnia obszaru, w którym szukamy | m² | granica jednostki administracyjnej albo `ST_MakeEnvelope` |
| `PRÓG` | próg wielkości obiektu | m² | warunek `ST_Area(...) > x` lub `< x`, także przez alias i po przeliczeniu z ha |
| `K_SKRAJNYCH` / `WZGLĘDNY` | k największych albo próg względny | – | `ORDER BY ST_Area ... LIMIT k`, `avg`, `percentile`, `ntile` |
| `ODLEGŁOŚĆ` / `LICZBA` | wynik zapytania (część 2e) | m / szt. | pierwsza liczba w pierwszym wierszu wyniku |
| `BRAK_SQL` | model odmówił (pusty SQL) | – | powód w `uwagi` |
| `PUSTY_WYNIK` | zapytanie wykonało się, ale zwróciło 0 wierszy (część 2e) | – | – |
| `INNY` | nie dało się odczytać automatycznie | – | przegląd ręczny, decyzja w `wyniki/korekty.json` |

- **Ujawnienie założenia:** pole `uwagi` podaje liczbę z jednostką (m, km, ha, minuty, km/h) albo słowa takie jak „przyjęto”, „założono”, „interpretacja”.

## Odczyt i jego kontrola

1. `run_h2.py extract` odczytuje wartości automatycznie (`h2/extract.py`).
2. Każdy odczyt przeglądamy razem z fragmentem SQL, z którego pochodzi (`run_h2.py show <wariant>`).
3. Ręczne poprawki trafiają wyłącznie do `wyniki/korekty.json`, razem z `sql_sha` (skrypt odrzuca korektę, gdy SQL się zmienił) i uzasadnieniem. Nie poprawiamy odczytów w kodzie pod konkretną próbę.
4. **Pusty wynik przy pytaniu z promieniem:** skrypt wykonuje zapytanie jeszcze raz z promieniem 10⁸ m. Jeśli dalej nic nie zwraca, zawiódł punkt odniesienia (np. stacja szukana ze złym `fclass`), a nie mały promień.
5. **Pusty wynik w 2e:** skrypt wykonuje każde podzapytanie osobno i podaje, które nic nie znajduje: obiekt z pytania czy PKiN.

## Jak porównujemy warianty

Dla pary wariantów (A, B) podajemy:
- **mediany** przyjętych wartości i **iloraz** mediana B / mediana A,
- **rozkład** wartości z powtórzeń, np. „500 ×8, 1000 ×2”,
- czy **zakresy są rozłączne**, czyli każda wartość B jest większa (albo mniejsza) od każdej wartości A.

Słowny opis zmiany:

| Opis | Kiedy |
|---|---|
| `ROŚNIE` | mediana B ≥ 1,25 × mediana A |
| `MALEJE` | mediana B ≤ mediana A / 1,25 |
| `BEZ_ZMIANY` | pomiędzy |
| `ZMIANA_INTERPRETACJI` | dominujący rodzaj interpretacji w A i B jest inny, np. promień i k najbliższych |
| `NIESTABILNY` | w jednym z wariantów mniej niż 60% prób ma ten sam rodzaj interpretacji z odczytaną wartością (np. model często odmawia) |

**Dlaczego 1,25:** model używa okrągłych wartości (300, 500, 800, 1000, 1500, 2000, 3000, 5000 m). Najmniejszy krok między nimi, 800 → 1000, daje iloraz 1,25. Próg odrzuca więc różnice w obrębie jednej „półki”, a przepuszcza przejście na następną. Wyniki podajemy też przy progach 1,5 i 2 (tabela wrażliwości).

### Pary dla czynników S, M i O

Pary różnią się **tylko** jednym czynnikiem. Zdroworozsądkowy kierunek to B > A: większa wartość przy szybszym środku transportu, w okolicy o mniejszej gęstości obiektów i przy obiekcie większej skali.

| Czynnik | Pary (A → B) | Liczba |
|---|---|---|
| **S: sytuacja pytającego** | 1b→1c, 2b→2c, 3b→3c, 4b→4c, 5b→5c, 6b→6c, 7b→7c, 8b→8d, 8d→8c | 9 |
| **M: miejsce** | 1x→3x, 1x→5x, 2x→4x dla x ∈ {a, b, c} | 9 |
| **O: rodzaj i skala obiektu** | 1x→2x, 3x→4x, 6x→7x dla x ∈ {a, b, c} | 9 |

Dla czynnika podajemy, w ilu parach wartość rośnie, nie zmienia się albo maleje, i ile par odpadło. Do tego słowny opis:

| Opis | Kiedy |
|---|---|
| **wyraźny wpływ** | wartość rośnie w co najmniej 2/3 par, które zostały |
| **częściowy wpływ** | rośnie w 1/3–2/3 par |
| **brak wyraźnego wpływu** | rośnie w mniej niż 1/3 par |
| **wpływ przeciwny do oczekiwań** | maleje w co najmniej 2/3 par |
| **za mało danych** | zostało mniej niż połowa par |

### Pary opisowe (bez oczekiwanego kierunku)

- 1a i 1d: „w pobliżu” i „niedaleko”,
- 1a, 1b i 1e: sytuacja, z której trzeba wywnioskować pośpiech,
- 8a z 8b, 8c i 8d: domyślny środek transportu,
- Na→Nb i Na→Nc dla N = 1…7: gdzie leży wartość domyślna między „pieszo” a „samochodem”,
- 9a, 9b, 9c oraz 10a, 10b: „centrum” w różnych miastach,
- 11a, 11b, 11c oraz 12a, 12b, 12c: progi „duży” i „mały”,
- część 2f:
  - gradient miejscowości: Warszawa → Radom → Siedlce → Tłuszcz → Celestynów → Krusze,
  - wieś i samochód,
  - siła określenia,
  - sytuacje do wywnioskowania,
  - język pytania.

## Części 2e i 2g: ocena obiektu

**Identyfikacja obiektu** (`h2/identify.py`) dotyczy pytań 13 i 15–20 oraz ich odpowiedników w 2g. Dla każdego obiektu w bazie, którego nazwa zawiera rdzeń z pytania („azienk”, „chopin”, „syren”, „kopernik”, „zygmunt”, „palm”, „powsta”), skrypt liczy odległość do PKiN w każdej kombinacji geometrii:
- obiekt: geometria, środek, punkt wewnątrz,
- PKiN: punkt, poligon, środek poligonu, punkt w poligonie, obrys budynku, środek budynku.

Wynik modelu przypisujemy do obiektu, który daje tę samą odległość z dokładnością do 2 m. Gdy pasuje kilka obiektów, decyduje najbliższe dopasowanie. Ocena wynika z osm_id i położenia obiektu:
- właściwy osm_id → `poprawny` (albo `dopuszczalny`),
- inny obiekt poza Warszawą → `duża_pomyłka`,
- inny obiekt w Warszawie, który jest pomnikiem lub atrakcją → `pomyłka`,
- inny obiekt w Warszawie innego rodzaju (szkoła, apteka, lokal) → `duża_pomyłka`.

Dla „pomnika Syrenki nad Wisłą” (16b, 33) właściwa jest tylko syrena na bulwarach. Dla „Syrenki Warszawskiej” (16a, 32) obie syreny: na Rynku i nad Wisłą.

**Lista kandydatów** (`h2/references.py`) zostaje dla pytań 14, 21 i 22 (dwa obszary, metro, liczba kawiarni) oraz dla wyników, których nie da się przypisać do jednego obiektu, np. środka ciężkości wielu obiektów naraz. Wynik przypisujemy do najbliższego kandydata, jeśli różni się od niego najwyżej o max(40 m, 4%). W 22a dopuszczamy ±3 obiekty. Przy każdym dopasowaniu z różnicą powyżej 5 m czytamy SQL.

| Ocena | Znaczenie |
|---|---|
| `poprawny` | właściwy obiekt; odległość od obrysu i od środka są obie poprawne |
| `dopuszczalny` | obiekt, który też można uznać za odpowiedź |
| `pomyłka` | inny obiekt w tym samym mieście |
| `duża_pomyłka` | obiekt w innym mieście albo zupełnie inny |
| `pusty` | 0 wierszy; przyczyna z diagnozy podzapytań |
| `nierozpoznany` | wynik nie pasuje do żadnego kandydata, więc przegląd ręczny |

## Część 2g: próba naprawy

Pytania 30–39 są identyczne z 15a, 15b, 16a, 16b, 17a, 18, 19, 20, 13a i 21a. Kontekst to K2 z dopisanym na końcu jednym akapitem o wyszukiwaniu po nazwie (pełny tekst w [pytania.md](pytania.md#część-2g-próba-naprawy-wyszukiwania-po-nazwie--10-wariantów) i w `h2/generate.py`). Porównujemy rozkład ocen obiektu (dobry, pusty, pomyłka, duża pomyłka, odmowa) z odpowiednikiem w 2e. Dwa ostatnie pytania (Łazienki, metro) to kontrola, czy wskazówka nie psuje tego, co działało.

## Replikacja

Oprócz serii głównej jest seria kontrolna z 24.11: 2 próby na każdy z 56 pierwszych wariantów (`wyniki/replikacja.jsonl`). Nie wchodzi do analizy. Sprawdza tylko, czy wartości powtarzają się w osobnym uruchomieniu.

## Ograniczenia

- **Powtórzenia nie są niezależnymi „ludźmi”.** Model jest prawie deterministyczny i często zwraca tę samą wartość we wszystkich próbach. Powtórzenia pokazują rozrzut, ale prawdziwą jednostką porównania jest para pytań.
- **Czynniki nie są idealnie rozdzielone:**
  - „Miejsce” zmienia jednocześnie gęstość okolicy i rodzaj stacji,
  - „Rodzaj obiektu” zmienia jednocześnie skalę i rzadkość (szpitali jest mniej niż aptek).
- **Próg 1,25 jest arbitralny.** Pokazujemy wrażliwość na próg.
- **Jeden model (`claude-sonnet-5-5`, effort `medium`), jeden poziom kontekstu (K2), jeden region.**
