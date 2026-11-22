-- Z05: Ile aptek jest w promieniu kilometra od Skweru Jolanty Brzeskiej?
-- Kolumna kluczowa: liczba. Skwer jest parkiem w landuse (ten sam osm_id powtórzony w pois_a).
WITH skwer AS (
    SELECT geom FROM gis_osm_landuse_a_free
    WHERE name = 'Skwer Jolanty Brzeskiej' AND fclass = 'park'
),
apteki AS (
    SELECT osm_id, geom FROM gis_osm_pois_free WHERE fclass = 'pharmacy'
    UNION ALL
    SELECT osm_id, geom FROM gis_osm_pois_a_free WHERE fclass = 'pharmacy'
)
SELECT count(DISTINCT apteki.osm_id) AS liczba_aptek
FROM apteki, skwer
WHERE ST_DWithin(apteki.geom::geography, skwer.geom::geography, 1000);
