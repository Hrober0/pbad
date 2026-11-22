# Eksperyment 1 (H1) — opracowanie wyników

Materiał do artykułu. Szczegóły metody: [pytania.md](pytania.md), dane surowe: [wyniki/](wyniki/).

## Ustawienie

20 pytań przestrzennych o Warszawę (5 kategorii po 4 pytania) × 4 poziomy kontekstu × 3 powtórzenia = 240 zapytań wygenerowanych przez `claude-sonnet-5-5` (`effort: medium`, jedno wywołanie bez historii). Każde zapytanie wykonano na bazie OSM (Geofabrik, mazowieckie, 2026-11-20) i porównano z zapytaniem wzorcowym. Cała seria kosztowała ok. $4,50 i trwała 4 minuty.

## Wynik główny

| Poziom | Co dodaje | Tokeny promptu | Trafność | 95% CI |
|---|---|---|---|---|
| K0 | nazwy tabel i kolumn | 1 500 | 58% | 46–70% |
| K1 | + typy, geometria, SRID | 2 828 | 52% | 39–64% |
| K2 | + opis zawartości danych | 9 524 | 68% | 56–79% |
| K3 | + wskazówki i 5 przykładów | 12 160 | 80% | 68–88% |

Przyrosty: K0→K1 **−6,7 pp**, K1→K2 **+16,7 pp**, K2→K3 **+11,7 pp**. Największy jest przyrost po dodaniu opisu zawartości danych, czyli zgodnie z H1 — ale różnice między przyrostami mieszczą się w przedziałach ufności, a przy ścisłej ocenie (bez wariantów dopuszczalnych, patrz „Ograniczenia") największy byłby przyrost K2→K3. Wynik traktujemy jako opisowy.

Opis struktury (K1) nie pomógł wcale — trafność lekko spadła. Model zna konwencje Geofabrik na tyle dobrze, że same nazwy tabel i kolumn wystarczają mu do poprawnego SQL tam, gdzie nie ma pułapek w danych.

## Ciekawe wyniki

### 1. Opis danych usuwa konkretne błędy, i to całkowicie

Najczystszy efekt H1 widać na pojedynczych błędach, które K2 opisuje wprost:

| Błąd w wygenerowanym SQL (na 60 prób) | K0 | K1 | K2 | K3 |
|---|---|---|---|---|
| granica Warszawy bez `fclass` (ta sama geometria jest w bazie 3 razy → wynik ×3) | 21 | 19 | **0** | **0** |
| filtr `name IS NOT NULL` (brak nazwy to w bazie pusty napis, więc nic nie odfiltrowuje) | 9 | 10 | 2 | **0** |

Przykład: „Ile supermarketów jest w Warszawie?" — na K0 model zwraca 1500 zamiast 500, na K2 i K3 zawsze 500. Najmocniej widać to w złączeniach przestrzennych (kategoria J): **2, 0, 5 i 11 poprawnych na 12** na kolejnych poziomach. W J05 („budynki na terenie Łazienek") na K0–K1 model filtruje `IS NOT NULL` i dokłada budynek o pustej nazwie, od K2 konsekwentnie używa `name <> ''`.

### 2. Kontekst nie pomaga w nazwach własnych — a bywa, że szkodzi

Największą grupą błędów na K2–K3 jest **nieznalezienie obiektu odniesienia**: 0, 0, 8 i 4 przypadki na kolejnych poziomach. Model zgaduje nazwę w OSM i łączy ją z warunkiem na typ obiektu, przez co oba warunki wzajemnie się wykluczają:

- „Stadion Narodowy" szukany jako `fclass='stadium' AND name ILIKE '%Stadion Narodowy%'` — w bazie stadion nazywa się „PGE Narodowy",
- „Zamek Królewski w Warszawie" z `fclass='castle'` — pod tą pełną nazwą jest tylko muzeum,
- „Plac Bociani Zakątek" szukany jako plac zabaw (`playground`), a to park.

Na K0–K1 tych pustych wyników nie ma, bo model pisze luźniejsze warunki. **Więcej wiedzy o danych prowadzi do bardziej rygorystycznych zapytań, a te częściej rozmijają się z rzeczywistą nazwą obiektu.**

Skrajny przypadek to pytanie o przystanki przy pomniku Ordona „w Rembertowie" — 0 na 12 na wszystkich poziomach. Model szuka po fragmencie „Ordon", trafia w Redutę Ordona na Ochocie i sam pisze, że „nie ma kolumny z dzielnicą", choć K2 mówi, że dzielnice są osobną warstwą granic, którą sprawdza się przestrzennie.

### 3. Wskazówka może pogorszyć wynik

Pomiary (kategoria M) jako jedyne spadają na K3: 7, 8, 8 i **5** na 12. Pytanie o długość Wisły w Warszawie ma na K2 3/3, a na K3 **0/3** — wskazówka „dopasowuj nazwy po fragmencie" sprawia, że model pisze `ILIKE '%Wisła%'` i dolicza starorzecze „Stara Wisła" (30,15 km zamiast 29,40). Rada dobra dla jednych pytań psuje inne.

### 4. „Działa, ale jest źle"

Spośród 240 zapytań **każde wykonało się bez błędu składni**. Błędy są wyłącznie semantyczne i nie widać ich po samym wyniku: 1500 supermarketów wygląda wiarygodnie, a lista kawiarni wokół przypadkowego przystanku „Dworzec Centralny 01" wygląda jak poprawna odpowiedź. To argument za oceną wynikiem, a nie wykonywalnością — odsetek zapytań wykonujących się (100% na każdym poziomie) nie różnicuje poziomów kontekstu w ogóle.

### 5. Błędy, których się spodziewaliśmy, a których nie było

- Liczenie w stopniach zamiast w metrach: model rzutuje na `geography` w 83–88% zapytań już na K0, niezależnie od poziomu.
- Współrzędne wpisane z pamięci (np. dla PKiN): ani razu na 240 prób.

### 6. Koszt i stabilność

Kontekst K3 jest 8 razy dłuższy niż K0, a podnosi trafność o 22 pp. Odpowiedzi skracają się wraz z kontekstem (614 → 546 tokenów). Model jest przy tym niestabilny: tylko 4 z 80 kombinacji pytanie × poziom dały identyczny SQL we wszystkich 3 powtórzeniach — powtórzenia faktycznie mierzą rozrzut.

## Ograniczenia

- **Warianty dopuszczalne ustalono po obejrzeniu wyników.** Uznajemy odległość liczoną od obrysu lub od środka obiektu oraz — w dwóch pytaniach o najbliższy obiekt — odpowiedź z obiektem bez nazwy. Wzorce główne używają konwencji, które model dostaje dopiero w K3, więc bez wariantów K0–K2 tracą 26 trafień, a K3 żadnego. Przy ocenie ścisłej trafność wynosi 43/37/55/80% i największy jest przyrost K2→K3.
- **Mała próba:** 60 prób na poziom, 12 na kategorię. Przedziały ufności dla sąsiednich poziomów się nakładają.
- **Zmiany w zestawie pytań po pierwszej serii:** pytanie o parki nad Wisłą zastąpiono innym, bo w danych nie miało odpowiedzi (żaden park nie dotyka linii rzeki); pytanie o pomnik Ordona doprecyzowano dopisaniem dzielnicy.
- **Jedno pytanie nie różnicuje poziomów:** najbliższy szpital od PKiN jest obiektem punktowym, więc pominięcie tabeli poligonowej i tak daje dobrą odpowiedź.
- **Dane OSM:** Marszałkowska to w OSM dwie jednokierunkowe jezdnie, więc „długość ulicy" (5,61 km) jest sumą obu; sama ulica ma ok. 3,3 km.
- **Jeden model, jedno ustawienie `effort`, jeden region.**
