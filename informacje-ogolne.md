## Cel badania (co chcemy się dowiedzieć i po co)

Chcemy sprawdzić, jak różne sposoby zwiększania kontekstu wpływają na jakość zapytań przestrzennych SQL generowanych przez modele językowe oraz jak modele te radzą sobie z niejasnymi pytaniami. Dzięki temu dowiemy się, jakie informacje warto przekazywać modelowi i na ile można polegać na jego interpretacji pytań o dane przestrzenne.

## Hipoteza badawcza (hipoteza musi być testowalna)

**H1:** Opis tego, co zawierają dane, poprawia trafność zapytań przestrzennych SQL bardziej niż sam opis struktury bazy danych.

> Wyjaśnienie: opis struktury to nazwy tabel i kolumn wraz z typami, w tym typem geometrii i układem współrzędnych. Opis zawartości danych to znaczenie tabel i kolumn, dopuszczalne wartości typu obiektu (np. `'pharmacy'`) oraz fakty o danych, np. że ten sam rodzaj obiektu bywa zapisany raz jako punkt, a raz jako poligon, albo że brak nazwy to pusty napis. W eksperymencie porównujemy cztery kolejne poziomy kontekstu, każdy zawierający poprzedni: K0 (same nazwy tabel i kolumn), K1 (struktura z typami), K2 (K1 + opis zawartości danych) i K3 (K2 + wskazówki, jak pisać zapytania przestrzenne, i przykłady). Hipoteza zakłada, że przyrost trafności między K1 a K2 jest większy niż między K0 a K1. Szczegóły: [poziomy-kontekstu.md](eksperyment/poziomy-kontekstu.md).

**H2:** Im bardziej niejasne jest pytanie, tym bardziej wynik zależy od założeń, które model przyjmuje samodzielnie i nie ujawnia pytającemu, przez co wynik staje się dla pytającego nieprzewidywalny.

> Wyjaśnienie: hipoteza ma trzy mierzalne części.
>
> 1. **Model przyjmuje własne założenia.** Przy sformułowaniach takich jak „w pobliżu” czy „10 minut spacerem” model sam wybiera wartości parametrów, np. promień w metrach albo prędkość marszu. Odczytujemy je z wygenerowanego SQL.
> 2. **Model ich nie ujawnia.** Model nie odmawia odpowiedzi, nie dopytuje i nie zaznacza, że pytanie jest niejasne, tylko zwraca zapytanie jak poprawną odpowiedź. Sprawdzamy to w polu `uwagi` odpowiedzi.
> 3. **Wynik jest nieprzewidywalny dla pytającego.** Może tak być na dwa sposoby:
>    - kolejne odpowiedzi na to samo pytanie zwracają różne zbiory obiektów, co mierzymy średnim indeksem Jaccarda między powtórzeniami,
>    - model zawsze przyjmuje tę samą wartość domyślną, np. „w pobliżu” = 500 m, ale pytający jej nie zna.
>
> Literatura (AmbiQT, praca 10 w przeglądzie) sugeruje, że modele trzymają się jednej interpretacji, więc spodziewamy się raczej drugiego przypadku. Hipoteza zostanie obalona, jeśli model przy niejasnych pytaniach będzie wyraźnie sygnalizował przyjęte założenia albo dopytywał o nie.

## Metoda (jakie narzędzia badawcze, jakie eskperymenty, warunki eksperymentów, jakie narzędzia informatyczne, punkt odniesienia)

- **Eksperyment 1 (H1):** 20 pytań testowych (po 4 z każdej kategorii zapytań, w tym kilka o mało znane obiekty) zadajemy modelowi na czterech poziomach kontekstu (K0–K3), po 3 powtórzenia. Używamy naturalnej wersji pytań (bez nazw tabel i kolumn), bo wersja precyzyjna sama podaje modelowi część kontekstu. Liczymy odsetek poprawnych zapytań. Zapytanie jest poprawne, gdy zwraca taki sam wynik jak zapytanie wzorcowe, według zasad porównania opisanych niżej. Każdą próbę oceniamy osobno, a odsetek liczymy ze wszystkich prób na danym poziomie.
- **Eksperyment 2 (H2):** około 5 zadań zapisujemy na trzech poziomach niejasności: S1 jasne (wszystko podane wprost), S2 średnio niejasne (jest konkretna miara, ale trzeba ją przeliczyć, np. „10 minut spacerem”) i S3 bardzo niejasne (model sam musi przyjąć wartość, np. „w pobliżu”). Każde pytanie zadajemy 10 razy przy stałym kontekście **K3**. K3 zawiera wskazówki dotyczące jednostek i przykłady, więc różnice między powtórzeniami nie wynikają z błędów technicznych, np. liczenia odległości w stopniach zamiast w metrach. Wszystkie zadania zwracają **listę obiektów** (`osm_id` i nazwę), a nie pojedynczą liczbę, żeby dało się policzyć indeks Jaccarda. Model odpowiada w formacie JSON: `{"sql": "...", "uwagi": "..."}`, gdzie pole `uwagi` może pozostać puste. Z SQL odczytujemy przyjęte wartości (np. promień), a z pola `uwagi` sprawdzamy, czy model zasygnalizował niejasność. Przykładowe pytania: [plan-eksperymentow.md](eksperyment/plan-eksperymentow.md).
- **Zasady porównania wyników z wzorcem (eksperyment 1):**
  - Dla każdego pytania ustalamy kolumny kluczowe, np. `name` albo liczbę. Pozostałe kolumny w wyniku modelu ignorujemy.
  - Wiersze porównujemy jako zbiory, bez względu na kolejność. Kolejność ma znaczenie tylko w pytaniach o „najbliższe” i „top k”.
  - Liczby zmiennoprzecinkowe (odległości, powierzchnie, długości) uznajemy za równe przy różnicy do 1%, żeby różne zaokrąglenia nie były traktowane jako błąd.
  - Napisy porównujemy dokładnie.
  - Zapytanie, które się nie wykonuje, jest niepoprawne.
- **Warunki eksperymentów:** jedno wywołanie modelu bez historii i bez poprawiania zapytań, ten sam model i te same ustawienia we wszystkich próbach. Pytania, treść poziomów i kryteria oceny ustalamy przed badaniem.

## Potrzebne zasoby, dane, materiały

- Dane OpenStreetMap dla województwa mazowieckiego z Geofabrik: https://download.geofabrik.de/europe/poland/mazowieckie.html
- Dokumentacja danych Geofabrik: https://download.geofabrik.de/osm-data-in-gis-formats-free.pdf
- Baza PostgreSQL z PostGIS uruchamiana w Dockerze: [docker-compose.yml](docker/docker-compose.yml)
- `ogr2ogr` do załadowania danych do bazy: z QGIS (OSGeo4W Shell) albo z obrazu Dockera `ghcr.io/osgeo/gdal`, bez instalowania QGIS. Instrukcja: [dane-testowe.md](dane/dane-testowe.md)
- Claude API z określonym budżetem
- Zestaw pytań testowych

## Zmienne zależne/niezależne (co będzie zmieniane, co będzie mierzone)

**Zmieniamy (zmienne niezależne):**
- Eksperyment 1: ilość i rodzaj informacji o bazie w prompcie, czyli poziom kontekstu K0–K3.
- Eksperyment 2: stopień niejasności pytania, czyli S1, S2 i S3.

**Mierzymy (zmienne zależne):**
- Eksperyment 1:
  - odsetek poprawnych zapytań, łącznie i osobno dla każdej kategorii zapytań,
  - odsetek zapytań, które w ogóle się wykonują,
  - rodzaje błędów: zła tabela, zła wartość typu obiektu, liczenie w stopniach zamiast w metrach, współrzędne wpisane z pamięci zamiast pobrane z bazy, zła funkcja przestrzenna, zła agregacja,
  - liczba tokenów w prompcie, czyli koszt danego poziomu kontekstu.
- Eksperyment 2:
  - powtarzalność wyniku, czyli średni indeks Jaccarda między wynikami 10 powtórzeń,
  - przyjęte wartości parametrów (np. promień w metrach, prędkość marszu) i ich rozrzut,
  - odsetek odpowiedzi, w których model zasygnalizował niejasność.

**Nie zmieniamy (zmienne kontrolowane):** model i jego ustawienia, instrukcja zadania, baza danych, treść pytań w obrębie danego eksperymentu.

## Oczekiwane wyniki (jakie są możliwe wyniki i jak zaadresują hipoteze, co dodatkowego można sprawdzić/zrobić)

**H1.** Spodziewamy się, że najsłabiej wypadnie K0, a największy skok nastąpi między K1 a K2, bo to tam model dowiaduje się o pułapkach w danych. Najczęstsze z nich to szpitale i szkoły zapisane w dwóch tabelach, puste nazwy oraz to, że Dworzec Centralny nazywa się w bazie „Warszawa Centralna”. Między K2 a K3 spodziewamy się mniejszego przyrostu.
- Jeśli największy skok będzie między K0 a K1, to dla współczesnych modeli ważniejsza jest sama struktura bazy niż jej opis, czyli H1 zostanie obalona.
- Jeśli największy skok będzie między K2 a K3, to modelowi nie wystarczą fakty o danych i potrzebuje gotowych wzorców zapytań.
- Każdy z tych wyników da się opisać w artykule.

**H2.** Spodziewamy się, że:
- dla pytań S1 wyniki będą prawie zawsze takie same,
- dla S2 model przeliczy miarę, ale z różnymi założeniami (np. 10 minut spacerem to 800 m albo 1 km),
- dla S3 model przyjmie jedną „okrągłą” wartość, np. 500 m albo 1 km, i rzadko zaznaczy, że pytanie było niejasne.

Jeśli wyniki S3 będą powtarzalne, H2 potwierdzi się przez ukryte wartości domyślne, a nie przez losowość. Wniosek będzie wtedy taki, że problemem nie jest losowość modelu, tylko założenia, których pytający nie widzi. Jeśli model będzie regularnie zaznaczał niejasność w polu `uwagi`, H2 zostanie obalona.

**Co dodatkowo możemy sprawdzić:**
- czy przy znanych obiektach (PKiN, Stadion Narodowy) model wpisuje współrzędne z pamięci zamiast pobierać je z bazy i czy przy mało znanych obiektach radzi sobie gorzej,
- które kategorie zapytań są najtrudniejsze,
- ile kosztuje (w tokenach) każdy poziom kontekstu w stosunku do zysku jakości.

## Brak trudności, ryzyka (czego nie wiemy, czego brakuje, co może pójść nie tak)

- **Błędy w zapytaniach wzorcowych.** Jeśli wzorzec jest zły, zła będzie cała ocena. Każdy wzorzec musi sprawdzić druga osoba i trzeba obejrzeć jego wynik, np. na mapie w QGIS albo w DataGrip.
- **Sporne przypadki przy porównaniu wyników.** Zaokrąglenia, dodatkowe kolumny i remisy w pytaniach „top k” mogą dawać sporne oceny. Zasady porównania ustalamy przed badaniem, a sporne przypadki opisujemy w artykule.
- **Mała próba.** 20 pytań × 3 powtórzenia nie da mocnych testów statystycznych. Wyniki pokażemy opisowo, z przedziałami ufności, i nie będziemy przesadzać z wnioskami.
- **Jakość danych OSM.** Brakuje nazw, obiekty są zdublowane w kilku tabelach, a nazwy różnią się od potocznych. Część tego to celowo badane pułapki, ale niektóre pytania mogą nie mieć jednoznacznej odpowiedzi i trzeba będzie je wymienić.
- **Model może znać dane Geofabrik.** Nazwy tabel Geofabrik są popularne, więc nawet na K0 model może trafiać. Osłabiłoby to różnice między poziomami, ale też byłoby ciekawym wynikiem.
- **Losowość i zmiany modelu.** Odpowiedzi różnią się między wywołaniami, a model w API może zostać zaktualizowany. Zapisujemy dokładną wersję modelu i ustawienia, a wszystkie odpowiedzi trzymamy w plikach.
- **Wpływ formatu odpowiedzi na eksperyment 2.** Pole `uwagi` w odpowiedzi może zachęcać model do zgłaszania niejasności częściej, niż robiłby to sam. Instrukcja musi być neutralna, a to ograniczenie trzeba opisać.
- **Brak jednej poprawnej odpowiedzi dla S2 i S3.** Dla tych pytań nie oceniamy poprawności, tylko powtarzalność i przyjęte wartości. Opcjonalnie możemy porównać wynik z ustaloną przez nas „rozsądną” interpretacją, np. 10 minut spacerem to ok. 800 m.
- **Pytania o czas dojazdu.** Bez danych o sieci dróg (np. pgRouting) model może tylko przeliczyć czas na odległość w linii prostej. To ograniczenie samego zadania, a nie modelu, i trzeba to uwzględnić przy interpretacji.
- **Czas i budżet.** Ok. 400 wywołań API to kilka dolarów, więc koszt nie jest problemem. Największe ryzyko to czas potrzebny na zapytania wzorcowe i skrypt oceniający.

## Zadania do wykonania i ich alokacja (jakie działania są wymagane)

- poprawić dane do eksperymentów i ostateczne ustalić hipotezę

- przygotowanie prezentacji zgodnie z wymaganiami

- dalszy ciąg przeglądu literatury jak będziemy już dokładnie wiedzili co mamy robić

- interfejs do konsolowego zadania pytań

- sprawdzić korzystanie z Claude API - konfiguracja, jak można zwiększać kontekst, jak można zmuszać do ustrukturyzowanej odpowiedzi, jak można zmieniać parametry modelu

- przedstawić wnioski na spotkaniu z opiekunem

- eksperymenty i draft artykułu
