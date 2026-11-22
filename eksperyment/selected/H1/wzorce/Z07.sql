-- Z07: Ile supermarketów jest w Warszawie?
-- Kolumna kluczowa: liczba. Granica tylko admin_level6 — bez fclass wynik rośnie trzykrotnie.
WITH waw AS (
    SELECT geom FROM gis_osm_adminareas_a_free
    WHERE fclass = 'admin_level6' AND name = 'Warszawa'
),
sklepy AS (
    SELECT osm_id, geom FROM gis_osm_pois_free WHERE fclass = 'supermarket'
    UNION ALL
    SELECT osm_id, geom FROM gis_osm_pois_a_free WHERE fclass = 'supermarket'
)
SELECT count(DISTINCT sklepy.osm_id) AS liczba_supermarketow
FROM sklepy, waw
WHERE ST_Intersects(sklepy.geom, waw.geom);
