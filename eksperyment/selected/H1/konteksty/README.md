# Konteksty bazy danych (K0–K3)

Każdy plik `kontekst.txt` zawiera dokładnie ten tekst, który trafia do promptu w miejsce `<KONTEKST>`. Pełną instrukcję zadania opisuje [poziomy-kontekstu.md](../../../draft/poziomy-kontekstu.md#część-wspólna-dla-wszystkich-poziomów). Poziomy są kumulatywne, a każdy plik jest kompletny, więc skrypt wczytuje tylko jeden plik.

| Poziom | Plik | Co zawiera | Rozmiar |
|---|---|---|---|
| K0 | [K0/kontekst.txt](K0/kontekst.txt) | nazwy 20 tabel i ich kolumn | ok. 1,4 tys. znaków |
| K1 | [K1/kontekst.txt](K1/kontekst.txt) | `CREATE TABLE` z typami, kluczem głównym i typem geometrii z SRID | ok. 4,2 tys. znaków |
| K2 | [K2/kontekst.txt](K2/kontekst.txt) | K1 + opis tabel i kolumn, wartości `fclass` każdej tabeli, znaczenie wybranych wartości `fclass`, fakty o danych | ok. 18,7 tys. znaków |
| K3 | [K3/kontekst.txt](K3/kontekst.txt) | K2 + wskazówki dotyczące pisania zapytań i 5 przykładów pytanie → SQL | ok. 23,8 tys. znaków |

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

## Dane, na których stoją konteksty

Plik `mazowieckie-261120-free.gpkg.zip` z Geofabrik, zrzut z **2026-11-20**.

- SHA-256 archiwum: `c5b88d39991946685b8e10845e6175b81caf1353a1fda64c38cf7ee400acf621`
- SHA-256 rozpakowanego `mazowieckie.gpkg`: `be32eee5ccbdb994f743ad3e5d41e8c757fb5a52d803be8b7110a32eb1c59a7a`

Wcześniejsza wersja kontekstów powstała na zrzucie z 2026-10-29. Tamten plik nie
jest już dostępny u Geofabrika (serwer trzyma tylko najnowszy zrzut), więc całość
przeniesiono na 20.11 i zweryfikowano ponownie na świeżo zaimportowanej bazie.

**Co się zgadzało bez zmian:** struktura wszystkich 20 tabel (nazwy i typy kolumn,
SRID 4326), listy `fclass` 19 z 20 tabel oraz wszystkie fakty o danych — szpitale
w Warszawie 7 punktów / 37 poligonów, wypożyczalnie rowerów 129 / 223, „Warszawa
Centralna", „PGE Narodowy", „Pałac Kultury i Nauki" w `buildings`, granica
Warszawy powtórzona jako `admin_level6/7/8` o identycznej geometrii, brak
wspólnych `osm_id` w parach tabel, `name` jako pusty napis zamiast `NULL`,
poligony `riverbank` bez nazw (651 z 662).

**Co poprawiono (2026-11-21):**

| Poziom | Zmiana | Powód |
|---|---|---|
| K2, K3 | `gis_osm_protected_areas_a_free.fclass`: dopisane `iucn_3` | jedyna różnica w listach `fclass` między zrzutami |
| K2, K3 | opis `railway_station` mówi teraz, że ten `fclass` obejmuje też stacje metra | w Warszawie 39 z 50 obiektów `railway_station` to metro, a nie kolej; stary opis („większa stacja kolejowa") był po prostu nieprawdziwy i psuł pytania A03 i A08 |
| K2, K3 | nowy fakt: parki z `landuse` to nadzbiór parków z `pois_a` | ujednolica regułę dla wszystkich pytań o parki |
| K2, K3 | nowy fakt: ten sam znany obiekt bywa jednocześnie poligonem w `buildings_a`, poligonem w `pois_a` i punktem w `pois_free`, a odległości od tych geometrii różnią się | bez tego pytania o „apteki w promieniu 500 m od PKiN" nie mają jednej poprawnej odpowiedzi (12 vs 9) |
| K2, K3 | nowy fakt: nazwę obiektu nosi czasem mniejszy obiekt w jego wnętrzu | w bazie są dwa sklepy z pamiątkami „Zamek Królewski" |
| K3 | dwie nowe wskazówki: łączyć dopasowanie nazwy z warunkiem na `fclass`; przy wyborze obiektu odniesienia brać poligon, nie punkt | to są właśnie wskazówki „jak pisać zapytania", czyli zawartość poziomu K3 |

Żadna z tych zmian nie podaje nazwy obiektu z pytań testowych. Konsekwencje dla
zapytań wzorcowych opisuje sekcja „Ustalenia rozstrzygające niejasności"
w [pytania.md](../pytania.md).

Wyniki pilotażu z 13.11 ([przyklad.md](../../../przyklad.md)) powstały na zrzucie
z 29.10 i na starszych kontekstach — liczby tokenów są tam o kilkaset za niskie
względem obecnych plików. Pilotaż zostaje jako ilustracja, ale nie jako pomiar.

Po wczytaniu kolejnego, nowszego pliku trzeba ponownie wygenerować listy `fclass`
i powtórzyć sprawdzenie faktów.
