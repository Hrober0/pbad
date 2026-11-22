-- M07: Jaka jest odległość w linii prostej w kilometrach między Parkiem Planeta Ursus
-- a Placem Bociani Zakątek?
-- Kolumna kluczowa: odległość (tolerancja 1%). Oba obiekty to parki w landuse.
WITH a AS (
    SELECT geom FROM gis_osm_landuse_a_free
    WHERE name = 'Park Planeta Ursus' AND fclass = 'park'
),
b AS (
    SELECT geom FROM gis_osm_landuse_a_free
    WHERE name = 'Plac Bociani Zakątek' AND fclass = 'park'
)
SELECT round((ST_Distance(a.geom::geography, b.geom::geography) / 1000)::numeric, 2) AS odleglosc_km
FROM a, b;
