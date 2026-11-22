-- J01: Które szkoły w Warszawie mają w promieniu 300 metrów co najmniej jeden fast food?
-- Kolumna kluczowa: name. Obie tabele dla obu warstw; name <> '' tylko dla szkół,
-- bo to one są wynikiem.
WITH waw AS (
    SELECT geom FROM gis_osm_adminareas_a_free
    WHERE fclass = 'admin_level6' AND name = 'Warszawa'
),
szkoly AS (
    SELECT osm_id, name, geom FROM gis_osm_pois_free WHERE fclass = 'school' AND name <> ''
    UNION ALL
    SELECT osm_id, name, geom FROM gis_osm_pois_a_free WHERE fclass = 'school' AND name <> ''
),
fastfoody AS (
    SELECT geom FROM gis_osm_pois_free WHERE fclass = 'fast_food'
    UNION ALL
    SELECT geom FROM gis_osm_pois_a_free WHERE fclass = 'fast_food'
)
SELECT DISTINCT s.name
FROM szkoly s, waw
WHERE ST_Intersects(s.geom, waw.geom)
  AND EXISTS (
      SELECT 1 FROM fastfoody f
      WHERE ST_DWithin(s.geom::geography, f.geom::geography, 300)
  )
ORDER BY s.name;
