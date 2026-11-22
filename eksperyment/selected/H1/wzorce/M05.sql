-- M05: Ile kilometrów długości ma Wisła na odcinku w granicach Warszawy?
-- Kolumna kluczowa: długość (tolerancja 1%). Wisła to 28 odcinków linii w województwie
-- (380,1 km); liczymy tylko część przyciętą do granicy miasta. Poligonów koryta
-- (fclass 'riverbank') nie używamy, bo to obszar, a nie długość.
WITH waw AS (
    SELECT geom FROM gis_osm_adminareas_a_free
    WHERE fclass = 'admin_level6' AND name = 'Warszawa'
)
SELECT round((ST_Length(ST_Union(ST_Intersection(w.geom, waw.geom))::geography) / 1000)::numeric, 2)
       AS dlugosc_km
FROM gis_osm_waterways_free w, waw
WHERE w.fclass = 'river' AND w.name = 'Wisła'
  AND ST_Intersects(w.geom, waw.geom);
