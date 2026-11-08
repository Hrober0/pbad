# H2: algorytm oceny

Algorytm rozstrzyga, czy H2 jest potwierdzona, na podstawie wartości przyjętych przez model. Pytania i kody wariantów: [pytania.md](pytania.md). Progi ustalamy przed uruchomieniem eksperymentu i nie zmieniamy ich po zobaczeniu wyników.

## Pojęcia

- **Próba** to jedno wywołanie modelu dla jednego wariantu. Każdy wariant ma 3 próby.
- **Czynnik** to jeden element kontekstu pytania, który według H2 może zmienić wartość przyjętą przez model. Mamy trzy czynniki:
  - **S, sytuacja pytającego:** brak informacji, pieszo, rowerem albo samochodem,
  - **M, miejsce:** centrum Warszawy, peryferie Warszawy albo małe miasto,
  - **O, rodzaj i skala obiektu:** szukany obiekt (apteka albo szpital) albo punkt odniesienia (kiosk albo lotnisko).

  Każdy czynnik oceniamy osobno. Bierzemy wszystkie pary wariantów, które różnią się **tylko** tym czynnikiem, a resztę mają taką samą, i sprawdzamy, czy wartość zmienia się w oczekiwanym kierunku. Pary dla każdego czynnika są wypisane w sekcji „Porównania”.
- **Niewiadoma** to wartość, którą model musiał sam przyjąć. Odczytujemy ją z wygenerowanego SQL. Zależnie od interpretacji jest to:

| Rodzaj interpretacji | Niewiadoma | Jednostka | Skąd w SQL |
|---|---|---|---|
| `PROMIEŃ` | odległość od punktu odniesienia | m | trzeci argument `ST_DWithin`, warunek `ST_Distance(...) < x`, promień `ST_Buffer` |
| `K_NAJBLIŻSZYCH` | liczba zwracanych obiektów | sztuki | `ORDER BY ... LIMIT k` |
| `OBSZAR` | powierzchnia obszaru, w którym szukamy | m² | geometria użyta w `ST_Intersects` lub `ST_Within`, np. granica dzielnicy albo prostokąt |
| `PRÓG` | próg wielkości obiektu | m² | warunek `ST_Area(...) > x` lub `< x` |
| `INNY` | brak | – | każdy inny przypadek, opisywany ręcznie |

## Porównania

Każde porównanie to para wariantów (A, B) i oczekiwany kierunek, czyli B > A. Kierunki wynikają z H2: wartość rośnie przy szybszym środku transportu, w okolicy o mniejszej gęstości obiektów i przy obiekcie większej skali.

| Czynnik | Porównania (A < B) | Liczba |
|---|---|---|
| **S: sytuacja pytającego** | 1b<1c, 2b<2c, 3b<3c, 4b<4c, 5b<5c, 6b<6c, 7b<7c, 8b<8d, 8d<8c | 9 |
| **M: miejsce** | 1x<3x, 1x<5x, 2x<4x dla x ∈ {a, b, c} | 9 |
| **O: rodzaj i skala obiektu** | 1x<2x, 3x<4x, 6x<7x dla x ∈ {a, b, c} | 9 |

Porównania bez oczekiwanego kierunku raportujemy opisowo i nie wliczamy ich do rozstrzygnięcia. Sprawdzamy w nich tylko, czy wartości się różnią:
- 1a i 1d, czyli „w pobliżu” i „niedaleko”,
- 8a i 8b, 8c, 8d, czyli jaki środek transportu model zakłada domyślnie,
- 9a, 9b, 9c oraz 10a, 10b, czyli „centrum” w różnych miastach,
- 11a, 11b, 11c oraz 12a, 12b, 12c, czyli próg „duży” i „mały” w różnych miastach.

## Progi

Progi działają na trzech poziomach: pojedynczy wariant, para wariantów i cały czynnik.

| Stała | Wartość | Poziom | Co oznacza |
|---|---|---|---|
| `MIN_PROB` | 2 | wariant | Z 3 prób wariantu co najmniej 2 muszą dać wartość, którą da się odczytać, i to tego samego rodzaju, np. obie promień. Inaczej wariant jest niestabilny i nie bierze udziału w porównaniach. |
| `MIN_ILORAZ` | 1,25 | para | Mediana wariantu B musi być co najmniej 1,25 raza większa od mediany wariantu A. Na przykład przy A = 500 m wariant B musi mieć co najmniej 625 m, a przy A = 800 m co najmniej 1000 m. |
| `MIN_ROZSTRZYGNIETYCH` | połowa porównań czynnika, w górę | czynnik | Część porównań może odpaść, bo wariant był niestabilny albo model zmienił rodzaj interpretacji. Jeśli zostanie mniej niż połowa porównań czynnika (zaokrąglona w górę), czynnik ma za mało danych i nie oceniamy go. Obecnie każdy czynnik ma 9 porównań, więc próg wynosi 5. Po zmianie listy pytań próg zmienia się sam. |
| `MIN_UDZIAL_ZGODNYCH` | 2/3 | czynnik | Spośród porównań, które zostały, co najmniej 2/3 musi wykazać różnicę w oczekiwanym kierunku. |

**Dlaczego 1,25:** przypadkowe wahania odsiewa już warunek, że wartości z powtórzeń się nie nakładają. Iloraz ma tylko odrzucić różnice zbyt małe, żeby miały praktyczne znaczenie, np. 500 i 550 m. Próg 1,25 przepuszcza najmniejsze typowe kroki między okrągłymi wartościami, np. 400 → 500 m albo 800 → 1000 m. Próg 1,5 odrzucałby takie zmiany, choć mogą być prawdziwą reakcją na kontekst.

**Dlaczego 2/3:** czynnik może działać, nawet jeśli w pojedynczych porównaniach model się nie wykaże, np. przy szpitalach przyjmie ten sam promień co przy aptekach. Wymagamy wyraźnej większości porównań, a nie wszystkich.

**Przykład dla czynnika „sytuacja pytającego” (9 porównań):**
- 1 wariant niestabilny, czyli porównanie odpada; zostaje 8 porównań, więc warunek `MIN_ROZSTRZYGNIETYCH` (co najmniej 5, czyli połowa z 9 w górę) jest spełniony,
- 6 porównań `ZGODNE`, 2 `BRAK_RÓŻNICY`, czyli 6 z 8 = 75%,
- 75% to więcej niż 2/3, więc czynnik **ma wpływ**.

## Rozstrzygnięcie H2

Najpierw każdy z trzech czynników (S, M, O) dostaje jeden z werdyktów:

| Werdykt czynnika | Kiedy |
|---|---|
| **ma wpływ** | rozstrzygniętych porównań jest co najmniej `MIN_ROZSTRZYGNIETYCH`, a co najmniej 2/3 z nich jest zgodnych z oczekiwanym kierunkiem |
| **brak wpływu** | rozstrzygniętych porównań jest wystarczająco dużo, ale zgodnych jest mniej niż 2/3 |
| **nierozstrzygnięty** | rozstrzygniętych porównań jest mniej niż `MIN_ROZSTRZYGNIETYCH` |

Potem z werdyktów czynników wynika werdykt całej hipotezy:

| Werdykt H2 | Kiedy | Co to znaczy |
|---|---|---|
| **potwierdzona** | wszystkie 3 czynniki mają wpływ | model dopasowuje przyjętą wartość do sytuacji pytającego, miejsca i obiektu |
| **potwierdzona częściowo** | 1 lub 2 czynniki mają wpływ | model reaguje na część kontekstu; w wynikach podajemy, na który |
| **obalona** | żaden czynnik nie ma wpływu, a wszystkie 3 są rozstrzygnięte | model stosuje stałe wartości domyślne niezależnie od kontekstu |
| **nierozstrzygnięta** | żaden czynnik nie ma wpływu, a co najmniej 1 jest nierozstrzygnięty | za mało danych, np. model często zmieniał interpretację albo odpowiadał niestabilnie |

Treść H2 mówi, że kontekst zmienia przyjętą wartość, ale nie wymaga, żeby robił to każdy jego element. Dlatego jeden czynnik z wpływem wystarcza do częściowego potwierdzenia, a pełne potwierdzenie wymaga wszystkich trzech.

**Przykład:** S ma wpływ (7 z 9 porównań zgodnych), M nie ma wpływu (2 z 9), O ma wpływ (6 z 8). Wpływ mają 2 czynniki, więc H2 jest **potwierdzona częściowo**. Wniosek: model reaguje na sposób poruszania się i na wielkość obiektu, ale nie bierze pod uwagę gęstości zabudowy w okolicy.

**Wynik odwrotny do oczekiwań:** jeśli w czynniku większość porównań wyjdzie `PRZECIWNE`, np. dla samochodu model przyjmuje mniejszy promień niż dla pieszego, czynnik dostaje werdykt „brak wpływu”, bo nie zgadza się z kierunkiem z H2. Taki wynik opisujemy jednak osobno, bo oznacza, że model reaguje na kontekst, tylko inaczej, niż zakładaliśmy.

## Przykład

Pytania 1b i 1c, czyli apteki w pobliżu Dworca Centralnego, pieszo i samochodem:
- 1b: trzy próby, wszystkie typu `PROMIEŃ`: 500, 500, 300 m. Mediana 500 m.
- 1c: trzy próby, wszystkie typu `PROMIEŃ`: 2000, 1000, 2000 m. Mediana 2000 m.
- min(1c) = 1000 > max(1b) = 500, a 2000 ≥ 1,25 · 500. Wynik: `ZGODNE`.

Gdyby w 1c jedna próba miała 500 m, warunek min(1c) > max(1b) nie byłby spełniony. Wynik byłby wtedy `BRAK_RÓŻNICY`, mimo że mediana jest większa.

## Ograniczenia

- **Przy 3 próbach na wariant nie robimy testu statystycznego dla pojedynczej pary.** Najmniejsze możliwe p w teście Manna–Whitneya przy 3 + 3 obserwacjach to 0,1. Zastępuje go warunek braku nakładania się wartości. Test znaków na poziomie czynnika daje p ≈ 0,002, gdy wszystkie 9 porównań jest zgodnych.
- **`ZMIANA_INTERPRETACJI` nie liczy się ani za, ani przeciw kierunkowi.** Dlatego czynnik, w którym model często zmienia interpretację, może wyjść `NIEROZSTRZYGNIĘTY`. Takie przypadki opisujemy w artykule osobno, bo też pokazują reakcję na kontekst.
- **Progi są arbitralne.** W artykule podajemy je wprost i pokazujemy, czy werdykt zmienia się przy progach 1,5 i 2.
