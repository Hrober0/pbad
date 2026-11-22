-- A03: Które 5 stacji kolejowych i metra w Warszawie ma najwięcej restauracji
-- w promieniu 500 metrów i ile ich jest?
-- Kolumny kluczowe: name w kolejności, liczba. 'railway_station' (obejmuje metro),
-- nie 'railway_halt'. Na 5. miejscu jest remis 39-39, więc wzorzec wypisuje 6 wierszy.
WITH waw AS (
    SELECT geom FROM gis_osm_adminareas_a_free
    WHERE fclass = 'admin_level6' AND name = 'Warszawa'
),
stacje AS (
    SELECT t.osm_id, t.name, t.geom
    FROM gis_osm_transport_free t, waw
    WHERE t.fclass = 'railway_station' AND t.name <> ''
      AND ST_Intersects(t.geom, waw.geom)
),
restauracje AS (
    SELECT osm_id, geom FROM gis_osm_pois_free WHERE fclass = 'restaurant'
    UNION ALL
    SELECT osm_id, geom FROM gis_osm_pois_a_free WHERE fclass = 'restaurant'
)
SELECT s.name, count(DISTINCT r.osm_id) AS liczba_restauracji
FROM stacje s
LEFT JOIN restauracje r ON ST_DWithin(r.geom::geography, s.geom::geography, 500)
GROUP BY s.name
ORDER BY liczba_restauracji DESC, s.name
LIMIT 6;
