## Wybrane przykłady

Pilotaż: model `claude-sonnet-5-5`, effort `medium`, po jednym wywołaniu na poziom kontekstu albo wariant.

### Przykład o numerze Z07 z eksperymentu nr. 1

**Pytanie:** Ile supermarketów jest w Warszawie?

#### K0

**Liczba tokenów wejściowych:** 1450

**Odpowiedź:**

```sql
SELECT COUNT(*) AS liczba_supermarketow FROM (SELECT p.geom FROM gis_osm_pois_free p JOIN gis_osm_adminareas_a_free a ON a.name = 'Warszawa' AND ST_Intersects(a.geom, p.geom) WHERE p.fclass = 'supermarket' UNION ALL SELECT p.geom FROM gis_osm_pois_a_free p JOIN gis_osm_adminareas_a_free a ON a.name = 'Warszawa' AND ST_Intersects(a.geom, ST_PointOnSurface(p.geom)) WHERE p.fclass = 'supermarket') s;
```

**Wynik:**

```text
liczba_supermarketow
1497
```

---

#### K1

**Liczba tokenów wejściowych:** 2778

**Odpowiedź:**

```sql
SELECT COUNT(*) AS liczba_supermarketow FROM (SELECT p.geom FROM gis_osm_pois_free p WHERE p.fclass = 'supermarket' AND EXISTS (SELECT 1 FROM gis_osm_adminareas_a_free a WHERE a.name = 'Warszawa' AND ST_Intersects(a.geom, p.geom)) UNION ALL SELECT p.geom FROM gis_osm_pois_a_free p WHERE p.fclass = 'supermarket' AND EXISTS (SELECT 1 FROM gis_osm_adminareas_a_free a WHERE a.name = 'Warszawa' AND ST_Intersects(a.geom, ST_PointOnSurface(p.geom)))) s
```

**Wynik:**

```text
liczba_supermarketow
499
```

---

#### K2

**Liczba tokenów wejściowych:** 8972

**Odpowiedź:**

```sql
SELECT COUNT(DISTINCT s.osm_id) AS liczba_supermarketow FROM (SELECT osm_id, geom FROM gis_osm_pois_free WHERE fclass = 'supermarket' UNION ALL SELECT osm_id, ST_PointOnSurface(geom) AS geom FROM gis_osm_pois_a_free WHERE fclass = 'supermarket') s JOIN gis_osm_adminareas_a_free w ON w.fclass = 'admin_level6' AND w.name = 'Warszawa' AND ST_Intersects(w.geom, s.geom)
```

**Wynik:**

```text
liczba_supermarketow
499
```

---

#### K3

**Liczba tokenów wejściowych:** 11411

**Odpowiedź:**

```sql
WITH waw AS (SELECT geom FROM gis_osm_adminareas_a_free WHERE fclass = 'admin_level6' AND name = 'Warszawa'), sm AS (SELECT osm_id, geom FROM gis_osm_pois_free WHERE fclass = 'supermarket' UNION SELECT osm_id, geom FROM gis_osm_pois_a_free WHERE fclass = 'supermarket') SELECT count(DISTINCT sm.osm_id) AS supermarkets FROM sm, waw WHERE ST_Intersects(sm.geom, waw.geom)
```

**Wynik:**

```text
supermarkets
499
```

---

### Przykład o numerze M03 z eksperymentu nr. 1

**Pytanie:** Jaka jest odległość w linii prostej w metrach między Pałacem Kultury i Nauki a Stadionem Narodowym?

#### K0

**Liczba tokenów wejściowych:** 1479

**Odpowiedź:**

```sql
SELECT ST_Distance(a.geom::geography, b.geom::geography) AS odleglosc_m FROM (SELECT ST_Centroid(ST_Collect(geom)) AS geom FROM (SELECT geom FROM gis_osm_buildings_a_free WHERE name ILIKE '%Pałac Kultury%' UNION ALL SELECT geom FROM gis_osm_pois_a_free WHERE name ILIKE '%Pałac Kultury%') x) a, (SELECT ST_Centroid(ST_Collect(geom)) AS geom FROM (SELECT geom FROM gis_osm_buildings_a_free WHERE name ILIKE '%Stadion Narodowy%' UNION ALL SELECT geom FROM gis_osm_pois_a_free WHERE name ILIKE '%Stadion Narodowy%') y) b
```

**Wynik:**

```text
odleglosc_m
2687.39133756
```

---

#### K1

**Liczba tokenów wejściowych:** 2807

**Odpowiedź:**

```sql
WITH a AS (SELECT geom FROM (SELECT name, geom FROM gis_osm_pois_free UNION ALL SELECT name, ST_Centroid(geom) FROM gis_osm_pois_a_free UNION ALL SELECT name, ST_Centroid(geom) FROM gis_osm_buildings_a_free) x WHERE name ILIKE '%Pałac Kultury i Nauki%' LIMIT 1), b AS (SELECT geom FROM (SELECT name, geom FROM gis_osm_pois_free UNION ALL SELECT name, ST_Centroid(geom) FROM gis_osm_pois_a_free UNION ALL SELECT name, ST_Centroid(geom) FROM gis_osm_buildings_a_free UNION ALL SELECT name, ST_Centroid(geom) FROM gis_osm_transport_a_free) y WHERE name ILIKE '%Stadion Narodowy%' LIMIT 1) SELECT ST_Distance(a.geom::geography, b.geom::geography) AS odleglosc_m FROM a, b
```

**Wynik:**

```text
3154.28510751
```

---

#### K2

**Liczba tokenów wejściowych:** 9001

**Odpowiedź:**

```sql
SELECT ST_Distance(a.geom::geography, b.geom::geography) AS odleglosc_m FROM (SELECT ST_Centroid(ST_Collect(geom)) AS geom FROM (SELECT geom FROM gis_osm_pois_free WHERE name ILIKE '%Pałac Kultury%' UNION ALL SELECT geom FROM gis_osm_pois_a_free WHERE name ILIKE '%Pałac Kultury%') x) a, (SELECT ST_Centroid(ST_Collect(geom)) AS geom FROM (SELECT geom FROM gis_osm_pois_free WHERE name ILIKE '%Stadion Narodowy%' AND fclass = 'stadium' UNION ALL SELECT geom FROM gis_osm_pois_a_free WHERE name ILIKE '%Stadion Narodowy%' AND fclass = 'stadium') y) b
```

**Wynik:**

```text
odleglosc_m
null
```

---

#### K3

**Liczba tokenów wejściowych:** 11440

**Odpowiedź:**

```sql
WITH a AS (SELECT geom FROM gis_osm_pois_free WHERE name ILIKE '%Pałac Kultury%' UNION ALL SELECT geom FROM gis_osm_pois_a_free WHERE name ILIKE '%Pałac Kultury%'), b AS (SELECT geom FROM gis_osm_pois_free WHERE name ILIKE '%Stadion Narodowy%' UNION ALL SELECT geom FROM gis_osm_pois_a_free WHERE name ILIKE '%Stadion Narodowy%') SELECT round(min(ST_Distance(a.geom::geography, b.geom::geography))::numeric) AS distance_m FROM a, b
```

**Wynik:**

```text
2527
```

---

### Przykład o numerze 1 z eksperymentu nr. 2

**Kontekst:** K2 we wszystkich wariantach

**Pytanie:** Wymień apteki w pobliżu Dworca Centralnego.

**Odpowiedź:**

```sql
WITH dc AS (SELECT geom FROM gis_osm_transport_free WHERE fclass = 'railway_station' AND name = 'Warszawa Centralna' LIMIT 1), apt AS (SELECT name, geom FROM gis_osm_pois_free WHERE fclass = 'pharmacy' UNION ALL SELECT name, ST_PointOnSurface(geom) FROM gis_osm_pois_a_free WHERE fclass = 'pharmacy') SELECT apt.name, ROUND(ST_Distance(apt.geom::geography, dc.geom::geography)) AS odleglosc_m FROM apt, dc WHERE ST_DWithin(apt.geom::geography, dc.geom::geography, 1000) ORDER BY ST_Distance(apt.geom::geography, dc.geom::geography)
```

**Wynik:**

```text
Dbam o Zdrowie,45
Super-Pharm,172
Dbam o Zdrowie,182
"",330
Dbam o Zdrowie,359
Cosmedica,405
Przy Lindleya,434
Wawa,539
Dbam o Zdrowie,542
Aptekarz Warszawski,650
Europa,658
Prima,661
Słoneczna,684
Słoneczna,706
Dbam o Zdrowie,709
Cefarm,727
Dr. Max,752
Sawa,763
Słoneczna,780
Na Wspólnej,808
Super-Pharm,896
Cefarm,905
Kliniczna,910
Aptekarz Warszawski,913
Ziko Apteka,939
Syrenka,991
Ziko Apteka,994
```

**Przyjęta wartość:** promień 1000m

---

**Pytanie:** Idę pieszo. Wymień apteki w pobliżu Dworca Centralnego.

**Odpowiedź:**

```sql
WITH dc AS (SELECT geom FROM gis_osm_transport_free WHERE fclass = 'railway_station' AND name = 'Warszawa Centralna' LIMIT 1), apteki AS (SELECT fid, osm_id, name, geom FROM gis_osm_pois_free WHERE fclass = 'pharmacy' UNION ALL SELECT fid, osm_id, name, ST_PointOnSurface(geom) FROM gis_osm_pois_a_free WHERE fclass = 'pharmacy') SELECT a.name, a.osm_id, ROUND(ST_Distance(a.geom::geography, dc.geom::geography)) AS odleglosc_m, ST_Y(a.geom) AS lat, ST_X(a.geom) AS lon FROM apteki a CROSS JOIN dc WHERE ST_DWithin(a.geom::geography, dc.geom::geography, 1000) ORDER BY odleglosc_m
```

**Wynik:**

```text
Dbam o Zdrowie,288935477,45,52.22859595,21.002614899207494
Super-Pharm,1333675064,172,52.2303559,21.0035021
Dbam o Zdrowie,1080555240,182,52.2273429,21.0042988
"",331106260,330,52.2263502,21.0004978
Dbam o Zdrowie,338509212,359,52.2277045,21.0080947
Cosmedica,338661544,405,52.2323568,21.0017715
Przy Lindleya,4551976497,434,52.2257683,20.9992087
Wawa,3693623805,539,52.2305476,21.0105322
Dbam o Zdrowie,310280495,542,52.226732,20.9960002
Aptekarz Warszawski,346403160,650,52.2346265,21.0041846
Europa,1535718899,658,52.2257358,21.0113672
Prima,4934955871,661,52.2316912,20.9946864
Słoneczna,4738323521,684,52.2231931,21.0071979
Słoneczna,369530075,706,52.2328609,20.9951926
Dbam o Zdrowie,367946843,709,52.2256802,21.0121958
Cefarm,314418382,727,52.2307719,21.0133107
Dr. Max,8942538973,752,52.2331034,21.0116679
Sawa,1111952497,763,52.2318559,21.0131705
Słoneczna,369523123,780,52.2281226,20.9918022
Na Wspólnej,3832853363,808,52.2272076,21.0146875
Super-Pharm,9790929331,896,52.2326257,20.9916017
Cefarm,311145360,905,52.2367789,21.0058853
Kliniczna,3822253566,910,52.2317362,21.0156051
Aptekarz Warszawski,3033983705,913,52.2305484,21.0162162
Ziko Apteka,3839329057,939,52.2366796,21.0081728
Syrenka,8688308543,991,52.2356232,20.9938061
Ziko Apteka,2534667586,994,52.2229261,21.0140872
```

**Przyjęta wartość:** promień 1000m

---

**Pytanie:** Jadę samochodem. Wymień apteki w pobliżu Dworca Centralnego.

**Odpowiedź:**

```sql
WITH dworzec AS (SELECT geom FROM gis_osm_transport_free WHERE fclass = 'railway_station' AND name = 'Warszawa Centralna' LIMIT 1) SELECT p.name, p.fclass, ST_Distance(p.geom::geography, d.geom::geography) AS odleglosc_m, ST_Y(p.geom) AS lat, ST_X(p.geom) AS lon FROM (SELECT name, fclass, geom FROM gis_osm_pois_free WHERE fclass = 'pharmacy' UNION ALL SELECT name, fclass, ST_PointOnSurface(geom) FROM gis_osm_pois_a_free WHERE fclass = 'pharmacy') p CROSS JOIN dworzec d WHERE ST_DWithin(p.geom::geography, d.geom::geography, 1500) ORDER BY odleglosc_m
```

**Wynik:**

```text
Dbam o Zdrowie,pharmacy,44.86237281,52.22859595
Super-Pharm,pharmacy,172.4161045,52.2303559
Dbam o Zdrowie,pharmacy,181.9186519,52.2273429
"",pharmacy,329.63307689,52.2263502
Dbam o Zdrowie,pharmacy,359.32665646,52.2277045
Cosmedica,pharmacy,404.74326095,52.2323568
Przy Lindleya,pharmacy,433.88276457,52.2257683
Wawa,pharmacy,539.11976079,52.2305476
Dbam o Zdrowie,pharmacy,541.62101833,52.226732
Aptekarz Warszawski,pharmacy,649.80329892,52.2346265
Europa,pharmacy,657.51051711,52.2257358
Prima,pharmacy,661.22159705,52.2316912
Słoneczna,pharmacy,684.28544413,52.2231931
Słoneczna,pharmacy,706.00200057,52.2328609
Dbam o Zdrowie,pharmacy,709.44620084,52.2256802
Cefarm,pharmacy,726.74366348,52.2307719
Dr. Max,pharmacy,751.66230958,52.2331034
Sawa,pharmacy,762.80656996,52.2318559
Słoneczna,pharmacy,779.93180339,52.2281226
Na Wspólnej,pharmacy,807.84985323,52.2272076
Super-Pharm,pharmacy,896.05014566,52.2326257
Cefarm,pharmacy,904.88666002,52.2367789
Kliniczna,pharmacy,910.0958598,52.2317362
Aptekarz Warszawski,pharmacy,912.55695264,52.2305484
Ziko Apteka,pharmacy,939.14717716,52.2366796
Syrenka,pharmacy,990.63501837,52.2356232
Ziko Apteka,pharmacy,993.84681339,52.2229261
Słoneczna,pharmacy,1033.8101143,52.2244397
Słoneczna,pharmacy,1087.62823392,52.2367821
Medicover,pharmacy,1093.097081,52.2374604
Słoneczna,pharmacy,1096.43149377,52.2351313
Dr. Max,pharmacy,1167.75013565,52.2388148
"",pharmacy,1177.23885918,52.2325637
Dr. Max,pharmacy,1201.03544921,52.2388513
Ziko Apteka,pharmacy,1217.90985424,52.2364693
Ziko Apteka,pharmacy,1238.60835631,52.234843
Ziko Apteka,pharmacy,1240.93658953,52.2349026
Aptekarz Warszawski,pharmacy,1287.95092252,52.2197915
Cefarm,pharmacy,1307.27175556,52.2358121
Ziko Apteka,pharmacy,1341.88684985,52.2221138
Dbam o Zdrowie,pharmacy,1357.99601324,52.2211699
Przy Placu Zbawiciela,pharmacy,1412.76524721,52.2202344
Europejska,pharmacy,1420.52277869,52.235443
```

**Przyjęta wartość:** promień 1500m

---

**Pytanie:** Wymień apteki niedaleko Dworca Centralnego.

**Odpowiedź:**

```sql
WITH dworzec AS (SELECT geom FROM gis_osm_transport_free WHERE fclass = 'railway_station' AND name = 'Warszawa Centralna' LIMIT 1), apteki AS (SELECT fid, osm_id, name, geom FROM gis_osm_pois_free WHERE fclass = 'pharmacy' UNION ALL SELECT fid, osm_id, name, ST_PointOnSurface(geom) FROM gis_osm_pois_a_free WHERE fclass = 'pharmacy') SELECT a.name, a.osm_id, ROUND(ST_Distance(a.geom::geography, d.geom::geography)) AS odleglosc_m FROM apteki a CROSS JOIN dworzec d WHERE ST_DWithin(a.geom::geography, d.geom::geography, 500) ORDER BY odleglosc_m
```

**Wynik:**

```text
Dbam o Zdrowie,288935477,45
Super-Pharm,1333675064,172
Dbam o Zdrowie,1080555240,182
"",331106260,330
Dbam o Zdrowie,338509212,359
Cosmedica,338661544,405
Przy Lindleya,4551976497,434
```

**Przyjęta wartość:** promień 500m

---

## Wnioski

Pilotaż obejmuje jedno wywołanie na każdy poziom albo wariant, więc nie pozwala jeszcze potwierdzić ani obalić H1 i H2. Pokazuje, gdzie pojawiają się różnice i z czego wynikają.

1. **Model zna schemat Geofabrik z wiedzy ogólnej,** więc już na K0 pisze sensowne zapytania: łączy tabele punktów i poligonów, liczy w metrach i szuka obiektów po fragmencie nazwy. Zna też wartości typów obiektów: na K0 sam wpisał `fclass = 'supermarket'`, choć listę wartości dostaje dopiero w K2.
2. **W Z07 model na każdym poziomie robił to samo:** brał supermarkety z obu tabel i liczył te, które leżą w granicy Warszawy. Różnica polegała na tym, jak szukał tej granicy. Na K0 szukał jej po samej nazwie „Warszawa”, a w bazie są trzy takie same granice o tej nazwie (Warszawa jako `admin_level6`, `7` i `8`). `JOIN` dopasował każdy supermarket do wszystkich trzech, więc każdy został policzony trzy razy (1497 zamiast 499). Na K1 wynik był poprawny tylko dlatego, że model użył `EXISTS`, które nie mnoży wierszy. Od K2 wybiera konkretną granicę (`admin_level6`), bo fakty o danych mówią mu, która to jest.
3. **W M03 na każdym poziomie model szukał stadionu po nazwie „Stadion Narodowy”,** a w bazie stadion nazywa się „PGE Narodowy”. Na K0, K1 i K3 trafiał więc w wypożyczalnie rowerów o tej nazwie (2687, 3154 i 2527 m). Na K2 dodał warunek `fclass = 'stadium'`, więc nie trafił nawet w wypożyczalnie i wynik był pusty. Żaden wynik nie był poprawny, a poprawna odległość to ok. 2,84 km.
4. **W H2 model zamienia „w pobliżu” na okrągły promień:** 1000 m bez informacji o sposobie poruszania się, 1000 m pieszo, 1500 m samochodem i 500 m dla „niedaleko”. Sposób poruszania się zmienia promień słabo.
5. **Wyniki nie są powtarzalne,** zwłaszcza przy mniejszych kontekstach i niejasnych pytaniach. W innym uruchomieniu wariant bez informacji o sposobie poruszania się dał 500 m zamiast 1000 m, więc każde pytanie trzeba zadać kilka razy.
6. **Pilotaż pokazał, że oba eksperymenty da się przeprowadzić.** Narzędzie generuje SQL na każdym poziomie kontekstu w ustalonym formacie, zapytania wykonują się na naszej bazie, a z wyników da się odczytać to, co chcemy mierzyć: poprawność wyniku w H1 i przyjęty promień w H2.
