## Cel badania (co chcemy się dowiedzieć i po co)

Chcemy sprawdzić, jak różne sposoby zwiększania kontekstu wpływają na jakość zapytań przestrzennych SQL generowanych przez modele językowe oraz jak modele te radzą sobie z niejasnymi pytaniami. Dzięki temu dowiemy się, jakie informacje warto przekazywać modelowi i na ile można polegać na jego interpretacji pytań o dane przestrzenne.

## Hipoteza badawcza (hipoteza musi być testowalna)

**H1:** Im pełniejszą informację o schemacie, danych i narzędziach GIS dostaje model, tym wyższy jest odsetek poprawnych zapytań przestrzennych SQL.

**H2:** Im bardziej niejasne jest pytanie, tym mniej powtarzalne są wyniki generowanych zapytań przestrzennych SQL.

## Metoda (jakie narzędzia badawcze, jakie eskperymenty, warunki eksperymentów, jakie narzędzia informatyczne, punkt odniesienia)

- Eksperyment 1 (H1): 20 pytań testowych zadajemy modelowi na czterech poziomach kontekstu (K0–K3), po 3 powtórzenia. Liczymy odsetek poprawnych zapytań. Zapytanie jest poprawne, gdy zwraca taki sam wynik jak zapytanie wzorcowe. Każdą próbę oceniamy osobno, a odsetek liczymy ze wszystkich prób na danym poziomie.
- Eksperyment 2 (H2): około 5 zadań zapisujemy na trzech poziomach niejasności (S1 jasne, S2 średnio niejasne, S3 bardzo niejasne) i każde pytanie zadajemy 10 razy przy stałym kontekście K2. Powtarzalność mierzymy indeksem Jaccarda, a dodatkowo zapisujemy wartości przyjęte przez model.
- Warunki eksperymentów: jedno wywołanie modelu bez historii i bez poprawiania zapytań, ten sam model i te same ustawienia we wszystkich próbach. Pytania, treść poziomów i kryteria oceny ustalamy przed badaniem.

## Potrzebne zasoby, dane, materiały

- Dane OpenStreetMap dla województwa mazowieckiego z Geofabrik: https://download.geofabrik.de/europe/poland/mazowieckie.html
- Dokumentacja danych Geofabrik: https://download.geofabrik.de/osm-data-in-gis-formats-free.pdf
- Baza PostgreSQL z PostGIS uruchamiana w Dockerze: [docker-compose.yml](docker/docker-compose.yml)
- `ogr2ogr` (instalowany z QGIS) do załadowania danych do bazy
- Claude API z określonym budżetem
- Zestaw pytań testowych

## Zmienne zależne/niezależne (co będzie zmieniane, co będzie mierzone)

#TODO

## Oczekiwane wyniki (jakie są możliwe wyniki i jak zaadresują hipoteze, co dodatkowego można sprawdzić/zrobić)

#TODO

## Brak trudności, ryzyka (czego nie wiemy, czego brakuje, co może pójść nie tak)

#TODO

## Zadania do wykonania i ich alokacja (jakie działania są wymagane)

- poprawić dane do eksperymentów i ostateczne ustalić hipotezę

- przygotowanie prezentacji zgodnie z wymaganiami

- dalszy ciąg przeglądu literatury jak będziemy już dokładnie wiedzili co mamy robić

- interfejs do konsolowego zadania pytań

- sprawdzić korzystanie z Claude API - konfiguracja, jak można zwiększać kontekst, jak można zmuszać do ustrukturyzowanej odpowiedzi, jak można zmieniać parametry modelu

- przedstawić wnioski na spotkaniu z opiekunem

- eksperymenty i draft artykułu
