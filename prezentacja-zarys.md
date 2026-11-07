# Zarys prezentacji: etap formalny

**Wymagania:**
- 5 minut,
- wysłanie do opiekuna najpóźniej **09.11**,
- prezentacja na Teams.

7 slajdów, ok. 40 sekund na slajd. Każdy slajd odpowiada jednemu punktowi z wytycznych, w tej samej kolejności:

| Punkt z wytycznych | Slajd |
|---|---|
| Kontekst | 1 |
| Co już wiadomo z badań literatury? | 2 |
| Jaka jest hipoteza? | 3 |
| Jakie narzędzia badawcze? | 4 |
| Jakie narzędzia informatyczne? Co wymaga poznania/napisania? | 5 |
| Plan eksperymentu/ów | 6 |
| Dalsze kroki (jaki harmonogram prac?) | 7 |

---

### 1. Kontekst (ok. 40 s)

- Roboczy tytuł: *„Schemat to za mało? Kontekst bazy danych i niejasne pytania przy generowaniu przestrzennego SQL przez LLM”*. Autorzy, opiekun, przedmiot.
- Użytkownik pyta językiem naturalnym, np. „gdzie jest apteka niedaleko dworca?”. LLM tłumaczy pytanie na SQL z funkcjami PostGIS, a obliczenia przestrzenne wykonuje baza.
- **Grafika:** schemat przepływu: pytanie → LLM (+ opis bazy) → SQL → PostGIS → wynik.
- **Do powiedzenia:** są dwa problemy. Model nie zna naszych danych, a ludzie pytają nieprecyzyjnie. Badamy oba.

### 2. Co już wiadomo z badań literatury (ok. 40 s)

- LLM słabo liczą relacje przestrzenne samodzielnie, więc lepiej, żeby tłumaczyły pytanie na zapytanie, a liczyła baza (praca 11).
- Sposób opisu bazy w prompcie wpływa na poprawność SQL, ale więcej informacji nie zawsze daje lepszy wynik (DAIL-SQL, Monkuu, praca 12).
- Poprawna składnia nie oznacza poprawnego wyniku, więc oceniamy wyniki zapytań, a nie ich tekst (GeoSQL-Eval).
- Przy niejasnym pytaniu modele trzymają się jednej interpretacji (AmbiQT).
- **Luka:** badania dotyczą głównie GPT-4 i nie rozdzielają wpływu różnych rodzajów informacji o bazie. Nie wiadomo też, czy interpretacja niejasnych określeń przestrzennych zależy od kontekstu.

### 3. Hipotezy (ok. 40 s)

- **H1:** Opis zawartości danych poprawia trafność zapytań przestrzennych SQL bardziej niż opis struktury bazy danych oraz wskazówki i przykłady zapytań.
- **H2:** Model interpretuje niejasne określenia przestrzenne zależnie od kontekstu pytania, dopasowując przyjęte wartości do rodzaju szukanego obiektu oraz do sytuacji pytającego.
- **Do powiedzenia:**
  - trafność to odsetek zapytań, które zwracają taki sam wynik jak zapytanie wzorcowe,
  - H2 może wyjść w obie strony: model może rozsądnie skalować promień albo zawsze wpisywać to samo.

### 4. Narzędzia badawcze (ok. 40 s)

- **Eksperyment porównawczy:** zmieniamy jeden czynnik, a resztę utrzymujemy stałą. Każda próba to jedno wywołanie modelu bez historii.
- **Eksperyment 1:**
  - trafność względem zapytań wzorcowych, czyli porównanie wyników, a nie tekstu SQL,
  - klasyfikacja błędów, np. zła tabela albo liczenie w stopniach zamiast w metrach.
- **Eksperyment 2:**
  - odczyt przyjętego promienia z SQL,
  - mediana i rozrzut z 10 powtórzeń,
  - klasyfikacja rodzaju interpretacji: promień, k najbliższych albo obszar.
- **Zestaw pytań testowych** w 5 kategoriach zapytań przestrzennych (NALSpatial, GS-SQL).
- **Opcjonalnie:** ankieta wśród ludzi jako punkt odniesienia dla H2.

### 5. Narzędzia informatyczne (ok. 40 s)

**Mamy:**
- dane OSM z Geofabrik dla Mazowsza,
- PostgreSQL 18 + PostGIS 3.6 w Dockerze,
- import przez `ogr2ogr` (GDAL),
- DataGrip i QGIS do podglądu danych.

**Do poznania:**
- Claude API:
  - ustawienia modelu,
  - odpowiedź w ustalonym formacie (JSON),
  - liczenie tokenów.
- Funkcje PostGIS dla odległości w metrach (`geography`).

**Do napisania (Python):**
- generator opisu bazy na poziomach K0–K3,
- skrypt uruchamiający testy i zapisujący odpowiedzi,
- porównywanie wyników z wzorcem,
- odczyt promienia z SQL,
- wykresy.

**Do przygotowania ręcznie:** zapytania wzorcowe do 20 pytań.

### 6. Plan eksperymentów (ok. 50 s)

**Eksperyment 1 (H1):**
- Cztery poziomy kontekstu, każdy dodaje jeden rodzaj informacji: same nazwy tabel → + opis struktury → + opis zawartości danych → + wskazówki i przykłady.
- 20 pytań × 4 poziomy × 3 powtórzenia = 240 wywołań.
- **Potwierdzenie H1:** największy przyrost trafności daje opis zawartości danych.
- **Przykład:** „Jaki szpital jest najbliżej PKiN?”. W bazie jest 7 szpitali zapisanych jako punkty i 37 jako poligony. Zapytanie tylko po punktach działa, ale zwraca zły szpital.

**Eksperyment 2 (H2):**
- Te same pytania z różnym kontekstem, np. „Idę pieszo / Jadę samochodem. Wymień apteki / lotniska w pobliżu Dworca Centralnego.”
- 28 pytań × 10 powtórzeń = 280 wywołań.
- **Potwierdzenie H2:** promień rośnie dla większych obiektów i szybszych środków transportu.

**Grafika:** dwa puste wykresy na wyniki:
- trafność na czterech poziomach,
- promień dla obiektów, osobno dla „pieszo” i „samochodem”.

### 7. Dalsze kroki i harmonogram (ok. 30 s)

| Termin | Zadanie |
|---|---|
| zrobione | przegląd literatury, baza z danymi, pytania testowe, opis poziomów kontekstu |
| do 09.11 | wysłanie prezentacji |
| do 13.11 | zapytania wzorcowe dla części pytań, pierwsza wersja skryptu, **pilotaż** na kilku pytaniach |
| 13.11 | spotkanie z opiekunem: wyniki pilotażu |
| do 27.11 | wszystkie zapytania wzorcowe, pełne eksperymenty 1 i 2 |
| do 11.12 | analiza wyników, wykresy, szkic artykułu |
| dalej | poprawki artykułu po uwagach opiekuna |

Terminy po 13.11 to nasza propozycja do potwierdzenia z opiekunem.

Na tym slajdzie albo w notatkach podajemy podział zadań w zespole.

---

## Ryzyka

Wytyczne nie wymagają osobnego slajdu o ryzykach. Jeśli padnie pytanie, odpowiadamy na podstawie sekcji „Ryzyka” w [informacje-ogolne.md](informacje-ogolne.md). Dwa najważniejsze:
- błędy w zapytaniach wzorcowych, które ogranicza weryfikacja przez drugą osobę,
- mała próba, więc wyniki pokażemy opisowo.

## Do ustalenia

- **Termin:** w notatce ze spotkania 30.10 jest 8 listopada, a w wytycznych 09.11. Bezpieczniej wysłać do 8.11.
- Kto prezentuje które slajdy.
- **Czy na slajdzie 6 pokazujemy prawdziwą odpowiedź Claude.** Wystarczy jedno wywołanie API przed wysłaniem prezentacji, a byłby to mocny punkt.
