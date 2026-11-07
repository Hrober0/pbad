# Plan eksperymentów: przykładowe pytania

Kilka przykładowych pytań do każdego eksperymentu, a dla każdego z nich: co chcemy sprawdzić i czego się spodziewamy. Hipotezy i metoda: [informacje-ogolne.md](../informacje-ogolne.md). Poziomy kontekstu: [poziomy-kontekstu.md](poziomy-kontekstu.md).

| | Eksperyment 1 | Eksperyment 2 |
|---|---|---|
| Hipoteza | H1 | H2 |
| Co zmieniamy | poziom kontekstu K0–K3 | niejasność pytania S1–S3 |
| Co jest stałe | wersja pytania (naturalna) | kontekst K3 |
| Pytania | 20 z [pytania-testowe.md](pytania-testowe.md) | ok. 5 zadań × 3 poziomy niejasności |
| Powtórzenia | 3 | 10 |
| Liczba wywołań | 20 × 4 × 3 = 240 | 5 × 3 × 10 = 150 |
| Odpowiedź modelu | samo zapytanie SQL | JSON `{"sql": "...", "uwagi": "..."}` |
| Co mierzymy | odsetek poprawnych zapytań, rodzaje błędów | indeks Jaccarda, przyjęte wartości, sygnalizowanie niejasności |

---

## Eksperyment 1: wpływ kontekstu (H1)

Pytania są w wersji naturalnej (P2) z [pytania-testowe.md](pytania-testowe.md). Każde ma jedno zapytanie wzorcowe.

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

## Eksperyment 2: niejasność pytań (H2)

Wszystkie pytania zadajemy na poziomie K3. Każde zwraca listę obiektów, czyli `osm_id` i nazwę. Dla S1 istnieje zapytanie wzorcowe. Dla S2 i S3 nie oceniamy poprawności, tylko:
- powtarzalność, czyli średni indeks Jaccarda między 10 wynikami,
- wartości przyjęte przez model, odczytane z SQL,
- czy model zasygnalizował niejasność w polu `uwagi`.

Obiekty z zadań 1 i 2 (Dworzec Centralny, PKiN, dzielnica Śródmieście) sprawdziliśmy wcześniej w bazie. Jeziora w zadaniu 3 i ewentualne obszary „centrum” na niższych poziomach administracyjnych trzeba jeszcze sprawdzić.

### Zadanie 1: odległość pieszo

| Poziom | Pytanie |
|---|---|
| S1 jasne | Wymień apteki w promieniu 500 m od Dworca Centralnego. |
| S2 średnio niejasne | Wymień apteki, do których dojdę w 10 minut spacerem od Dworca Centralnego. |
| S3 bardzo niejasne | Wymień apteki w pobliżu Dworca Centralnego. |

- **Co sprawdzamy:**
  - jaką prędkość marszu przyjmuje model w S2: 4 km/h daje ok. 670 m, 5 km/h ok. 830 m, 6 km/h 1 km,
  - jaki promień uznaje za „w pobliżu” w S3,
  - czy liczy w linii prostej i czy w ogóle wspomina, że prawdziwa droga pieszo jest dłuższa.
- **Czego się spodziewamy:**
  - **S1:** Jaccard ≈ 1.
  - **S2:** model przeliczy czas na odległość, prawdopodobnie zawsze tak samo, np. 800 m, i bez komentarza.
  - **S3:** jedna okrągła wartość, 500 m albo 1 km. Wyniki będą powtarzalne, ale pytający nie wie, jaki promień przyjęto.

  Taki wynik potwierdza H2 przez ukryte wartości domyślne, a nie przez losowość.

### Zadanie 2: niejasny obszar

| Poziom | Pytanie |
|---|---|
| S1 jasne | Wymień kawiarnie w dzielnicy Śródmieście. |
| S2 średnio niejasne | Wymień kawiarnie w ścisłym centrum Warszawy. |
| S3 bardzo niejasne | Wymień kawiarnie w centrum. |

- **Co sprawdzamy:** jak model definiuje „centrum”, gdy nie ma jednej oczywistej geometrii. Możliwości:
  - granica dzielnicy Śródmieście,
  - promień wokół PKiN (jaki?),
  - mniejsza jednostka administracyjna, np. Śródmieście Północne, jeśli jest w danych,
  - prostokąt ze współrzędnymi z pamięci.

  W S3 brakuje nawet nazwy miasta. Sprawdzamy, czy model założy Warszawę.
- **Czego się spodziewamy:**
  - **S1:** Jaccard ≈ 1.
  - **S2 i S3:** różne podejścia w kolejnych powtórzeniach, więc niski Jaccard. To zadanie jest głównym kandydatem do potwierdzenia H2.

  Spodziewamy się, że model nie zaznaczy niejasności i za każdym razem zwróci zapytanie bez zastrzeżeń.

### Zadanie 3: czas dojazdu poza miasto

| Poziom | Pytanie |
|---|---|
| S1 jasne | Wymień jeziora położone do 60 km od granicy Warszawy. |
| S2 średnio niejasne | Wymień jeziora, do których dojadę z Warszawy samochodem w godzinę. |
| S3 bardzo niejasne | Wymień jeziora niedaleko Warszawy. |

- **Co sprawdzamy:**
  - jaką prędkość przyjmuje model w S2 (50, 60, 80 km/h?),
  - od czego liczy odległość: od granicy miasta, od jego środka czy od PKiN,
  - czy zauważy, że bez sieci dróg czasu dojazdu nie da się policzyć dokładnie.

  Jest to przypadek, o który pytał opiekun („coś, do czego moglibyśmy dojechać z Warszawy w godzinę”).
- **Czego się spodziewamy:**
  - **S2:** promień 50–80 km, liczony od różnych punktów odniesienia, więc Jaccard średni.
  - **S3:** okrągła wartość, np. 30 km albo 50 km.

  Dane obejmują tylko województwo mazowieckie, więc przy dużym promieniu wyniki będą ucięte granicą województwa. Trzeba to opisać jako ograniczenie, ale nie wpływa to na porównanie między powtórzeniami.

### Kandydaci na zadania 4 i 5

- **Niejasna cecha obiektu:**
  - S1: „parki w Warszawie o powierzchni ponad 20 ha”,
  - S2: „duże parki w Warszawie”,
  - S3: „parki w Warszawie na długi spacer”.

  Sprawdza niejasność, która nie dotyczy odległości.
- **Niejasność przy mało znanym obiekcie:**
  - S1: „przystanki autobusowe do 300 m od Skweru Jolanty Brzeskiej”,
  - S2: „5 minut pieszo od…”,
  - S3: „blisko…”.

  Sprawdza, czy przy obiekcie, którego model nie zna, przyjmuje te same wartości domyślne co przy Dworcu Centralnym.
