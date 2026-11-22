-- Z01: Ile aptek jest w promieniu 500 metrów od Pałacu Kultury i Nauki?
-- Kolumna kluczowa: liczba. Obiekt odniesienia: poligon 'attraction' (wariant: obrys budynku, ten sam wynik).
WITH pkin AS (
    SELECT geom FROM gis_osm_pois_a_free
    WHERE name = 'Pałac Kultury i Nauki' AND fclass = 'attraction'
),
apteki AS (
    SELECT osm_id, geom FROM gis_osm_pois_free WHERE fclass = 'pharmacy'
    UNION ALL
    SELECT osm_id, geom FROM gis_osm_pois_a_free WHERE fclass = 'pharmacy'
)
SELECT count(DISTINCT apteki.osm_id) AS liczba_aptek
FROM apteki, pkin
WHERE ST_DWithin(apteki.geom::geography, pkin.geom::geography, 500);
