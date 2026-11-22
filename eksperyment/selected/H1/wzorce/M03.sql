-- M03: Jaka jest odległość w linii prostej w metrach między Pałacem Kultury i Nauki
-- a Stadionem Narodowym?
-- Kolumna kluczowa: odległość (tolerancja 1%). Stadion to 'PGE Narodowy' w pois_a,
-- a nie stacja kolejowa o nazwie 'Stadion Narodowy'. Odległość między obrysami.
WITH pkin AS (
    SELECT geom FROM gis_osm_pois_a_free
    WHERE name = 'Pałac Kultury i Nauki' AND fclass = 'attraction'
),
stadion AS (
    SELECT geom FROM gis_osm_pois_a_free
    WHERE name = 'PGE Narodowy' AND fclass = 'stadium'
)
SELECT round(ST_Distance(pkin.geom::geography, stadion.geom::geography)) AS odleglosc_m
FROM pkin, stadion;
