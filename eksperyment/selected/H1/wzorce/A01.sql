-- A01: Ile jest restauracji, kawiarni, fast foodów, pubów i barów w promieniu kilometra
-- od Pałacu Kultury i Nauki? Podaj liczbę dla każdego typu osobno.
-- Kolumny kluczowe: typ, liczba. Wszystkie pięć wartości fclass, obie tabele pois.
WITH pkin AS (
    SELECT geom FROM gis_osm_pois_a_free
    WHERE name = 'Pałac Kultury i Nauki' AND fclass = 'attraction'
),
lokale AS (
    SELECT osm_id, fclass, geom FROM gis_osm_pois_free
    WHERE fclass IN ('restaurant', 'cafe', 'fast_food', 'pub', 'bar')
    UNION ALL
    SELECT osm_id, fclass, geom FROM gis_osm_pois_a_free
    WHERE fclass IN ('restaurant', 'cafe', 'fast_food', 'pub', 'bar')
)
SELECT lokale.fclass, count(DISTINCT lokale.osm_id) AS liczba
FROM lokale, pkin
WHERE ST_DWithin(lokale.geom::geography, pkin.geom::geography, 1000)
GROUP BY lokale.fclass
ORDER BY lokale.fclass;
