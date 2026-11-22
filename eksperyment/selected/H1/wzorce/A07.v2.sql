-- WARIANT DOPUSZCZALNY A07.v2: punkt wewnątrz placu (ST_PointOnSurface)
-- A07: Ile szkół, a ile przedszkoli jest w promieniu kilometra od Placu Bociani Zakątek?
-- Kolumny kluczowe: typ, liczba. Plac to park w landuse.
WITH plac AS (
    SELECT geom FROM gis_osm_landuse_a_free
    WHERE name = 'Plac Bociani Zakątek' AND fclass = 'park'
),
obiekty AS (
    SELECT osm_id, fclass, geom FROM gis_osm_pois_free
    WHERE fclass IN ('school', 'kindergarten')
    UNION ALL
    SELECT osm_id, fclass, geom FROM gis_osm_pois_a_free
    WHERE fclass IN ('school', 'kindergarten')
)
SELECT obiekty.fclass, count(DISTINCT obiekty.osm_id) AS liczba
FROM obiekty, plac
WHERE ST_DWithin(obiekty.geom::geography, ST_PointOnSurface(plac.geom)::geography, 1000)
GROUP BY obiekty.fclass
ORDER BY obiekty.fclass;
