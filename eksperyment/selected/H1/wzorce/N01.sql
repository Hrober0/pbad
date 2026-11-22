-- N01: Jaki szpital jest najbliżej Pałacu Kultury i Nauki?
-- Kolumna kluczowa: name. Szpitale z obu tabel pois, nazwy są wynikiem, więc name <> ''.
WITH pkin AS (
    SELECT geom FROM gis_osm_pois_a_free
    WHERE name = 'Pałac Kultury i Nauki' AND fclass = 'attraction'
),
szpitale AS (
    SELECT name, geom FROM gis_osm_pois_free WHERE fclass = 'hospital' AND name <> ''
    UNION ALL
    SELECT name, geom FROM gis_osm_pois_a_free WHERE fclass = 'hospital' AND name <> ''
)
SELECT szpitale.name, round(ST_Distance(szpitale.geom::geography, pkin.geom::geography)) AS odleglosc_m
FROM szpitale, pkin
ORDER BY odleglosc_m
LIMIT 1;
