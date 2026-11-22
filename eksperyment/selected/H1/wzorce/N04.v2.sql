-- WARIANT DOPUSZCZALNY N04.v2: środek zamku
-- N04: Wymień 5 aptek położonych najbliżej Zamku Królewskiego.
-- Kolumna kluczowa: name w kolejności. Zamek to poligon 'castle' w pois_a — sama nazwa
-- bez fclass trafia w sklepy z pamiątkami i w muzeum.
WITH zamek AS (
    SELECT geom FROM gis_osm_pois_a_free
    WHERE name = 'Zamek Królewski' AND fclass = 'castle'
),
apteki AS (
    SELECT name, geom FROM gis_osm_pois_free WHERE fclass = 'pharmacy' AND name <> ''
    UNION ALL
    SELECT name, geom FROM gis_osm_pois_a_free WHERE fclass = 'pharmacy' AND name <> ''
)
SELECT apteki.name, round(ST_Distance(apteki.geom::geography, ST_Centroid(zamek.geom)::geography)) AS odleglosc_m
FROM apteki, zamek
ORDER BY odleglosc_m
LIMIT 5;
