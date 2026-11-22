-- A08: Ile wypożyczalni rowerów w Warszawie jest w promieniu 300 metrów od stacji
-- kolejowej lub metra, a ile dalej?
-- Kolumny kluczowe: kategoria, liczba. 'railway_station' obejmuje też metro.
WITH waw AS (
    SELECT geom FROM gis_osm_adminareas_a_free
    WHERE fclass = 'admin_level6' AND name = 'Warszawa'
),
stacje AS (
    SELECT geom FROM gis_osm_transport_free WHERE fclass = 'railway_station'
),
rowery AS (
    SELECT osm_id, geom FROM gis_osm_pois_free WHERE fclass = 'bicycle_rental'
    UNION ALL
    SELECT osm_id, geom FROM gis_osm_pois_a_free WHERE fclass = 'bicycle_rental'
)
SELECT CASE WHEN EXISTS (
           SELECT 1 FROM stacje s
           WHERE ST_DWithin(r.geom::geography, s.geom::geography, 300)
       ) THEN 'do 300 m' ELSE 'dalej' END AS kategoria,
       count(DISTINCT r.osm_id) AS liczba
FROM rowery r, waw
WHERE ST_Intersects(r.geom, waw.geom)
GROUP BY 1
ORDER BY 1;
