-- N07: Wymień 3 przystanki autobusowe najbliższe pomnikowi pamięci Konstantego
-- Juliana Ordona i podaj, jak daleko są w metrach.
-- Kolumny kluczowe: name w kolejności, odległość (tolerancja 1%).
-- Pomnik w bazie: 'Pamięci Konstantego Juliana Ordona' (są też trzy „Reduta Ordona").
WITH pomnik AS (
    SELECT geom FROM gis_osm_pois_free
    WHERE fclass = 'memorial' AND name = 'Pamięci Konstantego Juliana Ordona'
),
przystanki AS (
    SELECT name, geom FROM gis_osm_transport_free WHERE fclass = 'bus_stop' AND name <> ''
    UNION ALL
    SELECT name, geom FROM gis_osm_transport_a_free WHERE fclass = 'bus_stop' AND name <> ''
)
SELECT przystanki.name, round(ST_Distance(przystanki.geom::geography, pomnik.geom::geography)) AS odleglosc_m
FROM przystanki, pomnik
ORDER BY odleglosc_m
LIMIT 3;
