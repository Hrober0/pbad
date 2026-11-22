-- M02: Ile kilometrów ma ulica Marszałkowska w Warszawie?
-- Kolumna kluczowa: długość (tolerancja 1%). Bez zawężenia do Warszawy wychodzi
-- 9,90 km, bo ulice o tej nazwie są też w innych miejscowościach województwa.
WITH waw AS (
    SELECT geom FROM gis_osm_adminareas_a_free
    WHERE fclass = 'admin_level6' AND name = 'Warszawa'
)
SELECT round((ST_Length(ST_Union(ST_Intersection(r.geom, waw.geom))::geography) / 1000)::numeric, 2)
       AS dlugosc_km
FROM gis_osm_roads_free r, waw
WHERE r.name = 'Marszałkowska'
  AND ST_Intersects(r.geom, waw.geom);
