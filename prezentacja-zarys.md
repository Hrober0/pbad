# Zarys prezentacji: etap formalny (termin 8.11)

Kolejność slajdów odpowiada sekcjom w [informacje-ogolne.md](informacje-ogolne.md), bo ten plik powstał według wymagań etapu. Nie znamy limitu czasu, więc zarys zakłada ok. 10–12 slajdów na ok. 10 minut. Jeśli limit jest krótszy, slajdy 4 i 11 można połączyć z sąsiednimi.

---

### 1. Tytuł

- Roboczy tytuł: *„Schemat to za mało? Wpływ kontekstu bazy danych i niejasności pytań na generowanie przestrzennego SQL przez LLM”*.
- Autorzy, opiekun, przedmiot, data.

### 2. Problem i motywacja

- Użytkownik pyta językiem naturalnym („gdzie jest apteka niedaleko dworca?”), a LLM ma to przetłumaczyć na SQL z funkcjami PostGIS.
- LLM słabo liczy relacje przestrzenne samodzielnie (praca 11), więc liczenie zostawiamy bazie, a model tylko tłumaczy pytanie.
- Dwa problemy:
  1. Model nie zna danych.
  2. Pytania ludzi są nieprecyzyjne.
- **Grafika:** prosty schemat przepływu: pytanie → LLM (+ kontekst) → SQL → PostGIS → wynik.

### 3. Stan wiedzy (krótko)

- Text-to-SQL ma długą historię: reguły, potem sieci neuronowe, teraz LLM (praca 12).
- Sposób opisania bazy w prompcie wpływa na wynik, ale więcej nie zawsze znaczy lepiej (DAIL-SQL, Monkuu).
- Poprawna składnia nie oznacza poprawnego wyniku (GeoSQL-Eval).
- Modele trzymają się jednej interpretacji niejasnych pytań (AmbiQT).
- **Luka:** mało badań na nowszych modelach (głównie GPT-4) i mało badań nad niejasnością w pytaniach przestrzennych.

### 4. Cel badania

- Sprawdzić, jakie informacje o bazie warto przekazać modelowi.
- Sprawdzić, na ile można polegać na jego interpretacji niejasnych pytań.
- Treść: sekcja „Cel badania” z [informacje-ogolne.md](informacje-ogolne.md).

### 5. Hipotezy

- **H1:** Opis tego, co zawierają dane, poprawia trafność zapytań bardziej niż sam opis struktury bazy.
- **H2:** Im bardziej niejasne jest pytanie, tym bardziej wynik zależy od założeń, które model przyjmuje samodzielnie i nie ujawnia pytającemu, przez co wynik staje się dla pytającego nieprzewidywalny.
- Uwaga do powiedzenia: nieprzewidywalność może wynikać z losowości, czyli różnych wyników przy powtórzeniach, albo z ukrytej wartości domyślnej. Eksperyment pokaże, który przypadek występuje.

### 6. Dane i środowisko

- OSM z Geofabrik dla Mazowsza, PostgreSQL + PostGIS w Dockerze, Claude przez API.
- **Ciekawostki z danych, które są jednocześnie pułapkami dla modelu:**
  - 7 szpitali w Warszawie zapisano jako punkty, a 37 jako poligony,
  - Dworzec Centralny nazywa się w bazie „Warszawa Centralna”,
  - brak nazwy to `''`, a nie NULL,
  - w województwie jest kilka ulic Marszałkowskich.
- **Grafika:** zrzut tabel w DataGrip albo mapa Warszawy z QGIS.

### 7. Eksperyment 1: poziomy kontekstu

- Tabela K0–K3, ale opisana słowami: same nazwy → struktura z typami → opis zawartości danych → wskazówki i przykłady.
- 20 pytań w 5 kategoriach (zakresowe, najbliżsi sąsiedzi, złączenia, agregacje, pomiary) × 4 poziomy × 3 powtórzenia = 240 wywołań.
- Poprawność oceniamy, porównując wynik z wynikiem zapytania wzorcowego, a nie tekst SQL.

### 8. Przykład: „działa” to nie to samo co „jest poprawne”

- Pytanie N01: „Jaki szpital jest najbliżej Pałacu Kultury i Nauki?”
- **Wariant błędny:** zapytanie przeszukuje tylko punkty. Wykonuje się i zwraca sensownie wyglądający, ale zły szpital.
- **Wariant poprawny:** zapytanie łączy punkty i poligony.
- **Grafika:** dwa krótkie zapytania SQL obok siebie i mapka z dwoma wynikami.
- Opcjonalnie para „znany i mało znany obiekt” (PKiN i Skwer Jolanty Brzeskiej): czy model wpisuje współrzędne z pamięci?

### 9. Eksperyment 2: niejasność pytań

- Tabela S1–S3 na przykładzie aptek przy Dworcu Centralnym: „do 500 m” / „10 minut spacerem” / „w pobliżu”.
- Dwa pozostałe przykłady w jednym zdaniu każdy: „w centrum” (niejasny obszar) i „godzina jazdy autem” (czas zamiast odległości).
- 5 zadań × 3 poziomy × 10 powtórzeń = 150 wywołań, na stałym, pełnym kontekście.
- Mierzymy:
  - powtarzalność (indeks Jaccarda),
  - przyjęte wartości (np. promień),
  - czy model sygnalizuje niejasność.

### 10. Zmienne i oczekiwane wyniki

- **Lewa kolumna, zmienne:** zmieniamy poziom kontekstu i stopień niejasności; mierzymy odsetek poprawnych zapytań, rodzaje błędów, Jaccard i przyjęte wartości; stałe są model, ustawienia i instrukcja.
- **Prawa kolumna, oczekiwane wyniki:**
  - największy skok poprawności po dodaniu opisu danych,
  - przy niejasnych pytaniach powtarzalne, ale ukryte wartości domyślne, np. „w pobliżu” = 500 m.
- Każdy wynik, także obalający hipotezę, da się opisać.

### 11. Ryzyka

Wybieramy 4–5 najważniejszych z sekcji „Ryzyka”:
- błędy w zapytaniach wzorcowych (rozwiązanie: weryfikacja przez drugą osobę),
- mała próba, więc wyniki opisowe z przedziałami ufności,
- jakość danych OSM,
- model może znać schemat Geofabrik,
- pole `uwagi` może wpływać na zachowanie modelu.

### 12. Plan prac i podział zadań

- **Oś czasu:**
  - zrobione: przegląd literatury, dane, pytania testowe,
  - teraz: zapytania wzorcowe i skrypt do uruchamiania testów,
  - 13.11: pilotaż na spotkaniu z opiekunem,
  - dalej: pełne eksperymenty, analiza, szkic artykułu.
- Kto za co odpowiada (do uzupełnienia na spotkaniu).

---

## Do ustalenia na spotkaniu

- Limit czasu i wymagany format prezentacji (czy jest szablon wydziałowy?).
- Podział slajdów między osoby.
- Czy na slajdzie 8 pokazujemy prawdziwy wynik z Claude. Wymaga to choćby jednego wywołania API przed 8.11, co byłoby mocnym punktem prezentacji.
