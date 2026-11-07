## Cel badania (co chcemy się dowiedzieć i po co)

Chcemy sprawdzić, jak różne sposoby zwiększania kontekstu wpływają na jakość zapytań przestrzennych SQL generowanych przez modele językowe oraz jak modele te radzą sobie z niejasnymi pytaniami. Dzięki temu dowiemy się, jakie informacje warto przekazywać modelowi i na ile można polegać na jego interpretacji pytań o dane przestrzenne.

## Hipoteza badawcza (hipoteza musi być testowalna)

**H1:** Opis zawartości danych poprawia trafność zapytań przestrzennych SQL bardziej niż opis struktury bazy danych oraz wskazówki i przykłady zapytań.

#### Wyjaśnienie H1
- **Opis struktury bazy danych** to nazwy tabel i kolumn wraz z typami, w tym typem geometrii i układem współrzędnych.
- **Opis zawartości danych** to znaczenie tabel i kolumn, dopuszczalne wartości typu obiektu (np. `'pharmacy'`) oraz fakty o danych, np. że ten sam rodzaj obiektu bywa zapisany raz jako punkt, a raz jako poligon, albo że brak nazwy to pusty napis. Ten opis mówi, **co jest w bazie**, ale nie mówi, jak pisać zapytania.
- **Wskazówki i przykłady zapytań** mówią, **jak pisać zapytania**:
  - wskazówki przestrzenne, np. „aby liczyć w metrach, rzutuj na `geography`”, „połącz tabele punktów i poligonów”, „pomijaj obiekty bez nazwy warunkiem `name <> ''`”,
  - 5 przykładów pytanie → SQL, które nie dotyczą obiektów z pytań testowych.
- **Trafność** to odsetek zapytań, które zwracają taki sam wynik jak zapytanie wzorcowe.
- **Jak sprawdzamy:** porównujemy cztery kolejne poziomy kontekstu, z których każdy zawiera poprzedni:
  - K0: same nazwy tabel i kolumn,
  - K1: K0 + opis struktury bazy danych,
  - K2: K1 + opis zawartości danych,
  - K3: K2 + wskazówki i przykłady zapytań.

  Każdy rodzaj informacji mierzymy przyrostem trafności po dodaniu go do poprzedniego poziomu:
  - opis struktury: przyrost K0 → K1,
  - opis zawartości danych: przyrost K1 → K2,
  - wskazówki i przykłady: przyrost K2 → K3.

  Szczegóły poziomów: [poziomy-kontekstu.md](eksperyment/draft/poziomy-kontekstu.md).
- **Potwierdzenie:** przyrost K1 → K2 jest większy od obu pozostałych.
- **Obalenie:** największy jest przyrost K0 → K1 albo K2 → K3.
- **Literatura:** DAIL-SQL (praca 9) i przegląd z pracy 12 pokazują, że sposób opisu bazy w prompcie wpływa na wynik, ale nie rozdzielają wpływu opisu struktury, opisu zawartości danych oraz przykładów.

**H2:** Model interpretuje niejasne określenia przestrzenne zależnie od kontekstu pytania. Zmiana opisu sytuacji pytającego, miejsca albo rodzaju szukanego obiektu zmienia wartość, którą model przyjmuje dla tego samego określenia.

#### Wyjaśnienie H2
- **Niejasne określenie przestrzenne** to sformułowanie, które nie podaje odległości wprost:
  - bez żadnej miary, np. „w pobliżu”, „niedaleko”,
  - z miarą, którą trzeba przeliczyć, np. „w 15 minut”.
- **Przyjęta wartość** to wartość, którą model musi sam wybrać, najczęściej promień w metrach. Odczytujemy ją z wygenerowanego SQL.
- **Kontekst pytania** to wszystko w pytaniu poza samym niejasnym określeniem:
  - **opis sytuacji pytającego:** czy idzie pieszo, czy jedzie samochodem,
  - **miejsce:** gęsto zabudowane centrum miasta albo okolica, w której obiektów jest mało,
  - **rodzaj i skala szukanego obiektu:** apteka „w pobliżu” to zwykle kilkaset metrów, a park czy szpital może oznaczać więcej.
- **Jak sprawdzamy:** zadajemy to samo niejasne określenie („w pobliżu”) w różnych kontekstach, przy stałej formie zdania i stałym poziomie kontekstu bazy (K2). Każde pytanie zadajemy 3 razy i porównujemy przyjęte wartości między kontekstami. Szczegóły: [plan-eksperymentow.md](eksperyment/draft/plan-eksperymentow.md), pełna lista pytań: [selected/H2](eksperyment/selected/H2/pytania.md).
- **Potwierdzenie:** przyjęty promień zmienia się wraz z kontekstem zgodnie ze zdrowym rozsądkiem, czyli rośnie przy szybszym środku transportu, w okolicy o mniejszej gęstości obiektów albo przy obiekcie większej skali. Sprawdzamy wszystkie trzy sposoby i osobno podajemy, który z nich zmienia przyjętą wartość, a który nie.
- **Obalenie:** model przyjmuje te same wartości niezależnie od kontekstu, np. zawsze 500 m dla „w pobliżu”. Wniosek jest wtedy taki, że model stosuje mechaniczne wartości domyślne.
- **Literatura:** AmbiQT (praca 10) pokazuje, że modele trzymają się jednej interpretacji pytania, ale nie mówi, czy ta interpretacja zależy od kontekstu.

## Metoda (jakie narzędzia badawcze, jakie eskperymenty, warunki eksperymentów, jakie narzędzia informatyczne, punkt odniesienia)

- **Eksperyment 1 (H1):** 20 pytań testowych (po 4 z każdej kategorii zapytań, w tym kilka o mało znane obiekty) zadajemy modelowi na czterech poziomach kontekstu (K0–K3), po 3 powtórzenia. Używamy naturalnej wersji pytań (bez nazw tabel i kolumn), bo wersja precyzyjna sama podaje modelowi część kontekstu. Dla każdego poziomu liczymy trafność, czyli odsetek poprawnych zapytań. Zapytanie jest poprawne, gdy zwraca taki sam wynik jak zapytanie wzorcowe, według zasad porównania opisanych niżej. Każdą próbę oceniamy osobno, a trafność liczymy ze wszystkich prób na danym poziomie. Następnie porównujemy trzy przyrosty trafności: K0 → K1, K1 → K2 i K2 → K3.
- **Eksperyment 2 (H2):** zadajemy pytania z tym samym niejasnym określeniem i zmieniamy kontekst wokół niego, a z SQL odczytujemy wartość przyjętą przez model. Eksperyment ma dwie części:
  - **2a: „w pobliżu”.** Zmieniamy opis sytuacji pytającego (brak informacji, pieszo, samochodem) × miejsce (gęste centrum, okolica peryferyjna) × rodzaj obiektu (apteki, szpitale). Daje to 12 pytań, a z jednym pytaniem kontrolnym („niedaleko” zamiast „w pobliżu”) 13.
  - **2b: czas dojazdu.** „W 15 minut” × cztery środki transportu (brak informacji, pieszo, rowerem, samochodem) oraz pytanie w większej skali, o godzinę jazdy z Warszawy. Daje to 5 pytań. Sprawdzamy, jakie prędkości przyjmuje model i czy w ogóle przelicza czas na odległość.
  - **2c: „w centrum”.** Niejasny obszar, a nie promień. Dwa rodzaje obiektów × dwa miasta (Warszawa, Płock) oraz pytanie bez nazwy miasta. Daje to 5 pytań. Sprawdzamy, czym model zastępuje „centrum”.
  - **2d: „duże” i „małe”.** Niejasna cecha obiektu, niezwiązana z odległością. Dwie cechy × trzy miasta różnej wielkości (Warszawa, Radom, Płock). Daje to 6 pytań. Sprawdzamy, jak model rozumie wielkość i czy progi dla obu cech są spójne.

  Każde pytanie zadajemy 3 razy przy stałym kontekście **K2**. K2 zawiera pełny opis danych, ale nie ma wskazówek ani przykładów zapytań. Model odpowiada w formacie JSON: `{"sql": "...", "uwagi": "..."}`, gdzie pole `uwagi` może pozostać puste. Z SQL odczytujemy przyjęty promień oraz rodzaj interpretacji: promień, k najbliższych obiektów, obszar administracyjny albo inny. Z pola `uwagi` sprawdzamy, czy model ujawnił przyjęte założenie. Eksperyment nie wymaga zapytań wzorcowych, bo nie oceniamy poprawności, tylko przyjęte wartości. Pełna lista pytań: [selected/H2](eksperyment/selected/H2/pytania.md).
- **Zasady porównania wyników z wzorcem (eksperyment 1):**
  - Dla każdego pytania ustalamy kolumny kluczowe, np. `name` albo liczbę. Pozostałe kolumny w wyniku modelu ignorujemy.
  - Wiersze porównujemy jako zbiory, bez względu na kolejność. Kolejność ma znaczenie tylko w pytaniach o „najbliższe” i „top k”.
  - Liczby zmiennoprzecinkowe (odległości, powierzchnie, długości) uznajemy za równe przy różnicy do 1%, żeby różne zaokrąglenia nie były traktowane jako błąd.
  - Napisy porównujemy dokładnie.
  - Zapytanie, które się nie wykonuje, jest niepoprawne.
- **Warunki eksperymentów:** jedno wywołanie modelu bez historii i bez poprawiania zapytań, ten sam model i te same ustawienia we wszystkich próbach. W artykule podajemy dokładny identyfikator modelu (np. `claude-sonnet-5`) oraz wartość parametru `effort`, który ustawiamy jawnie. Temperatury nie ustawiamy, bo w obecnym API modeli Claude wartość inna niż domyślna jest odrzucana. Pytania, treść poziomów i kryteria oceny ustalamy przed badaniem.

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
- Eksperyment 2: kontekst wokół niejasnego określenia, czyli opis sytuacji pytającego, miejsce, rodzaj szukanego obiektu i miasto.

**Mierzymy (zmienne zależne):**
- Eksperyment 1:
  - trafność, czyli odsetek poprawnych zapytań, na każdym poziomie, łącznie i osobno dla każdej kategorii zapytań,
  - przyrosty trafności między kolejnymi poziomami: K0 → K1, K1 → K2, K2 → K3,
  - odsetek zapytań, które w ogóle się wykonują,
  - rodzaje błędów: zła tabela, zła wartość typu obiektu, liczenie w stopniach zamiast w metrach, współrzędne wpisane z pamięci zamiast pobrane z bazy, zła funkcja przestrzenna, zła agregacja,
  - liczba tokenów w prompcie, czyli koszt danego poziomu kontekstu.
- Eksperyment 2:
  - przyjęta wartość: promień w metrach w częściach 2a i 2b, użyty obszar w części 2c, próg wielkości w części 2d,
  - rodzaj interpretacji: promień, k najbliższych, obszar administracyjny albo inny,
  - w części 2b przyjęta prędkość, wyliczona z promienia i czasu,
  - rozrzut przyjętych wartości między 3 powtórzeniami,
  - odsetek odpowiedzi, w których model ujawnił przyjęte założenie.

**Nie zmieniamy (zmienne kontrolowane):** model i jego ustawienia, instrukcja zadania, baza danych, w eksperymencie 1 treść pytań, a w eksperymencie 2 forma zdania i niejasne określenie.

## Oczekiwane wyniki (jakie są możliwe wyniki i jak zaadresują hipoteze, co dodatkowego można sprawdzić/zrobić)

**H1.** Spodziewamy się, że najsłabiej wypadnie K0, a największy skok nastąpi między K1 a K2, bo to tam model dowiaduje się o pułapkach w danych. Najczęstsze z nich to szpitale i szkoły zapisane w dwóch tabelach, puste nazwy oraz to, że Dworzec Centralny nazywa się w bazie „Warszawa Centralna”.

Między K2 a K3 spodziewamy się mniejszego, ale zauważalnego przyrostu. Wskazówki i przykłady pomogą głównie tam, gdzie model zna fakt o danych, ale nie umie go przełożyć na SQL. Typowe przypadki:
- wie, że obiekty są w dwóch tabelach, ale ich nie łączy,
- wie, że dane są w stopniach, ale nie rzutuje na `geography`.

Możliwe wyniki:
- **Największy przyrost K1 → K2:** H1 potwierdzona. Modelowi najbardziej brakuje wiedzy o danych.
- **Największy przyrost K0 → K1:** H1 obalona. Dla współczesnych modeli ważniejsza jest sama struktura bazy.
- **Największy przyrost K2 → K3:** H1 obalona. Fakty o danych nie wystarczą, a model potrzebuje gotowych wzorców zapytań. To ważny wniosek praktyczny: opis danych trzeba uzupełniać przykładami.
- **Podobne przyrosty na wszystkich poziomach:** żaden rodzaj informacji nie dominuje, a liczy się łączna ilość kontekstu.

Każdy z tych wyników da się opisać w artykule. Przy K3 sprawdzamy też, które błędy z K2 znikają po dodaniu wskazówek i przykładów, a które zostają.

**H2.** Spodziewamy się, że:
- **Opis sytuacji zmieni promień najmocniej.** Dla „samochodem” promień będzie kilka razy większy niż dla „pieszo”, bo ta informacja jest podana wprost.
- **Miejsce zmieni promień słabo albo wcale.** Model musiałby sam ocenić, że w okolicy peryferyjnej obiektów jest mniej, a w pytaniu tej informacji nie ma.
- **Rodzaj obiektu zmieni promień słabiej niż sytuacja.** Apteki, parki i szpitale mogą dostać tę samą wartość, np. 1 km.
- **Bez żadnego kontekstu model przyjmie okrągłą wartość domyślną,** np. 500 m albo 1 km, i rzadko ją ujawni.
- **W części 2b przyjmie typowe prędkości:** ok. 5 km/h pieszo, ok. 15 km/h rowerem, 30–50 km/h samochodem w mieście.

Możliwe wyniki:
- **Promień zmienia się przy wszystkich trzech czynnikach:** H2 potwierdzona. Model interpretuje kontekst także tam, gdzie musi sam wnioskować.
- **Promień zmienia się tylko przy opisie sytuacji:** H2 potwierdzona, ale model reaguje jedynie na informację podaną wprost i nie wnioskuje sam z miejsca ani z rodzaju obiektu.
- **Promień jest stały:** H2 obalona. Model stosuje mechaniczne wartości domyślne.

**Rozszerzenie, jeśli starczy czasu:** krótka ankieta wśród ludzi z tymi samymi pytaniami, np. „co dla Ciebie znaczy apteka w pobliżu dworca, gdy idziesz pieszo?”. Pozwoli sprawdzić, czy wartości przyjmowane przez model są zbliżone do oczekiwań pytających.

**Co dodatkowo możemy sprawdzić:**
- czy model reaguje tak samo na wskazówkę podaną wprost („Idę pieszo.”) i na sam opis sytuacji, z którego trzeba ją wywnioskować („Mam 20 minut do odjazdu pociągu.”),
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
- **Odczytanie przyjętej wartości z SQL.** Model nie zawsze użyje promienia. Może zwrócić k najbliższych obiektów, użyć granicy dzielnicy albo zapisać promień jako wyrażenie, np. `15 * 5000 / 60`. Promień odczytujemy skryptem, a przypadki nietypowe klasyfikujemy ręcznie. Rodzaj interpretacji jest osobną zmienną, a nie błędem.
- **Brak jednej poprawnej odpowiedzi w eksperymencie 2.** Nie oceniamy poprawności, tylko przyjęte wartości i ich zależność od kontekstu. Nie mówimy, która wartość jest „dobra”. Do tego potrzebna byłaby ankieta wśród ludzi.
- **Pytania o czas dojazdu.** Bez danych o sieci dróg (np. pgRouting) model może tylko przeliczyć czas na odległość w linii prostej. To ograniczenie samego zadania, a nie modelu, i trzeba to uwzględnić przy interpretacji.
- **Czas i budżet.** Ok. 327 wywołań API (240 w eksperymencie 1 i 87 w eksperymencie 2) to kilka dolarów, więc koszt nie jest problemem. Największe ryzyko to czas potrzebny na zapytania wzorcowe i skrypt oceniający.

## Zadania do wykonania i ich alokacja (jakie działania są wymagane)

- poprawić dane do eksperymentów i ostateczne ustalić hipotezę

- przygotowanie prezentacji zgodnie z wymaganiami

- dalszy ciąg przeglądu literatury jak będziemy już dokładnie wiedzili co mamy robić

- interfejs do konsolowego zadania pytań

- sprawdzić korzystanie z Claude API - konfiguracja, jak można zwiększać kontekst, jak można zmuszać do ustrukturyzowanej odpowiedzi, jak można zmieniać parametry modelu

- przedstawić wnioski na spotkaniu z opiekunem

- eksperymenty i draft artykułu
