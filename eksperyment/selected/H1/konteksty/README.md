# Konteksty bazy danych (K0–K3)

Każdy plik `kontekst.txt` zawiera dokładnie ten tekst, który trafia do promptu w miejsce `<KONTEKST>`. Pełną instrukcję zadania opisuje [poziomy-kontekstu.md](../../../draft/poziomy-kontekstu.md#część-wspólna-dla-wszystkich-poziomów). Poziomy są kumulatywne, a każdy plik jest kompletny, więc skrypt wczytuje tylko jeden plik.

| Poziom | Plik | Co zawiera | Rozmiar |
|---|---|---|---|
| K0 | [K0/kontekst.txt](K0/kontekst.txt) | nazwy 20 tabel i ich kolumn | ok. 1,4 tys. znaków |
| K1 | [K1/kontekst.txt](K1/kontekst.txt) | `CREATE TABLE` z typami, kluczem głównym i typem geometrii z SRID | ok. 4,2 tys. znaków |
| K2 | [K2/kontekst.txt](K2/kontekst.txt) | K1 + opis tabel i kolumn, wartości `fclass` każdej tabeli, znaczenie wybranych wartości `fclass`, fakty o danych | ok. 17 tys. znaków |
| K3 | [K3/kontekst.txt](K3/kontekst.txt) | K2 + wskazówki dotyczące pisania zapytań i 5 przykładów pytanie → SQL | ok. 21 tys. znaków |

Dokładną liczbę tokenów odczytamy z `usage.input_tokens` przy pierwszym wywołaniu API.

## Skąd pochodzi treść

- **Z bazy, zapytaniami do `information_schema` i `geometry_columns`:**
  - K0, czyli nazwy tabel i kolumn,
  - K1, czyli DDL,
  - listy wartości `fclass` w K2 (`SELECT DISTINCT fclass`).
- **Napisane ręcznie:**
  - opisy tabel i kolumn oraz znaczenie wartości `fclass` w K2, na podstawie dokumentacji Geofabrik ([K2/osm-data-in-gis-formats-free.pdf](K2/osm-data-in-gis-formats-free.pdf), wersja z 2026-04-02),
  - fakty o danych w K2, sprawdzone zapytaniami do bazy,
  - wskazówki i przykłady w K3.
- **Gdy dokumentacja różni się od bazy, w K2 obowiązuje stan bazy.** Według dokumentacji tabele `buildings` i `railways` nie mają kolumny `name`. W naszym pliku GeoPackage mają ją, a część obiektów ma nazwy, np. „Pałac Kultury i Nauki” w `buildings`. Podobnie poligony koryt rzek mają w bazie `fclass = 'riverbank'`, a nie `'river'` jak w dokumentacji.
- **Przykłady w K3** zostały wykonane na bazie i zwracają sensowne wyniki. Nie używają żadnego obiektu ani wartości `fclass` z pytań testowych.
- **Żaden poziom nie podaje nazwy obiektu z pytań testowych,** np. „Warszawa Centralna” czy „PGE Narodowy”. Model musi sam znaleźć je w bazie.

Dane: plik `mazowieckie-latest-free.gpkg` z Geofabrik z 2026-10-29. Po wczytaniu nowszego pliku trzeba ponownie wygenerować listy `fclass`.
