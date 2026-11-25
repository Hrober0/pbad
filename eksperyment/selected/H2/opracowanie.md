# Eksperyment 2 (PB2): opracowanie wyników

Materiał do artykułu. Pytania: [pytania.md](pytania.md). Sposób oceny: [ocena.md](ocena.md). Pełne tabele (generowane skryptem): [wyniki/tabele.md](wyniki/tabele.md). Dane surowe: [wyniki/](wyniki/). Wszystkie liczby niżej pochodzą z tych plików.

**Pytanie badawcze PB2:** jak model interpretuje niejasne określenia przestrzenne i nazwy potoczne oraz czy kontekst pytania zmienia wartość, którą przyjmuje? (Dawniej hipoteza H2, którą na spotkaniu 20.11 zamieniliśmy na pytanie badawcze. Analiza jest opisowa, bez testów statystycznych.)

## Spis treści

1. [Ustawienie](#1-ustawienie)
2. [Najważniejsze obserwacje](#2-najważniejsze-obserwacje)
3. [Część 2a: „w pobliżu”](#3-część-2a-w-pobliżu)
4. [Część 2b: czas dojazdu](#4-część-2b-czas-dojazdu)
5. [Część 2c: „w centrum”](#5-część-2c-w-centrum)
6. [Część 2d: „duże” i „małe”](#6-część-2d-duże-i-małe)
7. [Część 2e: miejsca podane nazwą potoczną](#7-część-2e-miejsca-podane-nazwą-potoczną)
8. [Część 2f: dodatkowe kontrasty](#8-część-2f-dodatkowe-kontrasty)
9. [Zachowania przekrojowe](#9-zachowania-przekrojowe)
10. [Kontrola jakości](#10-kontrola-jakości)
11. [5 czy 10 powtórzeń](#11-5-czy-10-powtórzeń)
12. [Na co uważać przy porównaniach i opisie](#12-na-co-uważać-przy-porównaniach-i-opisie)
13. [Ograniczenia](#13-ograniczenia)
14. [Wnioski do artykułu](#14-wnioski-do-artykułu)
15. [Jak powtórzyć](#15-jak-powtórzyć)
16. [Szkielet części artykułu o PB2](#16-szkielet-części-artykułu-o-pb2)

---

## 1. Ustawienie

| | |
|---|---|
| Model | `claude-sonnet-5-5`, `effort: medium`, temperatura domyślna |
| Kontekst bazy | K2 (struktura i opis zawartości danych, bez wskazówek i przykładów) we wszystkich próbach |
| Instrukcja | ta sama co w eksperymencie 1; format odpowiedzi `{"sql", "uwagi"}`, opis pola `uwagi` neutralny („Uwagi do zapytania. Może pozostać pustym ciągiem.”) |
| Warianty | 84 w siedmiu częściach: 2a „w pobliżu” (23), 2b czas dojazdu (4), 2c „w centrum” (5), 2d „duże/małe” (6), 2e nazwy potoczne (18), 2f dodatkowe kontrasty (18), 2g próba naprawy wyszukiwania po nazwie (10). Do tego jedno pytanie dodatkowe (2h, „od metra”, 10 prób, 25.11), poza główną serią |
| Co model miał, a czego nie | opis bazy (K2), bez dostępu do danych; jedno podejście; bez możliwości dopytania (instrukcja: jedno zapytanie SELECT albo odmowa) |
| Powtórzenia | **10 na wariant, czyli 840 wywołań.** Próby 1–5 dla części 2a–2e pochodzą z pierwszej serii z 24.11, reszta z kolejnych serii tego samego dnia (ten sam model, ten sam kod). Do tego replikacja kontrolna: 2 próby na każdy z 56 pierwszych wariantów, 112 wywołań poza analizą |
| Baza | OSM Geofabrik, mazowieckie, zrzut z 2026-11-20, PostGIS 3.6. SQL wykonywany rolą tylko do odczytu `pbad_ro` |
| Koszt | 7,87 mln tokenów wejściowych i 0,36 mln wyjściowych. Prompt ma ok. 9 340 tokenów (w 2g ok. 9 600, bo dochodzi wskazówka) |
| Błędy | 0 błędów API, 0 błędów wykonania SQL. 22 puste SQL, czyli odmowy |

Z każdej odpowiedzi skrypt odczytuje przyjętą wartość, czyli promień, próg albo wynik zapytania. Wszystkie odczyty przejrzeliśmy razem z SQL, z którego pochodzą (§10).

---

## 2. Najważniejsze obserwacje

Obserwacje są ułożone według PB2: najpierw jak model interpretuje niejasne określenie (A), potem czy i jak kontekst tę interpretację zmienia (B, C), jak interpretuje nazwy potoczne (D) i czy mówi o swojej interpretacji (E). Na końcu (F) skutki, które zależą już od ustawienia eksperymentu i od danych.

**O ustawieniu trzeba pamiętać przy czytaniu:** model nie widział danych, odpowiadał w jednym kroku, nie mógł dopytać (instrukcja każe zwrócić jedno zapytanie SELECT albo odmówić) i miał w odpowiedzi pole na uwagi. Zachowania, które wynikają wprost z tego ustawienia, np. że nie dopytuje albo nie dopasowuje wartości do danych, nie są obserwacjami o interpretacji.

**Teza w jednym zdaniu:** model rozstrzyga niejasne określenia przestrzenne za użytkownika jedną stałą, okrągłą wartością, którą kontekst pytania przesuwa w zdroworozsądkowym kierunku, ale zgrubnie, kilkoma „szufladkami”; przyjętą wartość model podaje, ale prawie nigdy nie mówi, że pytanie było niejasne.

### A. Jak model interpretuje niejasne określenie

1. **Zawsze jako jedną konkretną wartość.**
   - 470 promieni w `ST_DWithin` (części 2a, 2b, 2c, 2f), 60 progów powierzchni (2d), a „najbliższe” bez liczby to zawsze `LIMIT 10` (10/10).
   - Tylko 11 różnych promieni: 300, 500, 700, 800, 1000, 1250, 1500, 2000, 3000, 3750 i 5000 m. Wszystkie są okrągłe albo wyliczone z okrągłej prędkości (1250 m = 5 km/h × 15 min, 3750 m = 15 km/h × 15 min).
   - Ani razu granica administracyjna przy „w centrum” (0/50, choć K2 opisuje dzielnice) ani próg względny przy „duży” (np. percentyl).

   | Określenie | Przyjęta wartość (10 prób) |
   |---|---|
   | apteki „w pobliżu” Dworca Centralnego | 500 m ×10 |
   | szpitale „w pobliżu” Dworca Centralnego | 2000 m ×10 |
   | „bardzo blisko” / „w zasięgu krótkiego spaceru” | 300 m ×9 / 500 m ×5, 800 m ×5 |
   | „w centrum Warszawy” | koło o promieniu 1500 m (kawiarnie 8/10, apteki 7/10) wokół współrzędnych z pamięci (21.0122, 52.2297; 28 z 30 prób) |
   | „duże parki” | Warszawa 20 ha (8/10), Radom 10 ha (9/10), Płock 5 ha (9/10) |
   | „małe parki” | 1 ha (30 na 30 prób, we wszystkich miastach) |
   | „w 15 minut” pieszo / rowerem | 5 km/h → 1250 m (10/10) / 15 km/h → 3750 m albo 3000 m z poprawką na krętość dróg (6/10) |
   | „najbliższe apteki” | 10 aptek (10/10) |
2. **Interpretacja jest powtarzalna.** Na 56 pytań z przyjętą wartością (2a–2d, 2f) 27 daje tę samą wartość we wszystkich 10 próbach, a 52 tę samą w co najmniej 6 na 10. Pozostałe 4 wahają się między dwiema sąsiednimi wartościami (np. 3c: 2000 m ×5, 1500 m ×5). Rozrzut jest skokowy, między sąsiednimi okrągłymi liczbami, nigdy pomiędzy (§9.3). W osobnym uruchomieniu (replikacja) 108 na 112 prób ma ten sam rodzaj interpretacji.

### B. Czy kontekst zmienia interpretację

3. **Tak: wszystkie trzy czynniki przesuwają wartość w zdroworozsądkowym kierunku, ale z inną siłą, niż zakładaliśmy** (§3.2).
   - **rodzaj obiektu:** wartość rośnie w 9 z 9 par i we wszystkich 9 zakresy z 10 prób są rozłączne (szpital 1,5–5 km, apteka 0,5–2 km; iloraz median 1,9–4),
   - **miejsce:** rośnie w 9 z 9 par (peryferie i inne miasta 1,25–2 razy więcej niż centrum Warszawy),
   - **sytuacja pytającego:** rośnie w 6 z 8 par (przy kiosku i lotnisku bez zmiany; 8c odpada przez odmowę).

   Przy ostrzejszym progu (iloraz ≥ 2) zostaje: rodzaj obiektu 8/9, sytuacja 4/8, miejsce 3/9. Plan zakładał odwrotną kolejność: najsilniejsza miała być sytuacja pytającego, bo jest podana wprost, a miejsce miało działać słabo albo wcale. Różnica między centrum Warszawy a resztą nie wynika ze sformułowania pytania: „stacja Warszawa Centralna” daje to samo co „Dworzec Centralny” (500 m ×9, samochodem 1000 m ×10; §8.1).

### C. Jak kontekst zmienia interpretację: zgrubnie, szufladkami

4. **Model reaguje na pojedyncze cechy pytania, a nie na sytuację jako całość.**
   - **Miejsce ma praktycznie dwa poziomy:** centrum Warszawy 500 m, a „wszystko inne” 1000 m. Radom, Siedlce i wieś Krusze dostały 1000 m w 10 na 10 próbach, Tłuszcz w 6 na 10, peryferyjne Płudy w 8 na 10. Więcej (mediana 1,5 km) dostał tylko Celestynów. W uwagach do pytań o wsie ani razu nie pada słowo „wieś” ani „mała miejscowość” (0/30; §8.1).
   - **„Duży” skaluje się z miastem (20 / 10 / 5 ha), „mały” nie (1 ha wszędzie).** Progi się nie stykają: park 2–5 ha nie jest w żadnym mieście ani duży, ani mały (§6).
   - **Siła określenia jest uporządkowana, ale w wąskim zakresie:** „bardzo blisko” 300 m < „w pobliżu” = „w okolicy” 500 m < „krótki spacer” 500–800 m. „W okolicy” nie jest szersze niż „w pobliżu” (§8.2).
   - **Prawie każde zdanie o sytuacji zwiększa promień.** Apteki przy Dworcu Centralnym: bez kontekstu 500 m, a pieszo, samochodem, rowerem, z wózkiem, z dzieckiem czy „pilnie” mediany 800–1500 m. Wyjątkiem jest pośpiech („Mam 10 minut do odjazdu pociągu”): 500 m (§8.3).
   - **Zdarzają się nieintuicyjne kolejności:** rower 1500 m (10/10) więcej niż samochód 1000 m (9/10); wózek i dziecko (mediana 1000 m) więcej niż pieszo (800 m); po angielsku informacja o samochodzie podnosi promień do 1000 m tylko w 4 na 10 prób, a po polsku w 9 na 10 (§8.3, §8.4).
   - **Uwagi pokazują, skąd asymetria roweru i samochodu.** Przy rowerze model w 10 na 10 prób wiąże promień z rowerem („ok. 5 min jazdy rowerem”). Przy samochodzie tylko raz na 10, a dwa razy pisze wprost, że informacja o samochodzie nie zmienia zapytania, bo w bazie nie ma sieci dróg. Z tego samego powodu odmawia przy „w 15 minut samochodem” (10/10; §4).

### D. Jak model interpretuje nazwy potoczne

5. **Za obiekt przyjmuje najbardziej znane znaczenie nazwy, a dodatkowe wybory robi po cichu.**
   - „Łazienki” to park Łazienki Królewskie w 40 na 40 prób, nigdy przysiółek Łazienki (99 km). „Najbliższa stacja metra” to Centrum albo Politechnika (20/20), rozpoznane jako stacje przy torach metra.
   - „Od metra do Gmachu Głównego PW” (pytanie dodatkowe, 2h): „metro” to zawsze stacja Politechnika (10/10), nigdy przystanek „Metro Politechnika” (§7.7).
   - Przy pomnikach model szuka właściwego obiektu, ale słabo trafia w jego zapis w bazie: dobry obiekt w 19 na 60 prób, przy obiektach kontrolnych w 5 na 30. Powodem jest zbyt ścisłe zgadywanie tabeli, `fclass` i formy nazwy (np. „Małego Powstańca” zamiast „Mały Powstaniec”), czyli dopasowanie do danych, a nie interpretacja nazwy (§7.3).
   - **Ukryte wybory:** ta sama odległość Łazienki–PKiN raz od obrysu parku (2042 m), raz od jego środka (2778 m), różnica 36%. Dopisek „nad Wisłą” przy pomniku Syrenki nie zmienia zapytania (10/10 ta sama rzeźba; §7.1).

### E. Czy model mówi o swojej interpretacji

6. **Przyjętą wartość podaje prawie zawsze, ale niejasności pytania prawie nie zgłasza.**
   - Wartość albo założenie podał w uwagach w 556 na 560 prób (2a–2d, 2f), a gdy podał liczbę, zgadzała się z SQL w 549 na 549 przypadków (§9.2). Dotyczy to formatu z polem na uwagi (§12.9).
   - Słowa „niejednoznaczne”, „nieprecyzyjne” i podobne pojawiają się tylko w 11 na 560 prób: 8 razy przy „w centrum” bez nazwy miasta i 3 razy w odmowach przy czasie dojazdu bez środka transportu. Przy „w pobliżu” 0 na 230, przy „duże” i „małe” 0 na 60, w części 2f 0 na 180. Przy „od metra” (2h) 3 na 10 (§9.6).
   - **Model nazywa pytanie niejasnym prawie wyłącznie wtedy, gdy czegoś w nim brakuje** (miasta, stacji, środka transportu; 9 z 11 zgłoszeń w 2a–2d i 2f, a 2 pozostałe dotyczą tego, jak dworzec jest zapisany w danych). Samego niejasnego słowa nie traktuje jako problemu: zamienia je na wartość i nie odmawia (0 odmów przy „w pobliżu”, „w centrum” i „duże”; odmawia tylko przy braku danych, §9.4).

### F. Skutki interpretacji (zależą od ustawienia i od danych)

7. **Stała wartość tam, gdzie obiektów jest mało, daje pusty wynik.** Model nie widział danych, więc nie mógł dopasować wartości do okolicy.

   | Pytanie | Przyjęta wartość | Stan w danych | Pusty wynik |
   |---|---|---|---|
   | wieś Krusze, apteki | 1000 m (tyle samo co Radom i Siedlce) | najbliższa apteka 5,4 km | 10/10 |
   | wieś Krusze, apteki, samochodem | 2000 m | jw. | 10/10 |
   | szpitale przy stacji Warszawa Płudy | 3000 m | najbliższy szpital 3,12 km | 10/10 |
   | „duże parki” w Radomiu | próg 10 ha | największy park 8,2 ha | 9/10 |
8. **Jeden akapit w kontekście przestawia sposób rozstrzygania nazw (część 2g).** Dla 8 problematycznych pytań wskazówka „szukaj po rdzeniu nazwy, w obu tabelach, bez `fclass`” zmienia dobre obiekty z 14 na 38 (na 80), puste wyniki z 42 na 1, ale duże pomyłki z 5 na 20 (szkoła imienia Małego Powstańca, kebab „Palmyra” w Płocku, pomnik Chopina w Radomiu; §7.6). Interpretację nazw da się więc łatwo przesunąć, ale w obie strony.

---

## 3. Część 2a: „w pobliżu”

### 3.1. Przyjęte promienie (rozkład z 10 prób, w metrach)

| Szukane / punkt odniesienia | bez kontekstu (a) | pieszo (b) | samochodem (c) |
|---|---|---|---|
| 1. apteki / Dworzec Centralny (centrum) | 500 ×10 | 800 ×7, 1000 ×3 | 1000 ×9, 1500 ×1 |
| 2. szpitale / Dworzec Centralny | 2000 ×10 | 1500 ×6, 2000 ×4 | 3000 ×10 |
| 3. apteki / Warszawa Płudy (peryferie) | 1000 ×8, 1500 ×2 | 1000 ×10 | 2000 ×5, 1500 ×5 |
| 4. szpitale / Warszawa Płudy | 3000 ×10 | 2000 ×6, 1500 ×4 | 5000 ×10 |
| 5. apteki / Tłuszcz (małe miasto) | 1000 ×6, 1500 ×4 | 1000 ×6, 1500 ×4 | 2000 ×5, 3000 ×4, 1500 ×1 |
| 6. przystanki / kiosk Ciasteczkowo (mały obiekt) | 300 ×10 | 500 ×10 | 500 ×10 |
| 7. przystanki / Lotnisko Chopina (duży obiekt) | 1000 ×10 | 1000 ×7, 800 ×3 | 1000 ×7, 1500 ×3 |

Do tego „niedaleko” zamiast „w pobliżu” (1d): 500 ×6, 1000 ×4. Pośpiech (1e): 500 ×10.

Wszystkie 230 prób to promień w `ST_DWithin` na `geography` (metry), ani razu w stopniach. Ani razu też „k najbliższych”.

### 3.2. Czynniki

Pary wariantów, które różnią się tylko jednym czynnikiem. „Rośnie” oznacza, że mediana wzrosła co najmniej 1,25 raza.

| Czynnik | Par | Rośnie | w tym zakresy rozłączne | Bez zmiany | Maleje | Odpadło |
|---|---|---|---|---|---|---|
| S: sytuacja pytającego | 9 | 6 | 4 | 2 (kiosk: 500 i 500 m; lotnisko: mediany 1000 i 1000 m) | 0 | 1 (8c, odmowa) |
| M: miejsce | 9 | 9 | 4 | 0 | 0 | 0 |
| O: rodzaj i skala obiektu | 9 | 9 | 9 | 0 | 0 | 0 |

Przy ostrzejszym progu: S rośnie w 5/8 par przy ilorazie ≥ 1,5 i w 4/8 przy ≥ 2. M w 6/9 i 3/9. O w 9/9 i 8/9. **Rodzaj obiektu jest najmocniejszy i najbardziej jednoznaczny:** każda para ma rozłączne zakresy, a iloraz wynosi od 1,9 do 4.

### 3.3. Co widać w szczegółach

- **Sytuacja działa słabo tam, gdzie obiektów jest dużo.** Przy aptekach w centrum samochód podnosi promień tylko z 800 do 1000 m. Przy kiosku i lotnisku nie zmienia go wcale (kiosk 500 → 500, lotnisko mediana 1000 → 1000). Poza centrum ta sama zmiana podwaja albo potraja promień: Płudy szpitale 2000 → 5000, Tłuszcz 1000 → 2000.
- **Wartość „bez kontekstu” nie jest wartością pieszego.** W 7 parach „brak informacji” → „pieszo” promień:
  - rośnie 2 razy: apteki w centrum 500 → 800, kiosk 300 → 500,
  - nie zmienia się 3 razy,
  - maleje 2 razy: szpitale w centrum 2000 → 1500, szpitale przy Płudach 3000 → 2000.

  „Brak informacji” → „samochodem” rośnie w 6 z 7 par. Wartość domyślna leży więc między pieszym a samochodem. Przy aptekach w centrum jest mniejsza niż dla pieszego, a przy szpitalach większa.
- **„W pobliżu” i „niedaleko”** dają tę samą medianę (500 m), ale „niedaleko” ma większy rozrzut (4 z 10 prób po 1000 m).

### 3.4. Skutek: ile wyników dostaje użytkownik

| Miejsce | Aptek w 500 m | w 1 km | w 2 km | Przyjęty promień (bez kontekstu) | Wyników (mediana) |
|---|---|---|---|---|---|
| Warszawa Centralna | 7 | 27 | 63 | 500 m | 6 |
| Warszawa Płudy | 0 | 1 | 4 | 1000 m | 1 |

Szpitale przy Płudach: **0 wyników we wszystkich 30 próbach 4a–4c.** Przyczyny są dwie, rozdzielone automatycznym testem z promieniem 10⁸ m (§10):
- **4a i 4b:** promień 1,5–3 km, a najbliższy szpital leży 3,12 km dalej. Punkt odniesienia był znaleziony, zawiódł promień.
- **4c:** model szukał stacji z `fclass = 'railway_station'`, a Warszawa Płudy jest w danych przystankiem `railway_halt`. Punkt odniesienia nie znaleziony w 10 na 10 próbach, więc promień 5 km nie miał znaczenia.

---

## 4. Część 2b: czas dojazdu

| # | Wariant | Wynik 10 prób | Przyjęta prędkość |
|---|---|---|---|
| 8a | brak informacji | **odmowa 10/10**; w replikacji 2/2 promień (1000 i 1250 m, „przyjąłem dojście pieszo”) | – |
| 8b | pieszo | 1250 m ×10 | 5 km/h |
| 8d | rowerem | 3000 m ×6, 3750 m ×4 | 15 km/h ×10 (w uwagach); przy 3000 m z „poprawką na krętość tras” |
| 8c | samochodem | **odmowa 10/10**, także w replikacji 2/2 | – |

- **Prędkości są podręcznikowe:** pieszo 5 km/h (10/10), rowerem 15 km/h (10/10, prędkość podana w uwagach).
- **Krętość dróg model uwzględnia tylko dla roweru.** W 6 na 10 prób dla roweru zmniejszył 3750 m do 3000 m „z poprawką na krętość tras” (współczynnik ok. 1,25–1,3). Dla pieszego w serii głównej nie zrobił tego ani razu: 1250 m to dokładnie 5 km/h × 15 min w linii prostej. Jedyna poprawka dla pieszego pojawiła się w replikacji 8a (1250 → 1000 m). Sama prędkość jest więc stała, a zmienia się decyzja, czy przeliczyć linię prostą na drogę. Prędkość wyliczona naiwnie z promienia (3000 m / 15 min = 12 km/h) byłaby tu błędnym odczytem.
- **Asymetria:** dla pieszego i rowerzysty linia prosta jest dla modelu „przybliżeniem”, dla samochodu już nie. Cytat z uwag: „Czas dojazdu samochodem wymaga routingu po sieci drogowej (z prędkościami, ograniczeniami, korkami…), a baza nie ma topologii drogowej (pgRouting) ani wiarygodnych danych o prędkościach (maxspeed często = 0).” Model trafnie rozpoznaje, że przy samochodzie błąd linii prostej jest największy.
- **Odmowa przy 8a zależy od uruchomienia.** W serii głównej było 10 odmów na 10, a w osobnym uruchomieniu 2 razy przyjęte chodzenie pieszo. Pytanie leży na granicy decyzji modelu.

---

## 5. Część 2c: „w centrum”

| # | Pytanie | Promień (10 prób) | Środek „centrum” | Tabela poligonów uwzględniona |
|---|---|---|---|---|
| 9a | kawiarnie w centrum Warszawy | 1500 ×8, 2000 ×2 | współrzędne z pamięci (21.0122, 52.2297) ×8, punkt miejscowości z bazy ×2 | 0/10 |
| 9b | kawiarnie w centrum Płocka | 1000 ×10 | punkt miejscowości Płock z `gis_osm_places_free` ×10 | 0/10 |
| 9c | kawiarnie w centrum (bez miasta) | 1000 ×6, 1500 ×4 | zawsze Warszawa, współrzędne z pamięci ×10 | 0/10 |
| 10a | apteki w centrum Warszawy | 1500 ×7, 2000 ×3 | współrzędne z pamięci ×10 | 0/10 |
| 10b | apteki w centrum Płocka | 1500 ×8, 1000 ×2 | punkt miejscowości Płock ×10 | 9/10 |

- **Ani razu granica administracyjna (0/50),** choć K2 mówi, że dzielnice Warszawy to `admin_level9`. Śródmieście ma 15,6 km², a koło o promieniu 1,5 km to 7,1 km², mniej niż połowa.
- **Środek „centrum Warszawy” to zawsze ten sam punkt z pamięci,** ok. 470 m od punktu PKiN w bazie. Model opisuje go jako „okolice Pałacu Kultury i Nauki”.
- **Bez nazwy miasta model zakłada Warszawę w 10 na 10 próbach** i za każdym razem pisze o tym w uwagach („Pytanie nie określa miasta, więc przyjęto centrum Warszawy”).
- **Centrum lekko skaluje się z miastem:** kawiarnie w Warszawie 1500 m, a w Płocku 1000 m. Przy aptekach obie mediany wynoszą jednak 1500 m.
- **Obiekty zapisane jako poligony są pomijane świadomie.** W pytaniach o Warszawę model ani razu nie dołączył tabeli `pois_a`, a w uwagach pisze, że „kawiarnie narysowane jako poligony nie są uwzględnione”.

---

## 6. Część 2d: „duże” i „małe”

| Miasto (powierzchnia) | Próg „duży” (10 prób) | Wyników | Próg „mały” | Wyników |
|---|---|---|---|---|
| Warszawa (517 km²) | 20 ha ×8, 10 ha ×1, 30 ha ×1 | 14 | 1 ha ×10 | 239 |
| Radom (115 km²) | 10 ha ×9, 5 ha ×1 | **0 w 9 z 10 prób** | 1 ha ×10 | 51 |
| Płock (88 km²) | 5 ha ×9, 10 ha ×1 | 1 (w jednej próbie 0) | 1 ha ×10 | 19 |

- **„Duży” skaluje się z miastem, „mały” nie:** 1 ha w 30 na 30 próbach.
- **Progi się nie stykają.** Parki od 1 do 5–20 ha nie są ani „duże”, ani „małe”. Każdy próg jest dobierany osobno, bez spójnej skali.
- **Duża pomyłka praktyczna: Radom.** Największy park w danych to Park Stary Ogród, 8,2 ha, więc próg 10 ha daje pusty wynik w 9 z 10 prób. W Płocku próg 5 ha zostawia jeden park (Park Północny, 5,4 ha). Ani razu nie było progu względnego (percentyl, średnia) ani „kilku największych” (`ORDER BY ... LIMIT`). Model ustala próg z góry, bez spojrzenia na dane.

---

## 7. Część 2e: miejsca podane nazwą potoczną

Pomysły ze spotkania 20.11, uzupełnione o pomnik Kopernika i trzy obiekty kontrolne. Wartości wzorcowe dla każdego kandydata: [pytania.md](pytania.md#kandydaci-w-bazie-i-odległości-wzorcowe).

### 7.1. Wynik dla każdego obiektu (10 prób)

| # | Obiekt | Dobry obiekt | Co się stało |
|---|---|---|---|
| 13a | „Łazienki” → PKiN | **10/10** | od środka parku 2778 m (8 razy) albo od obrysu 2042 m (2 razy). Ani razu przysiółek Łazienki (99 km) |
| 13b | „Łazienki Królewskie” → PKiN | **10/10** | od obrysu 2042 m (6 razy), od środka 2778 m (3 razy), od środka do obrysu PKiN 2619 m (raz). Ta sama odpowiedź raz od obrysu, raz od środka, czyli różnica 36% |
| 14a, 14b | Łazienki → Pole Mokotowskie | **20/20** | zawsze 754 m, czyli między obrysami. Między środkami byłoby 2195 m |
| 15a | „pomnik Chopina” → PKiN | **0/10** | 6 razy pusty wynik (`fclass = 'monument'`, a pomnik jest `memorial`); 2 razy pusty, bo nie znaleziono PKiN; **raz Radom (93 072 m)**; **raz powiat sochaczewski (51 582 m)** |
| 15b | „pomnik Chopina w Łazienkach” | **0/10** | 10 razy pusty wynik: `monument` w tabeli punktów, a prawdziwy pomnik jest poligonem `memorial` „Fryderyk Chopin” |
| 16a | „Syrenka Warszawska” → PKiN | **0/10** | 7 razy betonowa rzeźba „Syrenka” (0,7–0,8 km od PKiN); **raz apteka „Syrenka”** (pierwszy punkt `%Syrenk%` bez warunku na `fclass`); **raz środek ciężkości wszystkich „Syrenek” w województwie (31 755 m)**; raz pusty (PKiN) |
| 16b | „pomnik Syrenki nad Wisłą” | **0/10** | 10 razy ta sama rzeźba: dopisek „nad Wisłą” nie zmienia zapytania |
| 17a | „pomnik Kopernika” → PKiN | **9/10** | pomnik na Krakowskim Przedmieściu (1067 albo 949 m); raz pusty (`monument`). Pułapka, czyli rzeźba Kopernika przy wejściu do PKiN (52 m), nie zadziałała, bo jest `artwork` |
| 17b | „… na Krakowskim Przedmieściu” | **10/10** | 1067, 1090 albo 949 m (różne geometrie PKiN) |
| 18 | Kolumna Zygmunta (kontrola) | **0/10** | 10 razy szukana w tabeli **punktów**, a jest wyłącznie poligonem |
| 19 | palma na rondzie de Gaulle'a (kontrola) | **4/10** | 3 razy pusty (PKiN); 2 odmowy („palma nie jest osobnym typem obiektu”); **raz środek wszystkich punktów `%palma%` (3889 m)** |
| 20 | Mały Powstaniec (kontrola) | **1/10** | 9 razy szukany jako „Małego Powstańca” (dopełniacz z pytania); raz w mianowniku i wtedy trafiony |
| 21a | najbliższa stacja metra od PKiN | **10/10** | Centrum, 147 m (od obrysu PKiN) albo 311 m. Nie pomylona z koleją (Warszawa Śródmieście, 284 m) |
| 21b | najbliższa stacja metra od Łazienek | **10/10** | Politechnika, 797 m |
| 22a | kawiarnie ≤ 200 m od metra | **10/10** | 72, czyli tylko metro. Wszystkie stacje kolejowe w Warszawie dałyby 111 |
| 22b | „kawiarnie w pobliżu stacji metra” (bez nazwy) | – | 10/10 wszystkie stacje metra, promień 300 m, 142–143 kawiarnie |
| 22c | „… stacji metra Centrum” | – | promień 500 m ×8, 300 m ×2 |

### 7.2. Zestawienie

| Grupa | Prób | Dobry obiekt | Pomyłka | Duża pomyłka | Pusty: obiekt | Pusty: PKiN | Odmowa |
|---|---|---|---|---|---|---|---|
| metro i parki (13, 14, 21, 22a) | 70 | **70** | 0 | 0 | 0 | 0 | 0 |
| pomniki (15, 16, 17) | 60 | 19 | 17 | 4 | 17 | 3 | 0 |
| obiekty kontrolne (18, 19, 20) | 30 | 5 | 0 | 1 | 19 | 3 | 2 |
| **razem** | 160 | 94 | 17 | 5 | 36 | 6 | 2 |

### 7.3. Dlaczego „łatwe” obiekty wypadły najgorzej

Model nie zna zawartości bazy, więc przy każdym obiekcie zgaduje trzy rzeczy naraz i łączy je spójnikiem `AND`:

| Obiekt | Tabela | `fclass` | Nazwa | Wynik |
|---|---|---|---|---|
| Kolumna Zygmunta | ✗ (szuka punktu, jest poligon) | ✓ | ✓ | pusty 10/10 |
| pomnik Chopina | ✗ / ✓ | ✗ (`monument`, jest `memorial`) | ✓ | pusty 16/20 |
| Mały Powstaniec | ✓ | ✓ / ✗ | ✗ (dopełniacz) | pusty 9/10 |
| pomnik Kopernika | ✓ | ✓ (`memorial` dopuszczony) | ✓ | trafiony 19/20 |

K2 mówi wprost, że znany obiekt bywa zapisany w kilku tabelach z różnym `fclass`, a nazwy w bazie mogą się różnić od potocznych. Model to powtarza w uwagach („jeśli Kolumna Zygmunta nie występuje jako punkt…, może być konieczne sprawdzenie tabeli pois_a”), ale nie przekłada tego na zapytanie: nie łączy obu tabel i nie rezygnuje z warunku na `fclass`. **Ostrzega zamiast pisać odporne zapytanie.** To ten sam mechanizm co w eksperymencie 1: więcej wiedzy o danych daje bardziej rygorystyczne zapytania.

### 7.4. Rodzaje dużych pomyłek

Duże pomyłki zdarzają się rzadko, w 5 na 160 prób, ale są całkowicie niewidoczne w wyniku. Zapytanie zwraca jedną wiarygodnie wyglądającą liczbę:

| Próba | Wynik | Co model wybrał | Mechanizm |
|---|---|---|---|
| 15a #9 | 93 072 m | „Pomnik Fryderyka Chopina” w **Radomiu** | `name ILIKE '%Chopin%' AND name ILIKE '%pomnik%'`: jedyny obiekt z „pomnik” w nazwie jest w Radomiu |
| 15a #10 | 51 582 m | „Pomnik Fryderka Chopina” (literówka w OSM) pod Sochaczewem | ten sam warunek, z `UNION` obu tabel |
| 16a #7 | 1935 m | **apteka „Syrenka”** | `name ILIKE '%Syrenk%' ORDER BY fid LIMIT 1` bez warunku na `fclass` |
| 16a #10 | 31 755 m | punkt w polu, **środek ciężkości wszystkich „Syrenek”** w województwie | `ST_Centroid(ST_Collect(geom))` po wszystkich pasujących obiektach |
| 19 #10 | 3889 m | środek ciężkości wszystkich punktów `%palma%` | jw. |

Pomyłka w 16a #7 pokazuje też pułapkę oceny: 1935 m wypada blisko odległości prawdziwej Syreny nad Wisłą (1900 m). Dopiero sprawdzenie, który obiekt wybiera SQL, pokazało, że to apteka (§10).

### 7.5. Współrzędne z pamięci

W 48 zapytaniach model wpisał współrzędne z pamięci (`ST_MakePoint(21.0…, 52.2…)`):
- 28 razy jako środek „centrum Warszawy” (2c),
- 20 razy przy pomnikach (15, 16, 17), żeby wybrać jeden z kilku obiektów o tej samej nazwie (`ORDER BY ST_Distance(geom, punkt_z_pamięci) LIMIT 1`).

W eksperymencie 1 nie zdarzyło się to ani razu na 240 prób. Model sięga po pamięć dopiero wtedy, gdy wie, że nazwa jest niejednoznaczna. Pomaga to połowicznie: w 17b dało dobry pomnik (9 razy), a w 15b nic, bo warunek `fclass` i tak wykluczył właściwy obiekt.

### 7.6. Próba naprawy: wskazówka o wyszukiwaniu po nazwie (część 2g)

Sprawdziliśmy, czy błędy z 2e da się usunąć jednym ogólnym akapitem w kontekście. Akapit nie wymienia żadnego obiektu z pytań: szukaj w tabelach punktowych i poligonowych bez warunku na `fclass`, używaj rdzenia nazwy, bo w bazie jest mianownik, i wybierz jeden obiekt. Pełna treść: [pytania.md](pytania.md#część-2g-próba-naprawy-wyszukiwania-po-nazwie--10-wariantów). Pytania są identyczne jak w 2e, po 10 prób.

| Obiekt | 2e: bez wskazówki | 2g: ze wskazówką | Co wybiera model ze wskazówką |
|---|---|---|---|
| pomnik Chopina | 0 dobrych, 8 pustych, 2 duże pomyłki | 1 dobry, 8 pomyłek, 1 duża | „Fortepian Chopina” (8 razy), pomnik w Łazienkach (1), Radom (1) |
| pomnik Chopina w Łazienkach | 0 dobrych, 10 pustych | **5 dobrych**, 1 pomyłka, **4 duże** | pomnik w Łazienkach (5), **pod Sochaczewem (3) i w Radomiu (1)**, „Fortepian Chopina” (1) |
| Syrenka Warszawska | 0 dobrych, 7 pomyłek, 2 duże, 1 pusty | **5 dobrych**, 3 pomyłki, 2 duże | Syrenka z Rynku (4), Syrena znad Wisły (1), betonowa rzeźba (3), „Stadion Syrenki” i apteka „Syrenka” (2) |
| Syrenka nad Wisłą | 0 dobrych, 10 pomyłek | 0 dobrych, 9 pomyłek, 1 duża | **Syrenka z Rynku** (7), rzeźba (2), „Syrenka Białobrzeska” (1). Dopisek „nad Wisłą” nadal nie działa |
| pomnik Kopernika | 9 dobrych, 1 pusty | **10 dobrych** | pomnik na Krakowskim Przedmieściu |
| Kolumna Zygmunta | 0 dobrych, 10 pustych | **10 dobrych** | Kolumna (poligon) |
| palma | 4 dobre, 3 puste, 2 odmowy, 1 duża | 5 dobrych, **5 dużych** | palma (5), salon i kawiarnia „Las Palmas” (3), „Pizza pod Palmą” (1), **„Palmyra Kebab” w Płocku** (1) |
| Mały Powstaniec | 1 dobry, 9 pustych | 2 dobre, **7 dużych**, 1 pusty | **„Szkoła Podstawowa nr 32 im. Małego Powstańca”** (7) |
| Łazienki (kontrola) | 10 dobrych | 10 dobrych | – |
| najbliższa stacja metra (kontrola) | 10 dobrych | 10 dobrych | – |

**Razem dla 8 problematycznych pytań (80 prób):**

| | Dobry obiekt | Pusty wynik | Pomyłka | Duża pomyłka | Odmowa |
|---|---|---|---|---|---|
| bez wskazówki (2e) | 14 | 42 | 17 | 5 | 2 |
| ze wskazówką (2g) | **38** | **1** | 21 | **20** | 0 |

- **Wskazówka działa tam, gdzie problemem było zgadywanie tabeli i `fclass`.** Kolumna Zygmunta, pomnik Chopina w Łazienkach i Syrenka Warszawska przechodzą z pustego wyniku albo złego obiektu na dobry obiekt.
- **Rdzeń nazwy bez warunku na rodzaj obiektu łapie wszystko, co ma tę nazwę.** Szkoła imienia Małego Powstańca, kebab „Palmyra”, salon „Las Palmas”, „Fortepian Chopina”. Model, który ma wybrać „jeden obiekt, który najlepiej pasuje”, często bierze nie ten. Przy pomniku Chopina „w Łazienkach” w 4 na 10 prób trafia w pomnik w Radomiu albo pod Sochaczewem, mimo że pytanie podaje miejsce.
- **Ciche błędy zamieniają się w głośne, ale niewidoczne.** Pusty wynik użytkownik od razu zauważy. Odległość 2226 m do szkoły zamiast 1969 m do pomnika wygląda wiarygodnie.
- **Opisu położenia z pytania wskazówka nie naprawia:** „pomnik Syrenki nad Wisłą” nadal trafia w Syrenkę z Rynku albo w rzeźbę. Słowo „nad Wisłą” nie przechodzi na warunek przestrzenny.
- **Wniosek do artykułu:** sama zmiana strategii wyszukiwania nie wystarcza. Potrzebne jest jeszcze rozstrzyganie, który obiekt wybrać, np. preferencja dla rodzajów `memorial`/`monument`/`attraction`, kontrola miasta albo pokazanie użytkownikowi nazwy i położenia wybranego obiektu.

### 7.7. Co model uznaje za „metro” (część 2h, pytanie dodatkowe)

Pytanie dodane po dyskusji wyników, poza główną serią 840 wywołań (10 prób, K2 bez wskazówki): *„Jak daleko w linii prostej w metrach jest od metra do Gmachu Głównego Politechniki Warszawskiej?”*. Słowo „metro” nie wskazuje stacji, a w bazie są obok siebie stacja metra „Politechnika” (`railway_station`) i 14 przystanków autobusowych i tramwajowych „Metro Politechnika 01–14” (słowo „metro” w nazwie). Ocena z SQL i uwag, bo odległości stacji i przystanków do Gmachu są podobne (280–437 m).

| Co sprawdzamy | Wynik (10 prób) |
|---|---|
| „metro” = stacja metra Politechnika (`railway_station`, nazwa dokładnie „Politechnika”) | **10/10** |
| dodatkowo sprawdził, że stacja leży przy torach metra (`subway`, do 150 m) | 6/10 |
| wziął przystanek „Metro Politechnika …” | 0/10 |
| policzył najbliższą stację metra w SQL zamiast wpisać nazwę | 0/10 |
| w uwagach napisał, że pytanie jest niejednoznaczne | 3/10 |
| wynik zapytania | **pusty 10/10** |

- **„Metro” model rozumie jako najbliższą stację metra i wybiera ją z własnej wiedzy.** Za każdym razem wpisuje nazwę „Politechnika” na sztywno (jedna próba: „zakładam, że chodzi o najbliższą stację metra (Politechnika)”). Przystanki z „Metro” w nazwie nigdy nie zmyliły modelu, bo szuka po `fclass = 'railway_station'`, a nie po słowie „metro”.
- **Wynik jest jednak pusty w 10 na 10 prób, i to przez Gmach Główny, nie przez metro.** Część zapytania ze stacją zwraca stację (sprawdzone). Budynek nazywa się w bazie „Gmach Główny PW”, a model szuka nazwy z „Politechnik” (np. „%Gmach Główny%Politechniki%” albo pełnej nazwy; 8 prób) albo samego „%Gmach Główny%”, ale tylko w tabeli `pois_a`, gdzie takiego obiektu nie ma (2 próby). To ten sam mechanizm co przy pomnikach w §7.3: zbyt ścisłe zgadywanie nazwy i tabeli. We wszystkich 10 próbach model sam ostrzega w uwagach, że nazwa albo tabela budynku może być inna i wynik może wyjść pusty.
- **Do artykułu:** niejasne „metro” model rozstrzyga sensownie i jednakowo, bez pomyłek typu przystanek, ale po cichu (tylko 3 razy na 10 nazywa to niejasnością). Pusty wynik pokazuje, że przy nazwach potocznych słabym ogniwem jest nazwa obiektu docelowego, a nie interpretacja niejasnego słowa.

---

## 8. Część 2f: dodatkowe kontrasty

Część dodana w drugiej serii. Wszystkie pytania mają postać „Wymień apteki … Dworca Centralnego / stacji X”, więc da się je zestawić z 1a (500 m).

### 8.1. Gradient wielkości miejscowości

| Stacja (miejscowość) | Promień (10 prób) | Aptek w 1 km | w 2 km | najbliższa | Wyników (mediana) | Pusty wynik |
|---|---|---|---|---|---|---|
| Warszawa Centralna | 500 ×10 | 27 | 63 | 45 m | 6 | 0/10 |
| Radom Główny (ok. 200 tys.) | 1000 ×10 | 15 | 39 | 187 m | 15 | 0/10 |
| Siedlce (ok. 76 tys.) | 1000 ×10 | 12 | 25 | 316 m | 5 | 0/10 |
| Tłuszcz (ok. 8 tys.) | 1000 ×6, 1500 ×4 | 5 | 5 | 194 m | 2 | 0/10 |
| Celestynów (wieś) | 2000 ×4, 1500 ×4, 1000 ×2 | 3 | 3 | 158 m | 3 | 0/10 |
| Krusze (wieś) | **1000 ×10** | 0 | 0 | **5407 m** | 0 | **10/10** |
| Krusze, „Jadę samochodem.” | 2000 ×8, 1500 ×1, 3000 ×1 | | | | 0 | **10/10** |

- **Model ma właściwie dwa poziomy: „centrum Warszawy” (500 m) i „wszystko inne” (1000 m).** Ściśle 1000 m w 10 na 10 próbach dostały Radom, Siedlce i wieś Krusze. Tłuszcz dostał 1000 m w 6 z 10 prób, a peryferyjna stacja Warszawa Płudy (3a) w 8 z 10.
- **Większy promień (mediana 1,5 km, do 2 km) dostał tylko Celestynów.** Krusze, wieś bez apteki w promieniu 5 km, dostały tyle samo co 200-tysięczny Radom. Dlaczego Celestynów tak, a Krusze nie, z danych nie wiemy. Możliwe, że model po prostu zna Celestynów, ale to nasza interpretacja. W uwagach w 30 próbach (23c, 23d, 24) ani razu nie pada słowo „wieś” ani „mała miejscowość”.
- **Na wsi bez apteki w okolicy odpowiedź jest pusta za każdym razem,** także samochodem. Punkt odniesienia był znaleziony w 20 na 20 próbach (test 10⁸ m), więc zawiódł wyłącznie promień.
- **Kontrola sformułowania (29a, 29b).** Warszawę reprezentował „Dworzec Centralny”, a inne miejscowości „stacja X”, więc różnica mogła wynikać ze sformułowania. Sprawdziliśmy to pytaniem o „stację Warszawa Centralna”: 500 m ×9 i 1000 m ×1, a samochodem 1000 m ×10, czyli tak samo jak „Dworzec Centralny” (1a i 1c). **Sformułowanie nie tłumaczy różnicy:** centrum Warszawy dostaje 500 m, a inne miejscowości 1000 m.

### 8.2. Siła określenia

| Określenie | Promień (10 prób) | Mediana |
|---|---|---|
| „bardzo blisko” | 300 ×9, 500 ×1 | 300 |
| „rzut beretem od” | 500 ×7, 300 ×3 | 500 |
| „w pobliżu” (1a) | 500 ×10 | 500 |
| „niedaleko” (1d) | 500 ×6, 1000 ×4 | 500 |
| „w okolicy” | 500 ×10 | 500 |
| „w zasięgu krótkiego spaceru” | 500 ×5, 800 ×5 | 650 |
| „najbliższe” (bez liczby) | `LIMIT 10` ×10 | – |

Skala jest uporządkowana i zgodna z intuicją: „bardzo blisko” < „rzut beretem” ≤ „w pobliżu” = „w okolicy” ≤ „niedaleko” < „krótki spacer”. Różnice są jednak małe, wszystko mieści się w 300–800 m, a „w okolicy” nie jest szersze niż „w pobliżu”. „Krótki spacer” model sam przelicza: „krótki spacer = 500 m (ok. 5–7 minut)”. „Najbliższe” bez liczby to zawsze 10 obiektów, z uzasadnieniem „Pytanie nie określa liczby aptek, więc zwracam 10 najbliższych”.

### 8.3. Sytuacja do wywnioskowania

| Sytuacja | Promień (10 prób) | Mediana | Jak model to uzasadnia (cytaty z uwag) |
|---|---|---|---|
| brak (1a) | 500 ×10 | 500 | – |
| „Mam 10 minut do odjazdu pociągu.” (1e) | 500 ×10 | 500 | „przy 10 minutach do odjazdu »w pobliżu« oznacza ok. 500 m (kilka minut pieszo)” |
| „Idę pieszo.” (1b) | 800 ×7, 1000 ×3 | 800 | – |
| „Jestem z małym dzieckiem.” | 1000 ×7, 800 ×2, 700 ×1 | 1000 | „promień 1000 m (ok. 10–15 min spaceru z dzieckiem)” |
| „Poruszam się na wózku inwalidzkim.” | 1000 ×9, 500 ×1 | 1000 | „Baza nie zawiera informacji o dostępności dla wózków inwalidzkich (brak atrybutu wheelchair)…” |
| „Pilnie potrzebuję leków.” | 1000 ×10 | 1000 | brak uzasadnienia promienia, tylko „przyjęto promień 1 km” |
| „Jestem na rowerze.” | 1500 ×10 | 1500 | „Ponieważ użytkownik jest na rowerze, »w pobliżu« przyjęto jako promień 1500 m (ok. 5 min jazdy rowerem)” |
| „Jadę samochodem.” (1c) | 1000 ×9, 1500 ×1 | 1000 | – |

- **Rower daje większy promień niż samochód** (1500 m i 1000 m), czyli kolejność środków transportu nie jest spójna.
- **Wózek i małe dziecko dają zwykle więcej niż „pieszo”** (mediany 1000 m i 800 m; zakresy się nakładają), choć zdroworozsądkowo powinno być mniej. Przy wózku model skupia się na tym, czego nie ma w danych (dostępność), a nie na zasięgu. Przy dziecku liczy „10–15 minut spaceru”, ale z tego samego założenia wychodzi mu większa odległość.
- **„Pilnie”** podwaja promień (500 → 1000 m) bez wyjaśnienia. Przy „Mam 10 minut do odjazdu” zostaje przy 500 m z rozsądnym uzasadnieniem.
- Ogólny wzorzec z §2 (punkt 4): **każde dodatkowe zdanie o sytuacji (poza pośpiechem) zwiększa promień w stosunku do pytania bez kontekstu.**

### 8.4. Język pytania

| Pytanie | Promień (10 prób) |
|---|---|
| Wymień apteki w pobliżu Dworca Centralnego. (1a) | 500 ×10 |
| List pharmacies near Warsaw Central railway station. | 500 ×10 |
| Jadę samochodem. Wymień apteki w pobliżu Dworca Centralnego. (1c) | 1000 ×9, 1500 ×1 |
| I'm driving. List pharmacies near Warsaw Central railway station. | **500 ×6, 1000 ×4** |

- Bez kontekstu język nie ma znaczenia: „near” = „w pobliżu” = 500 m. Model nie przeszedł na mile (np. pół mili = 805 m).
- **Informacja o samochodzie działa słabiej po angielsku:** mediana zostaje przy 500 m, a 1000 m pada tylko w 4 z 10 prób. Po polsku to 1000 m w 9 z 10. Uwagi model pisze po polsku także przy angielskim pytaniu (20 na 20 prób).

---

## 9. Zachowania przekrojowe

### 9.1. Ujawnianie założeń

| Część | Prób | Uwagi niepuste | Ujawniona wartość lub założenie |
|---|---|---|---|
| 2a | 230 | 230 | 229 |
| 2b | 40 | 40 | 38 (2 odmowy bez liczby) |
| 2c | 50 | 50 | 50 |
| 2d | 60 | 60 | 60 |
| 2e | 180 | 180 | 104 (często nie ma czego ujawniać) |
| 2f | 180 | 180 | 179 |
| 2g | 100 | 100 | 40 (jak w 2e, często nie ma czego ujawniać) |

### 9.2. Czy uwagi mówią prawdę

Porównaliśmy liczbę z jednostką podaną w uwagach („przyjęto promień 1,5 km”, „co najmniej 10 ha”) z wartością w SQL we wszystkich próbach z promieniem albo progiem. W 549 próbach uwagi podają liczbę (w jednej jej brak) i **wszystkie 549 zgadzają się z SQL.** Model nigdy nie napisał jednej wartości, używając innej. Uwagi są więc wiarygodnym źródłem informacji o interpretacji, a nie tylko ozdobą.

### 9.3. Powtarzalność

- **Wartość jest stabilniejsza niż SQL.** W 2a żaden wariant nie dał 10 razy identycznego SQL, ale 11 z 23 wariantów dało 10 razy tę samą wartość.
- **Rozrzut jest skokowy:** wartości przeskakują między sąsiednimi okrągłymi liczbami (800 i 1000, 1500 i 2000, 3000 i 3750), nigdy nie wypadają pomiędzy.
- **Replikacja w osobnym uruchomieniu** (112 prób): 108 ma ten sam rodzaj interpretacji co seria główna, a 99 wartość w zakresie serii głównej. Różnice to odmowa w 8a i obiekty w 2e.

### 9.4. Odmowy

22 puste SQL na 840: 8a (10), 8c (10) i palma (2). Wszystkie z sensownym uzasadnieniem. Model nie odmówił ani razu przy „w pobliżu”, „w centrum” czy „duże”, choć te określenia są równie niejasne jak „w 15 minut”. **Odmawia, gdy brakuje mu danych do obliczenia (sieci dróg) albo obiektu (palma). Niejasność znaczenia nie jest dla niego powodem do odmowy.**

### 9.5. Obiekty zapisane jako poligony

K2 mówi, że ten sam rodzaj obiektu bywa w tabeli punktów i poligonów. W 480 zapytaniach z SQL w częściach 2a, 2b, 2c i 2f tabelę poligonów uwzględniło 256 (53%). Model zwykle zaznacza w uwagach, że ją pominął. To nie zmienia przyjętej wartości, ale zmienia liczbę wyników, co ma znaczenie przy porównywaniu liczby wierszy (§12).

### 9.6. Czy model nazywa pytanie niejasnym

Szukaliśmy w uwagach słów „niejednoznaczne”, „niejasne”, „nieprecyzyjne”, „nie wiadomo” i podobnych.

| Część | Prób | Uwagi nazywają pytanie niejasnym |
|---|---|---|
| 2a „w pobliżu” | 230 | 0 |
| 2b czas dojazdu | 40 | 3 (wszystkie w odmowach 8a: raz brak środka transportu, dwa razy niejednoznaczne położenie dworca) |
| 2c „w centrum” | 50 | 8 (wszystkie w 9c, pytaniu bez nazwy miasta: „Pytanie jest niejednoznaczne: nie podano miasta ani granic centrum”) |
| 2d „duże” i „małe” | 60 | 0 |
| 2f dodatkowe kontrasty | 180 | 0 |
| 2h „od metra” | 10 | 3 (np. „nie podano konkretnej stacji”) |

W częściach 2e i 2g takie słowa pojawiają się w 1 na 180 i 2 na 100 prób. Model zgłasza niejasność prawie wyłącznie wtedy, gdy w pytaniu brakuje elementu (miasta, stacji, środka transportu). Niejasnego słowa („w pobliżu”, „duży”, „w okolicy”) nie zgłasza ani razu, choć jego wartość zawsze podaje (§9.1).

---

## 10. Kontrola jakości

Badanie robiliśmy w pętli: generowanie → wykonanie → odczyt → przegląd z SQL → poprawka **narzędzi** (nigdy wyników) → ponowny odczyt.

1. **Każdy odczyt zestawiony z fragmentem SQL, z którego pochodzi:**
   - 490 promieni z `ST_DWithin` (w 20 zapytaniach z 22b i 22c drugi, mniejszy `ST_DWithin` to odległość stacji od torów `subway`, a za promień uznajemy większy),
   - 60 progów `ST_Area` (dwa zapytania mają dodatkowy warunek „> 0,5”, czyli udział parku w granicy miasta, a nie próg wielkości),
   - 10 razy `LIMIT 10`.
2. **Przypisanie wyników 2e do kandydatów sprawdzone ściśle.** Każdy wynik musi się zgadzać z wartością kandydata co do 5 m. Gdy się nie zgadzał, czytaliśmy SQL. Tak wykryliśmy:
   - odległości liczone do środka poligonu PKiN (palma 1018 m, Mały Powstaniec 1969 m, Centrum 311 m), czyli poprawne, ale brakowało ich w tabeli kandydatów,
   - aptekę „Syrenka” (1935 m), którą tolerancja 4% przypisywała do Syreny nad Wisłą,
   - środki ciężkości wielu obiektów (31 755 m, 3889 m).

   Poprawiliśmy **tabelę kandydatów** (`h2/references.py`), a nie pojedyncze próby. Plik ręcznych korekt `wyniki/korekty.json` jest pusty.

   **Niezależna identyfikacja obiektu** (`h2/identify.py`, dodana przy części 2g). Dla każdego obiektu w bazie, którego nazwa zawiera rdzeń („chopin”, „syren”, „powsta”…), skrypt liczy odległość do PKiN w każdej kombinacji geometrii (punkt, obrys, środek, budynek). Wynik modelu przypisuje do obiektu, który daje tę samą odległość z dokładnością do 2 m, a ocenę wyprowadza z osm_id i położenia obiektu. Ta metoda **potwierdziła wszystkie 160 ocen z 2e bez zmian.** W 2g rozpoznała obiekty, których nie było na liście kandydatów: szkołę, kebab, „Fortepian Chopina”, „Las Palmas”, „Stadion Syrenki”. Bez identyfikacji przypisana do listy zostaje tylko odległość liczona do środka ciężkości wielu obiektów naraz (2 próby). Gdy w granicy 2 m pasuje kilka obiektów, decyduje najbliższe dopasowanie, np. pomnik Kopernika (0,03 m) przed tablicą informacyjną stojącą obok (0,86 m).
3. **Pusty wynik ≠ mały promień:** test z promieniem 10⁸ m rozdziela nieznaleziony punkt odniesienia (4c) od za małego promienia (4a, 4b, Krusze).
4. **Pusty wynik w 2e: który obiekt zawiódł?** Każde podzapytanie jest wykonywane osobno. Wynik NULL (zamiast 0 wierszy) też jest diagnozowany. 6 pustych wyników to wina PKiN, a nie obiektu z pytania.
5. **Sprawdzenie w OpenStreetMap, czym jest wybrany obiekt.** Rzeźba „Syrenka” z 16a i 16b to węzeł 7641177462: `artwork_type=statue`, `artist_name=Ryszard Kozłowski`, `disused:amenity=fountain`, `material=concrete`. To nie Syrenka z Rynku ani znad Wisły.
6. **Wartości wzorcowe** policzone ręcznie napisanym SQL, niezależnie od modelu ([pytania.md](pytania.md)).
7. **Uwagi a SQL:** zgodność liczb sprawdzona automatycznie (§9.2).
8. **Replikacja w osobnym uruchomieniu** (§9.3).
9. **Wrażliwość na próg ilorazu** (1,25 / 1,5 / 2) (§3.2).
10. **Środowisko:** rola tylko do odczytu `pbad_ro` według `H1/plan-uruchomienia.md`, sprawdzona (`CREATE TABLE` odrzucony). Brakujący w venv `psycopg` doinstalowany w wersji z `requirements.txt`.

---

## 11. 5 czy 10 powtórzeń

Pierwsza seria miała 5 prób na wariant. Dołożyliśmy próby 6–10 i porównaliśmy wyniki z prób 1–5 z wynikami z prób 1–10 (tabele, §10).

- **Opis czynników się nie zmienia.** S, M i O mają „wyraźny wpływ” przy 5 i przy 10 próbach (S: 7/8 → 6/8, M: 9/9 → 9/9, O: 9/9 → 9/9).
- **Ale 5 z 56 wariantów z przyjętą wartością (2a–2d, 2f) zmienia medianę.** To warianty, w których model waha się między dwiema wartościami mniej więcej pół na pół: 3c (2000 ×5, 1500 ×5), 5c, 7c, 8d, 25c (500 ×5, 800 ×5). Przy 5 próbach mediana zależy od przypadku. W dwóch parach zmienia to opis:
  - lotnisko „bez informacji” → „samochodem”: przy 5 próbach rośnie, przy 10 bez zmiany,
  - „krótki spacer” wobec „w pobliżu”: przy 5 bez zmiany, przy 10 rośnie.
- **Rzadkie duże pomyłki wychodzą dopiero przy 10 próbach.** Pomnik Chopina w Radomiu i pod Sochaczewem (15a), apteka „Syrenka” i środek ciężkości „Syrenek” (16a), „palma” 3889 m (19) oraz jedyne trafienie Małego Powstańca (20) to wszystko próby 6–10. Przy 5 próbach 15a wyglądało na „zawsze pusty wynik”.

Dlatego zostajemy przy 10 próbach. Wnioski o kierunku efektów są stabilne, a 10 prób pokazuje rozrzut i rzadkie zachowania, które przy 5 próbach są niewidoczne.

---

## 12. Na co uważać przy porównaniach i opisie

1. **Porównujemy mediany i rozkłady, nie pojedyncze próby.** Model często waha się między dwiema sąsiednimi wartościami. Przy wariantach „pół na pół” (3c, 5c, 25c) mediana jest średnią dwóch wartości (1750, 650) i nie odpowiada żadnej próbie. W tekście lepiej podawać rozkład („2000 ×5, 1500 ×5”).
2. **Powtórzenia nie są niezależnymi osobami.** Model jest prawie deterministyczny. 10 identycznych wartości nie oznacza, że „wszyscy się zgadzają”, tylko że model ma jedną odpowiedź. Prawdziwą jednostką porównania jest para pytań.
3. **Czynniki są splątane:**
   - „Miejsce” zmienia naraz gęstość okolicy, rodzaj stacji i miasto,
   - „Rodzaj obiektu” zmienia naraz skalę i rzadkość (szpitali jest mniej niż aptek).

   Wynik „rodzaj obiektu działa najsilniej” można też czytać jako „model wie, że szpitali jest mało”.
4. **Liczba wierszy nie mierzy interpretacji.** Zależy też od tego, czy model dołączył tabelę poligonów (53% zapytań), czy znalazł punkt odniesienia i czy użył `DISTINCT`. Do porównań bierzemy przyjętą wartość, a liczbę wierszy tylko jako ilustrację skutków.
5. **Pusty wynik ma co najmniej trzy różne przyczyny:** za mały promień (4a, Krusze), nieznaleziony punkt odniesienia (4c) albo nieznaleziony drugi obiekt (PKiN w 2e). Trzeba je rozdzielać, inaczej przypisuje się modelowi złą interpretację tam, gdzie zawiodło dopasowanie nazwy.
6. **Odmowa zmienia liczbę porównań.** 8c odpada, więc czynnik S ma 8 par, a nie 9. Odmowy raportujemy osobno, bo same są wynikiem.
7. **W 2e odległość od obrysu i od środka są obie poprawne,** a różnią się do 36% (Łazienki–PKiN). Porównując z wzorcem, trzeba mieć kandydatów dla każdej kombinacji geometrii.
8. **Tolerancja przy dopasowaniu może ukryć złą odpowiedź.** Apteka „Syrenka” (1935 m) mieściła się w tolerancji 4% od Syreny nad Wisłą (1900 m). Przypisanie trzeba potwierdzać tym, co wybiera SQL, a nie samą liczbą. Dlatego w ostatecznej wersji obiekt identyfikujemy po osm_id (§10, punkt 2).
9. **Pole `uwagi` może zawyżać ujawnianie założeń.** Format `{"sql", "uwagi"}` sam podsuwa miejsce na komentarz. Wynik „ujawnia w 99%” dotyczy tego formatu.
10. **Części 2f i 2g dodaliśmy po obejrzeniu pierwszych wyników.** Pytania dobraliśmy, wiedząc już, co wyszło w 2a–2e. Wyniki 2f i 2g opisujemy jako obserwacje i sprawdzenia konkretnych wątków, a nie jako zaplanowane z góry porównania. Wskazówka w 2g to jedno sformułowanie: inne mogłoby dać inny bilans trafień i pomyłek.
11. **Wartości między częściami porównujemy ostrożnie.** Pytania 2f mają tę samą formę co 1a, więc z 1a je zestawiamy. Części 2c, 2d i 2e mają inne sformułowania.
12. **Pilotaż (13.11) i seria różnią się w szczegółach.** W pilotażu 1a dało 1000 m, a w serii 500 m w 10 na 10 próbach. Pilotaż to ilustracja, a nie pomiar. W artykule podajemy datę serii i identyfikator modelu.

---

## 13. Ograniczenia

- **Jeden model** (`claude-sonnet-5-5`, `effort: medium`), jeden poziom kontekstu (K2), jeden region. Inne modele mogą mieć inne wartości domyślne.
- **Czynniki splątane** (§12.3) i mała liczba par na czynnik (8–9).
- **Brak punktu odniesienia ludzkiego.** Nie oceniamy, czy 500 m to „dobra” interpretacja apteki w pobliżu dworca. Opisujemy, jaką wartość model przyjmuje i jak zależy ona od kontekstu; tam, gdzie mówimy o rozsądnej wartości, to nasza ocena.
- **Część 2e zależy od tego, jak obiekt zapisano w OSM.** „Kolumna Zygmunta 0/10” mówi, że model nie przewiduje zapisu poligonowego, a nie że nie zna Kolumny.
- **Części 2f i 2g są eksploracyjne** (§12.10). Każdy kontrast w 2f ma jedną albo dwie pary, a w 2g sprawdziliśmy tylko jedno sformułowanie wskazówki.
- **Ustawienie:** model nie widział danych, nie mógł dopytać i miał pole na uwagi. Część zachowań (brak dopytania, stała wartość niezależna od danych, wysoki odsetek ujawnionych założeń) wynika z tego ustawienia.
- **Badanie eksploracyjne.** Możliwe rozszerzenia: §14, punkt 9.
- **Dane OSM to zrzut z 2026-11-20.**

---

## 14. Wnioski do artykułu

1. **Jak model interpretuje niejasne określenia (pierwsza część PB2):** zawsze jako jedną konkretną, okrągłą wartość (11 różnych promieni na 470), powtarzalną między próbami (w 52 z 56 pytań ta sama wartość w co najmniej 6 na 10 prób). Model ma więc stałe wartości domyślne, a nie losuje.
2. **Czy kontekst zmienia przyjętą wartość (druga część PB2):** tak, wszystkie trzy czynniki przesuwają ją w zdroworozsądkowym kierunku. Kolejność siły jest jednak inna, niż zakładaliśmy: rodzaj obiektu (9/9 par, zakresy rozłączne) > miejsce (9/9) > podana wprost sytuacja pytającego (6/8). W skali możliwych odpowiedzi z planu (od „żaden czynnik nie działa” do „wszystkie trzy działają”) wynik leży blisko drugiego końca, z zastrzeżeniem z punktu 3.
3. **Jak kontekst działa: zgrubnie, szufladkami.** Centrum Warszawy 500 m, a wszystko inne 1000 m (wieś tak samo jak Radom); „duży” zależy od miasta, „mały” nie; rower dalej niż samochód; po angielsku samochód zmienia mniej. Model reaguje na pojedyncze cechy pytania (rodzaj obiektu, „centrum Warszawy”, rower), a nie na sytuację jako całość.
4. **Nazwy potoczne:** model przyjmuje najbardziej znane znaczenie (Łazienki Królewskie, stacja metra Politechnika, nigdy przystanek „Metro Politechnika”). Wybory dodatkowe (od obrysu czy od środka, „nad Wisłą”) robi po cichu. Przy małych obiektach interpretacja jest właściwa, ale trafienie w zapis w bazie słabe (pomniki 19/60).
5. **Jawność interpretacji:** przyjętą wartość model podaje prawie zawsze i zgodnie z SQL (549/549), ale niejasność pytania zgłasza prawie wyłącznie wtedy, gdy czegoś w nim brakuje (miasta, stacji, środka transportu). Samo niejasne słowo nie jest dla niego problemem: „w pobliżu” 0 zgłoszeń na 230 prób.
6. **Odniesienie do literatury:** AmbiQT (praca 10) pokazuje, że modele trzymają się jednej interpretacji niejednoznacznego pytania. Nasze wyniki to potwierdzają (powtarzalność) i dokładają brakujący element: ta jedna interpretacja zależy od kontekstu pytania, w opisany wyżej, szufladkowy sposób.
7. **Skutki (zależne od ustawienia):** stała wartość daje pusty wynik tam, gdzie obiektów jest mało (Krusze, Płudy, parki w Radomiu, 9–10 na 10 prób), a jedna wskazówka w kontekście przestawia rozstrzyganie nazw (2g: mniej pustych wyników, ale więcej trafień w zupełnie inne obiekty).
8. **Rekomendacje praktyczne** dla systemów text-to-SQL na danych przestrzennych:
   - pokazywać użytkownikowi przyjętą wartość i wybrany obiekt („promień 500 m”, „Łazienki Królewskie, od środka parku”), bo model rzetelnie je podaje,
   - nie liczyć na to, że model sam zgłosi niejasność: przy niejasnych słowach („w pobliżu”, „duży”) nie zgłasza jej prawie nigdy,
   - przy nazwach potocznych sprawdzać, który obiekt został wybrany, a nie tylko, czy wynik nie jest pusty,
   - do oceny takich systemów potrzeba co najmniej ok. 10 powtórzeń, bo rzadkie zachowania przy 5 próbach są niewidoczne (§11).
9. **Charakter badania i możliwe rozszerzenia:** badanie jest eksploracyjne: jeden model, jedno ustawienie (bez dostępu do danych, bez możliwości dopytania), 10 prób na pytanie, a ocenę rozsądnej wartości przyjmujemy sami. Naturalne rozszerzenia to: kilka modeli (czy wartości domyślne i szufladki są cechą ogólną), wariant z dostępem do bazy (czy model dopasuje wartość do danych), możliwość dopytania użytkownika oraz sprawdzenie, na ile przyjmowana wartość zależy od wiedzy modelu o konkretnym miejscu (np. czy rozpoznaje miejscowość jako wieś).

---

## 15. Jak powtórzyć

```bash
cd python/console
python run_h2.py status            # postęp (domyślnie 10 powtórzeń)
python run_h2.py run               # brakujące wywołania → wyniki/odpowiedzi.jsonl (wznawia przerwaną serię)
python run_h2.py exec              # wykonanie SQL rolą pbad_ro → wyniki/wykonania.jsonl
python run_h2.py extract           # odczyt wartości → wyniki/odczyty.jsonl
python run_h2.py report            # porównania i tabele → wyniki/tabele.md
python run_h2.py show 15a          # SQL, uwagi i odczyt jednego wariantu
python run_h2.py replicate         # seria kontrolna → wyniki/replikacja.jsonl
```

| Plik | Zawartość |
|---|---|
| `wyniki/odpowiedzi.jsonl` | 840 odpowiedzi modelu (SQL, uwagi, tokeny, czas) |
| `wyniki/wykonania.jsonl` | wyniki wykonania (pierwsze 100 wierszy, liczba wierszy, błąd) |
| `wyniki/odczyty.jsonl` | odczytana wartość, rodzaj interpretacji, zidentyfikowany obiekt i jego ocena, diagnoza pustych wyników |
| `wyniki/replikacja.jsonl` | 112 odpowiedzi serii kontrolnej |
| `wyniki/korekty.json` | ręczne korekty odczytu (pusty) |
| `wyniki/tabele.md` | wszystkie tabele, generowane |

---

## 16. Szkielet części artykułu o PB2

Propozycja, jak ułożyć tę część artykułu. Przy każdym punkcie: liczby do zacytowania i gdzie są w tym pliku. Wszystkie pochodzą z serii z 24.11.2026 (`claude-sonnet-5-5`, effort `medium`, kontekst K2, 10 prób na wariant); pytanie dodatkowe 2h z 25.11.2026.

**Główna teza:** model rozstrzyga niejasne określenia przestrzenne za użytkownika jedną stałą, okrągłą wartością. Kontekst pytania przesuwa ją w zdroworozsądkowym kierunku, ale zgrubnie, kilkoma szufladkami. Przyjętą wartość model podaje, ale prawie nigdy nie mówi, że pytanie było niejasne.

### Metoda (krótko)

- 84 warianty pytań w 7 częściach, po 10 prób (840 wywołań), oraz jedno pytanie dodatkowe (2h). Kontekst bazy K2, odpowiedź `{"sql", "uwagi"}` z neutralnym opisem pola uwag.
- Model nie widział danych, odpowiadał w jednym kroku i nie mógł dopytać: mógł napisać zapytanie albo odmówić.
- Przyjętą wartość odczytujemy z SQL (promień, próg, `LIMIT`). Dla nazw potocznych identyfikujemy wybrany obiekt po osm_id.
- Analiza opisowa: rozkłady z 10 prób, mediany, iloraz median z progiem 1,25 i tabelą wrażliwości. Bez testów statystycznych.

### Wyniki: proponowana kolejność

1. **Jedna konkretna, okrągła wartość** (§2 A, §3.1, §8.2). 11 różnych promieni na 470; „w pobliżu” apteki 500 m, szpitala 2000 m; „centrum Warszawy” koło 1,5 km; „mały park” 1 ha; „najbliższe” 10 obiektów. **Proponowana Tabela 1:** tabela określeń z §2, punkt 1.
2. **Powtarzalność** (§2, punkt 2; §9.3). 27/56 pytań identycznie w 10 na 10, 52/56 w co najmniej 6 na 10.
3. **Kontekst działa, w innej kolejności niż zakładaliśmy** (§2 B, §3.2). Rodzaj obiektu 9/9 (zakresy rozłączne), miejsce 9/9, sytuacja 6/8. **Proponowana Tabela 2:** promienie z §3.1 (obiekt × miejsce × sytuacja).
4. **Szufladki** (§2 C, §8.1, §6, §8.3). Centrum Warszawy 500 m, reszta 1000 m (wieś jak Radom); „duży” 20/10/5 ha, „mały” 1 ha; rower 1500 m > samochód 1000 m, z wyjaśnieniem z uwag. **Proponowany rysunek:** promień dla kolejnych miejscowości (gradient z §8.1).
5. **Nazwy potoczne** (§2 D, §7.1, §7.7). Najbardziej znane znaczenie (Łazienki 40/40, metro: Politechnika 10/10, nigdy przystanek); ukryte wybory (obrys czy środek, „nad Wisłą”).
6. **Jawność interpretacji** (§2 E, §9.2, §9.6). Wartość podana w 556/560, zgodna z SQL 549/549; niejasność zgłoszona w 11/560, prawie wyłącznie gdy czegoś brakuje (miasto, stacja, środek transportu), przy „w pobliżu” 0/230.
7. **Skutki, krótko** (§2 F). Puste wyniki na wsi, przy Płudach i w Radomiu; wskazówka w 2g przestawia rozstrzyganie nazw (14 → 38/80 dobrych, ale 5 → 20 dużych pomyłek).

### Dyskusja: możliwe wyjaśnienia (oznaczyć, co jest hipotezą)

- **Okrągłe wartości i powtarzalność** (hipoteza): model odtwarza najczęstsze konwencje z tekstów i przykładów kodu („w promieniu 500 m”, `ST_DWithin(..., 1000)`) i wybiera najbardziej prawdopodobną odpowiedź.
- **Kierunek wpływu kontekstu** (hipoteza): wiedza o świecie z tekstów, np. że szpitali jest mniej niż aptek, a na peryferiach obiekty są rzadsze.
- **Słaby wpływ sytuacji pytającego** (częściowo poparte uwagami): informację o samochodzie model traktuje jako coś, czego nie umie użyć bez sieci dróg (cytaty z uwag, §4 i §2 C), a rower przelicza na minuty jazdy.
- **Szufladki** (hipoteza): wiedza kategorialna („centrum dużego miasta” a „reszta”) zamiast liczbowej o gęstości obiektów; mało znane miejsce trafia do szufladki domyślnej. Nie sprawdzaliśmy, co model wie o Kruszach.
- **Brak zgłaszania niejasności** (hipoteza, częściowo skutek ustawienia): model jest uczony dawać odpowiedź, a rozstrzyganie niejasnych słów traktuje jako rutynę; zadanie brzmiało „wygeneruj zapytanie”.
- **Związek z eksperymentem 1 (H1):** w obu eksperymentach więcej wiedzy o danych prowadzi do ściślejszych zapytań, które częściej rozmijają się z zapisem w OSM (§7.3).

### Ograniczenia i możliwe rozszerzenia

Badanie eksploracyjne: jeden model, jedno ustawienie (bez dostępu do danych, bez dopytania, z polem na uwagi), czynniki splątane (§12, punkt 3), kilka obserwacji opartych na jednej parze pytań (rower i samochód, język), części 2f–2h dodane po obejrzeniu wyników (§12, punkt 10), ocena rozsądnej wartości należy do nas, dane OSM z jednego dnia (§13). Rozszerzenia: §14, punkt 9.

### Uwaga o liczbach

Przy cytowaniu podawać rozkład („500 ×9, 1000 ×1”), a nie tylko medianę. Przy wariantach „pół na pół” mediana nie odpowiada żadnej próbie (§12, punkt 1). Pełne tabele: [wyniki/tabele.md](wyniki/tabele.md).
