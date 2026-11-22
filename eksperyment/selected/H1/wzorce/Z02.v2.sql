-- WARIANT DOPUSZCZALNY Z02.v2: środek budynku dworca
-- Z02: Wymień nazwy kawiarni w promieniu 300 metrów od Dworca Centralnego.
-- Kolumna kluczowa: name (zbiór, bez znaczenia kolejności).
-- Ustalenia: obiekt odniesienia = punkt stacji 'Warszawa Centralna' z gis_osm_transport_free
-- (wariant dopuszczalny: poligon budynku o tej samej nazwie z gis_osm_buildings_a_free),
-- kawiarnie z obu tabel pois, name <> '' bo nazwy są wynikiem, odległość na geography.
WITH ref AS (
    SELECT geom FROM gis_osm_buildings_a_free
    WHERE name = 'Warszawa Centralna'
),
cafe AS (
    SELECT osm_id, name, geom FROM gis_osm_pois_free
    WHERE fclass = 'cafe' AND name <> ''
    UNION ALL
    SELECT osm_id, name, geom FROM gis_osm_pois_a_free
    WHERE fclass = 'cafe' AND name <> ''
)
SELECT DISTINCT cafe.name
FROM cafe, ref
WHERE ST_DWithin(cafe.geom::geography, ST_Centroid(ref.geom)::geography, 300)
ORDER BY cafe.name;
