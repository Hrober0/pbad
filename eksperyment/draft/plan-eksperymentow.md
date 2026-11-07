# Plan eksperymentów: przykładowe pytania

Kilka przykładowych pytań do każdego eksperymentu, a dla każdego z nich: co chcemy sprawdzić i czego się spodziewamy. Hipotezy i metoda: [informacje-ogolne.md](../informacje-ogolne.md). Poziomy kontekstu: [poziomy-kontekstu.md](poziomy-kontekstu.md).

| | Eksperyment 1 | Eksperyment 2 |
|---|---|---|
| Hipoteza | H1 | H2 |
| Co zmieniamy | poziom kontekstu K0–K3 | opis sytuacji pytającego, miejsce, rodzaj obiektu, miasto |
| Co jest stałe | wersja pytania (naturalna) | kontekst K2, forma zdania i niejasne określenie w obrębie części |
| Pytania | 20 z [pytania-testowe.md](pytania-testowe.md), wybrane w [selected/H1](../selected/H1/pytania.md) | 29, wypisane w [selected/H2](../selected/H2/pytania.md) |
| Powtórzenia | 3 | 3 |
| Liczba wywołań | 20 × 4 × 3 = 240 | 29 × 3 = 87 |
| Odpowiedź modelu | samo zapytanie SQL | JSON `{"sql": "...", "uwagi": "..."}` |
| Co mierzymy | trafność na każdym poziomie i jej przyrosty, rodzaje błędów | przyjęty promień, rodzaj interpretacji, ujawnienie założenia |
| Potwierdzenie hipotezy | przyrost K1 → K2 większy niż K0 → K1 i K2 → K3 | promień zmienia się z opisem sytuacji, miejscem albo rodzajem obiektu |
| Zapytania wzorcowe | potrzebne | niepotrzebne |

---

## Eksperyment 1: wpływ kontekstu (H1)

Sprawdzamy, który rodzaj informacji o bazie najbardziej poprawia trafność. Porównujemy trzy przyrosty:
- opis struktury bazy danych: przyrost K0 → K1,
- opis zawartości danych: przyrost K1 → K2,
- wskazówki i przykłady zapytań: przyrost K2 → K3.

Według H1 największy ma być przyrost K1 → K2.

Pytania są w wersji naturalnej (P2) z [pytania-testowe.md](pytania-testowe.md). Każde ma jedno zapytanie wzorcowe. W przykładach poniżej przy każdym poziomie opisujemy, który rodzaj informacji powinien usunąć dany błąd.

### Co dokładnie dostaje model

Każda próba to jedno wywołanie API bez historii rozmowy. Model dostaje jedną wiadomość złożoną z trzech części:

1. **Instrukcja zadania.** Jest taka sama we wszystkich próbach: rola, format odpowiedzi i konwencje oceny (przecięcie z obszarem, liczenie raz, pomijanie obiektów bez nazwy, jednostki). Pełna treść: [poziomy-kontekstu.md](poziomy-kontekstu.md#część-wspólna-dla-wszystkich-poziomów).
2. **Opis bazy danych na jednym z poziomów K0–K3.** To jedyna część, która zmienia się między wariantami eksperymentu.
3. **Treść pytania.** Jest to dokładnie tekst z cytatu przy każdym przykładzie poniżej, np. „Wymień nazwy kawiarni w promieniu 300 metrów od Dworca Centralnego.”

Model nie dostaje niczego więcej. Nie widzi punktów „Co sprawdzamy” i „Czego się spodziewamy”, zapytania wzorcowego, nazw obiektów w bazie (chyba że są w opisie bazy na K2–K3) ani błędów z poprzednich prób.

Przykład pełnego promptu dla Z02 na poziomie K0 (opis bazy skrócony):

```text
Jesteś asystentem, który tłumaczy pytania w języku polskim na zapytania SQL
dla bazy PostgreSQL 18 z rozszerzeniem PostGIS 3.6.

Zwróć dokładnie jedno zapytanie SELECT w bloku ```sql ... ```, bez dodatkowych wyjaśnień.
Nie modyfikuj danych.

Obowiązujące konwencje:
1. Obiekt należy do obszaru, jeśli się z nim przecina. W pytaniach o długość lub
   powierzchnię „w granicach” obszaru licz tylko część leżącą wewnątrz obszaru.
2. Każdy obiekt licz tylko raz.
3. Pomijaj obiekty bez nazwy, zarówno w wynikach, jak i przy liczeniu.
4. Odległości podawaj w metrach, długości w metrach lub kilometrach, powierzchnie
   w metrach kwadratowych lub hektarach, zgodnie z pytaniem.

Opis bazy danych:
gis_osm_pois_free(fid, osm_id, code, fclass, name, geom)
gis_osm_pois_a_free(fid, osm_id, code, fclass, name, geom)
gis_osm_transport_free(fid, osm_id, code, fclass, name, geom)
... (pozostałe tabele gis_osm_*)

Pytanie: Wymień nazwy kawiarni w promieniu 300 metrów od Dworca Centralnego.
```

Na poziomach K1–K3 zmienia się tylko część „Opis bazy danych”. Model odpowiada blokiem ```` ```sql ```` z jednym zapytaniem. Skrypt wycina to zapytanie, wykonuje je na bazie i porównuje wynik z wynikiem zapytania wzorcowego.

### Z02: kawiarnie przy Dworcu Centralnym

> Wymień nazwy kawiarni w promieniu 300 metrów od Dworca Centralnego.

- **Co sprawdzamy:**
  - czy model znajdzie dworzec, który w bazie nazywa się „Warszawa Centralna”, a nie „Dworzec Centralny”,
  - czy liczy odległość w metrach (`geography`), a nie w stopniach,
  - czy uwzględnia kawiarnie zapisane jako poligony.
- **Czego się spodziewamy:**
  - **K0–K1:** model szuka `name = 'Dworzec Centralny'` i dostaje pusty wynik albo wpisuje współrzędne dworca z pamięci.
  - **K2:** zna prawdziwą nazwę z opisu danych, więc większość prób powinna być poprawna.
  - **K3:** poprawne prawie zawsze.

### N01: najbliższy szpital od PKiN

> Jaki szpital jest najbliżej Pałacu Kultury i Nauki?

- **Co sprawdzamy:** czy model przeszuka obie tabele. W Warszawie jest 7 szpitali zapisanych jako punkty i 37 jako poligony. Szukanie tylko w punktach daje wynik, który wygląda sensownie, ale jest zły.
- **Czego się spodziewamy:**
  - **K0–K1:** model przeszuka tylko `gis_osm_pois_free` i poda zły szpital. Zapytanie się wykona, więc nie widać, że jest błędne.
  - **K2:** wie o podziale na punkty i poligony, ale może nie połączyć tabel.
  - **K3:** łączy tabele, bo jest to pokazane w przykładach.

  To dobre pytanie, żeby w prezentacji pokazać różnicę między „zapytanie działa” a „zapytanie jest poprawne”.

### Z01 i Z05: znany i mało znany obiekt

> Z01: Ile aptek jest w promieniu 500 metrów od Pałacu Kultury i Nauki?
>
> Z05: Ile aptek jest w promieniu kilometra od Skweru Jolanty Brzeskiej?

- **Co sprawdzamy:** czy przy znanym obiekcie (PKiN) model wpisuje współrzędne z pamięci, np. `ST_MakePoint(21.006, 52.231)`, zamiast pobrać geometrię z bazy. Przy mało znanym skwerze na Mokotowie takiego skrótu nie ma.
- **Czego się spodziewamy:**
  - **Z01 na K0–K1:** część prób z wpisanymi współrzędnymi. Wynik może być „prawie dobry” i różnić się o jedną czy dwie apteki.
  - **Z05:** model musi wyszukać obiekt w bazie po nazwie. Na K0–K1 może nie wiedzieć, w której tabeli szukać, więc spodziewamy się więcej błędów niż przy Z01.
  - Porównanie tej pary pokaże, czy „wiedza z pamięci” modelu pomaga, czy szkodzi.

### M02: długość ulicy Marszałkowskiej

> Ile kilometrów ma ulica Marszałkowska w Warszawie?

- **Co sprawdzamy:**
  - czy model zawęzi wynik do Warszawy (w województwie jest kilka ulic Marszałkowskich, a bez zawężenia wychodzi 9,9 km),
  - czy policzy długość w metrach,
  - czy zsumuje wszystkie odcinki ulicy.
- **Czego się spodziewamy:**
  - **K0–K1:** suma bez zawężenia, czyli ok. 9,9 km, albo wynik w stopniach.
  - **K2:** model wie, że dane obejmują całe województwo, ale może zapomnieć o zawężeniu.
  - **K3:** poprawny wynik, bo wskazówka mówi wprost o zawężaniu do Warszawy.

  Możliwy też błąd odwrotny: model może odpowiedzieć z pamięci, np. `SELECT 3.5`, zamiast pytać bazę.

---

## Eksperyment 2: interpretacja niejasnych określeń (H2)

Sprawdzamy, czy wartość, którą model przyjmuje dla niejasnego określenia przestrzennego, zależy od kontekstu pytania. W każdej części niejasne określenie i forma zdania są stałe, a zmieniamy kontekst wokół nich. Dzięki temu różnica w przyjętej wartości wynika tylko ze zmiany kontekstu.

Eksperyment ma cztery części, po jednej na rodzaj niejasności:

| Część | Niejasne określenie | Co zmieniamy | Pytania |
|---|---|---|---|
| 2a | „w pobliżu” | opis sytuacji, miejsce, rodzaj obiektu | 13 |
| 2b | czas dojazdu | środek transportu, skala | 5 |
| 2c | „w centrum” | miasto, rodzaj obiektu | 5 |
| 2d | „duże” i „małe” | cecha, miasto | 6 |

Pełna lista pytań: [selected/H2/pytania.md](../selected/H2/pytania.md).

### Co dokładnie dostaje model

Tak jak w eksperymencie 1, każda próba to jedno wywołanie bez historii. Wiadomość ma trzy części:

1. **Instrukcja zadania z eksperymentu 1** ze zmienionym formatem odpowiedzi: zamiast samego bloku SQL model zwraca JSON `{"sql": "...", "uwagi": "..."}`, gdzie `uwagi` mogą pozostać puste. Instrukcja nie wspomina o niejasności ani o założeniach, żeby nie podpowiadać modelowi, że ma je zgłaszać.
2. **Opis bazy na poziomie K2,** czyli pełny opis danych bez wskazówek i przykładów zapytań. W prompcie nie ma więc żadnej gotowej wartości promienia. Jeśli model poda promień w stopniach, przeliczamy go na metry i oznaczamy jako błąd techniczny.
3. **Treść pytania z tabel poniżej.** Opis sytuacji pytającego jest częścią pytania, np. „Idę pieszo. Wymień apteki w pobliżu Dworca Centralnego.”

Każde pytanie zadajemy 3 razy. Z każdej odpowiedzi odczytujemy:
- **przyjęty promień w metrach,** np. trzeci argument `ST_DWithin`,
- **rodzaj interpretacji:** promień, k najbliższych obiektów (`ORDER BY ... LIMIT`), obszar administracyjny albo inny,
- **czy model ujawnił przyjęte założenie** w polu `uwagi`.

Wynikiem jest tabela: mediana promienia i jego rozrzut dla każdej kombinacji kontekstu. Poprawności nie oceniamy, więc zapytania wzorcowe nie są potrzebne.

### Część 2a: określenie bez miary

Pytanie ma zawsze tę samą postać: „[opis sytuacji] Wymień [obiekty] w pobliżu [miejsce].” Określenie „w pobliżu” i forma zdania się nie zmieniają. Zmieniamy trzy czynniki:

| Czynnik | Wartości |
|---|---|
| Opis sytuacji pytającego | brak informacji; „Idę pieszo.”; „Jadę samochodem.” |
| Miejsce | gęste centrum (Dworzec Centralny); okolica peryferyjna (stacja do wybrania, np. Warszawa Płudy) |
| Rodzaj obiektu (rosnąca skala) | apteki, szpitale |

Daje to 3 × 2 × 2 = 12 pytań, a z pytaniem kontrolnym opisanym niżej 13 pytań i 39 wywołań. Parki pomijamy, bo są poligonami i są zdublowane w dwóch tabelach, co dodałoby szum niezwiązany z interpretacją określenia. Przykładowe pytania:

| Opis sytuacji | Pytanie |
|---|---|
| brak informacji | Wymień apteki w pobliżu Dworca Centralnego. |
| pieszo | Idę pieszo. Wymień apteki w pobliżu Dworca Centralnego. |
| samochodem | Jadę samochodem. Wymień apteki w pobliżu Dworca Centralnego. |
| brak informacji | Wymień szpitale w pobliżu stacji Warszawa Płudy. |
| pieszo | Idę pieszo. Wymień szpitale w pobliżu stacji Warszawa Płudy. |
| samochodem | Jadę samochodem. Wymień apteki w pobliżu stacji Warszawa Płudy. |

Dwa czynniki różnią się tym, ile pracy wymagają od modelu. Opis sytuacji podaje informację wprost, więc model ma ją tylko odczytać. Miejsce i rodzaj obiektu wymagają już wnioskowania, bo w pytaniu nie ma nic o gęstości okolicy ani o typowej skali obiektu.

- **Co sprawdzamy:**
  - czy promień rośnie przy zmianie z „pieszo” na „samochodem”,
  - czy model zwiększa promień w okolicy, w której obiektów jest mniej,
  - czy promień rośnie razem ze skalą obiektu (apteka → szpital),
  - jaką wartość domyślną model przyjmuje bez żadnego kontekstu.
- **Czego się spodziewamy:**
  - **Opis sytuacji:** wyraźny efekt. „Samochodem” daje promień kilka razy większy niż „pieszo”, bo ta informacja jest podana wprost.
  - **Miejsce:** słaby efekt albo jego brak. Model musiałby sam ocenić gęstość obiektów w okolicy.
  - **Rodzaj obiektu:** słabszy efekt niż opis sytuacji. Apteki i szpitale mogą dostać tę samą wartość, np. 1 km.
  - **Bez żadnego kontekstu:** okrągła wartość, 500 m albo 1 km, najczęściej bez wzmianki w polu `uwagi`.
  - **Okolica peryferyjna:** możliwa zmiana interpretacji z promienia na „k najbliższych”, jeśli w okolicy nie ma żadnego obiektu danego rodzaju. To też jest ciekawy wynik, ale trzeba go odróżnić od zmiany promienia.
- **Jak rozstrzygamy H2:**
  - promień zmienia się przy którymkolwiek z trzech czynników, czyli H2 potwierdzona: zmianą kontekstu da się wpłynąć na interpretację,
  - promień nie zmienia się przy żadnym z nich, czyli H2 obalona: model stosuje wartość domyślną niezależną od kontekstu.

  Osobno opisujemy, które czynniki zadziałały i jak mocno. Jeśli zadziałał tylko opis sytuacji, znaczy to, że model odczytuje informację podaną wprost, ale nie wnioskuje z miejsca ani z rodzaju obiektu. Jest to wynik do opisania w artykule, a nie osobne rozstrzygnięcie hipotezy.
- **Rozszerzenie, jeśli starczy czasu:** dodać czwarty opis sytuacji, w którym sposób poruszania się trzeba wywnioskować, np. „Mam 20 minut do odjazdu pociągu.”. Pokazałoby to, czy model reaguje tylko na słowa kluczowe.
- **Kontrola na boku:** dla jednej kombinacji (apteki, centrum, brak kontekstu) zadajemy to samo pytanie z określeniem „niedaleko” zamiast „w pobliżu”. Sprawdza to, czy wynik nie zależy od jednego konkretnego słowa. Nie jest to czynnik eksperymentu, ale jedno dodatkowe pytanie wliczone do liczb.

### Część 2b: czas dojazdu

Zmienia się środek transportu, a ostatnie pytanie dodatkowo skalę.

| Sytuacja | Pytanie |
|---|---|
| brak informacji | Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |
| pieszo | Idę pieszo. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |
| rowerem | Jadę rowerem. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |
| samochodem | Jadę samochodem. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |
| poza miasto | Wymień jeziora, do których dojadę z Warszawy w godzinę. |

Daje to 5 pytań i 15 wywołań. Ostatnie pytanie jest w innej skali: promień idzie w dziesiątki kilometrów, a punktem odniesienia jest całe miasto, a nie jeden obiekt. O ten przypadek pytał opiekun na spotkaniu 30.10. Dane obejmują tylko mazowieckie, więc wynik może być ucięty granicą województwa.

- **Co sprawdzamy:**
  - jaką prędkość przyjmuje model dla każdego środka transportu (prędkość = promień / 15 minut),
  - jaki środek transportu zakłada, gdy pytający go nie podał,
  - czy uwzględnia, że droga jest dłuższa niż linia prosta, np. przez współczynnik krętości dróg,
  - czy zaznacza, że bez sieci dróg nie da się dokładnie policzyć czasu dojazdu.
- **Czego się spodziewamy:**
  - promień ok. 1,2 km pieszo (5 km/h), ok. 4 km rowerem (15 km/h) i 7,5–12,5 km samochodem (30–50 km/h w mieście),
  - bez informacji o środku transportu najpewniej założy chodzenie pieszo,
  - ograniczenie wynikające z braku sieci dróg wspomni rzadko.

Części 2a i 2b dotyczą niejasności związanej z odległością. Dwie kolejne sprawdzają inne rodzaje niejasności.

### Część 2c: niejasny obszar („w centrum”)

Tu model nie wybiera promienia, tylko obszar, więc musi sięgnąć po jakąś geometrię. Czynnikiem kontekstu jest miasto.

| Miasto | Pytanie |
|---|---|
| Warszawa | Wymień kawiarnie w centrum Warszawy. |
| Płock | Wymień kawiarnie w centrum Płocka. |
| Warszawa | Wymień apteki w centrum Warszawy. |
| Płock | Wymień apteki w centrum Płocka. |
| brak | Wymień kawiarnie w centrum. |

Daje to 5 pytań i 15 wywołań. W ostatnim pytaniu nie ma nazwy miasta, więc sprawdzamy też, czy model zakłada Warszawę.

- **Co sprawdzamy:** jak model definiuje centrum, czyli czy używa granicy dzielnicy, promienia wokół jakiegoś obiektu, czy prostokąta ze współrzędnymi, oraz jaką powierzchnię to daje. Osobno: czy „centrum” skaluje się do wielkości miasta.
- **Czego się spodziewamy:** w Warszawie najpewniej granica Śródmieścia albo promień wokół PKiN, a w Płocku brak oczywistej geometrii, więc możliwy promień wokół środka miasta.

### Część 2d: niejasna cecha („duże” i „małe”)

Niejasność, która w ogóle nie dotyczy odległości. Model musi sam zdecydować, co znaczy „duży” i „mały”.

| Cecha | Miasto | Pytanie |
|---|---|---|
| duże | Warszawa | Wymień duże parki w Warszawie. |
| duże | Radom | Wymień duże parki w Radomiu. |
| duże | Płock | Wymień duże parki w Płocku. |
| małe | Warszawa | Wymień małe parki w Warszawie. |
| małe | Radom | Wymień małe parki w Radomiu. |
| małe | Płock | Wymień małe parki w Płocku. |

Daje to 6 pytań i 18 wywołań. Trzy miasta różnej wielkości dają gradient: Warszawa, Radom i Płock.

- **Co sprawdzamy:** jak model rozumie „duży” i „mały”, czy zmienia to wraz z miastem i czy oba określenia dostają spójne progi.
- **Czego się spodziewamy:** różne podejścia, np. próg powierzchni, kilka skrajnych parków albo porównanie ze średnią. Jeśli progi dla „dużych” i „małych” nie stykają się albo zachodzą na siebie, znaczy to, że model dobiera je osobno przy każdym pytaniu. Co dokładnie mierzymy, ustalimy po pierwszych próbach.

### Do sprawdzenia w bazie przed uruchomieniem

- **Drugie miejsce.** Trzeba wybrać stację peryferyjną i sprawdzić jej nazwę w bazie (`gis_osm_transport_free`, `fclass = 'railway_station'`). Warunek: w okolicy muszą być apteki i szpitale, bo inaczej nie będzie czego porównać z centrum. Warszawa Płudy to kandydat do weryfikacji.
- **Liczba obiektów każdego rodzaju wokół obu miejsc:** apteki i szpitale w promieniu 500 m, 1 km, 2 km i 5 km. Daje to dwie rzeczy: potwierdzenie, że miejsca naprawdę różnią się gęstością, oraz tabelę pokazującą, jak liczba wyników zmienia się z promieniem. Jeśli w jakimś promieniu nie ma ani jednego obiektu, model może zmienić interpretację, a my chcemy to umieć odróżnić.
- **Płock i Radom (części 2c i 2d):** czy mają w danych granicę miasta i jednostki niższego poziomu, czy mają kawiarnie i apteki oraz czy mają parki, które da się porównać z warszawskimi.
