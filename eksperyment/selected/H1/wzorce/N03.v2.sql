-- WARIANT DOPUSZCZALNY N03.v2: bez filtra nazwy (A9)
-- N03: Jak daleko w metrach jest najbliższy urząd pocztowy od Dworca Centralnego
-- i jak się nazywa?
-- Kolumny kluczowe: name, odległość (tolerancja 1%). 'post_office', nie 'post_box'.
WITH dworzec AS (
    SELECT geom FROM gis_osm_transport_free
    WHERE fclass = 'railway_station' AND name = 'Warszawa Centralna'
),
poczty AS (
    SELECT name, geom FROM gis_osm_pois_free WHERE fclass = 'post_office'
    UNION ALL
    SELECT name, geom FROM gis_osm_pois_a_free WHERE fclass = 'post_office'
)
SELECT poczty.name, round(ST_Distance(poczty.geom::geography, dworzec.geom::geography)) AS odleglosc_m
FROM poczty, dworzec
ORDER BY odleglosc_m
LIMIT 1;
