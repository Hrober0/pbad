# Plan eksperymentów: przykładowe pytania

Kilka przykładowych pytań do każdego eksperymentu, a dla każdego z nich: co chcemy sprawdzić i czego się spodziewamy. Hipotezy i metoda: [informacje-ogolne.md](../informacje-ogolne.md). Poziomy kontekstu: [poziomy-kontekstu.md](poziomy-kontekstu.md).

| | Eksperyment 1 | Eksperyment 2 |
|---|---|---|
| Hipoteza | H1 | H2 |
| Co zmieniamy | poziom kontekstu K0–K3 | określenie przestrzenne, rodzaj obiektu, sytuacja pytającego |
| Co jest stałe | wersja pytania (naturalna) | kontekst K3, punkt odniesienia (Dworzec Centralny) |
| Pytania | 20 z [pytania-testowe.md](pytania-testowe.md) | 24 (część 2a) + 4 (część 2b) = 28 |
| Powtórzenia | 3 | 10 |
| Liczba wywołań | 20 × 4 × 3 = 240 | 28 × 10 = 280 |
| Odpowiedź modelu | samo zapytanie SQL | JSON `{"sql": "...", "uwagi": "..."}` |
| Co mierzymy | trafność na każdym poziomie i jej przyrosty, rodzaje błędów | przyjęty promień, rodzaj interpretacji, ujawnienie założenia |
| Potwierdzenie hipotezy | przyrost K1 → K2 większy niż K0 → K1 i K2 → K3 | promień zmienia się z rodzajem obiektu i sytuacją pytającego |
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

Sprawdzamy, czy wartość, którą model przyjmuje dla niejasnego określenia przestrzennego, zależy od kontekstu pytania. Kontekst to rodzaj szukanego obiektu i sytuacja pytającego. Punkt odniesienia jest zawsze ten sam, Dworzec Centralny, żeby różnice wynikały tylko z kontekstu.

### Co dokładnie dostaje model

Tak jak w eksperymencie 1, każda próba to jedno wywołanie bez historii. Wiadomość ma trzy części:

1. **Instrukcja zadania z eksperymentu 1** ze zmienionym formatem odpowiedzi: zamiast samego bloku SQL model zwraca JSON `{"sql": "...", "uwagi": "..."}`, gdzie `uwagi` mogą pozostać puste. Instrukcja nie wspomina o niejasności ani o założeniach, żeby nie podpowiadać modelowi, że ma je zgłaszać.
2. **Opis bazy na poziomie K3,** czyli najpełniejszy kontekst. Dzięki temu różnice nie wynikają z błędów technicznych, np. liczenia w stopniach zamiast w metrach.
3. **Treść pytania z tabel poniżej.** Sytuacja pytającego jest częścią pytania, np. „Idę pieszo. Wymień apteki w pobliżu Dworca Centralnego.”

Każde pytanie zadajemy 10 razy. Z każdej odpowiedzi odczytujemy:
- **przyjęty promień w metrach,** np. trzeci argument `ST_DWithin`,
- **rodzaj interpretacji:** promień, k najbliższych obiektów (`ORDER BY ... LIMIT`), obszar administracyjny albo inny,
- **czy model ujawnił przyjęte założenie** w polu `uwagi`.

Wynikiem jest tabela: mediana promienia i jego rozrzut dla każdej kombinacji kontekstu. Poprawności nie oceniamy, więc zapytania wzorcowe nie są potrzebne.

### Część 2a: określenia bez miary

Pytanie ma postać: „[sytuacja] Wymień [obiekty] [określenie] Dworca Centralnego.”

| Czynnik | Wartości |
|---|---|
| Określenie | „w pobliżu”, „niedaleko” |
| Rodzaj obiektu (rosnąca skala) | apteki, parki, szpitale, lotniska |
| Sytuacja pytającego | brak informacji, „Idę pieszo.”, „Jadę samochodem.” |

Daje to 2 × 4 × 3 = 24 pytania i 240 wywołań. Przykładowe pytania:

| Sytuacja | Pytanie |
|---|---|
| brak informacji | Wymień apteki w pobliżu Dworca Centralnego. |
| pieszo | Idę pieszo. Wymień apteki w pobliżu Dworca Centralnego. |
| samochodem | Jadę samochodem. Wymień apteki w pobliżu Dworca Centralnego. |
| brak informacji | Wymień lotniska niedaleko Dworca Centralnego. |
| pieszo | Idę pieszo. Wymień parki niedaleko Dworca Centralnego. |
| samochodem | Jadę samochodem. Wymień szpitale w pobliżu Dworca Centralnego. |

- **Co sprawdzamy:**
  - czy promień rośnie razem ze skalą obiektu (apteka → lotnisko),
  - czy rośnie przy zmianie z „pieszo” na „samochodem”,
  - czy „w pobliżu” i „niedaleko” dostają różne wartości,
  - jaką wartość domyślną model przyjmuje bez informacji o sytuacji pytającego.
- **Czego się spodziewamy:**
  - **Sytuacja pytającego:** wyraźny efekt. „Samochodem” daje promień kilka razy większy niż „pieszo”, bo kontekst jest podany wprost.
  - **Rodzaj obiektu:** słabszy efekt. Lotniska prawdopodobnie dostaną większy promień, ale apteki, parki i szpitale mogą dostać tę samą wartość, np. 1 km.
  - **Bez informacji o sytuacji:** okrągła wartość, 500 m albo 1 km, najczęściej bez wzmianki w polu `uwagi`.
  - **Lotniska:** możliwa zmiana interpretacji z promienia na „k najbliższych”, bo w promieniu kilometra lotniska nie ma. To też jest ciekawy wynik.
- **Jak rozstrzygamy H2:**
  - promień zależy od obu czynników, czyli H2 potwierdzona,
  - zależy tylko od sytuacji pytającego, czyli potwierdzona częściowo,
  - nie zależy od żadnego, czyli H2 obalona.

### Część 2b: miara czasu do przeliczenia

| Sytuacja | Pytanie |
|---|---|
| brak informacji | Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |
| pieszo | Idę pieszo. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |
| rowerem | Jadę rowerem. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |
| samochodem | Jadę samochodem. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. |

Daje to 4 pytania i 40 wywołań.

- **Co sprawdzamy:**
  - jaką prędkość przyjmuje model dla każdego środka transportu (prędkość = promień / 15 minut),
  - jaki środek transportu zakłada, gdy pytający go nie podał,
  - czy uwzględnia, że droga jest dłuższa niż linia prosta, np. przez współczynnik krętości dróg,
  - czy zaznacza, że bez sieci dróg nie da się dokładnie policzyć czasu dojazdu.
- **Czego się spodziewamy:**
  - promień ok. 1,2 km pieszo (5 km/h), ok. 4 km rowerem (15 km/h) i 7,5–12,5 km samochodem (30–50 km/h w mieście),
  - bez informacji o środku transportu najpewniej założy chodzenie pieszo,
  - ograniczenie wynikające z braku sieci dróg wspomni rzadko.

### Do sprawdzenia w bazie przed uruchomieniem

- **Lotniska:** czy są w danych pod `fclass = 'airport'` (w `gis_osm_transport_free` albo `gis_osm_transport_a_free`) i czy jest tam Lotnisko Chopina.
- **Liczba obiektów każdego rodzaju w okolicy dworca:** apteki, parki i szpitale. Jeśli w jakimś promieniu nie ma ani jednego obiektu, model może zmienić interpretację, a my chcemy to umieć odróżnić.
