-- J08: Wymień nazwy mostów samochodowych na Wiśle w Warszawie.
-- Kolumna kluczowa: name. Most = odcinek drogi z bridge = 'T' przecinający linię Wisły
-- w granicach Warszawy. „Samochodowy" wyklucza klasy pieszo-rowerowe; Most Świętokrzyski
-- ma odcinek tertiary i cycleway, więc filtr musi działać na poziomie odcinka.
WITH waw AS (
    SELECT geom FROM gis_osm_adminareas_a_free
    WHERE fclass = 'admin_level6' AND name = 'Warszawa'
),
wisla AS (
    SELECT geom FROM gis_osm_waterways_free
    WHERE fclass = 'river' AND name = 'Wisła'
)
SELECT DISTINCT r.name
FROM gis_osm_roads_free r, waw, wisla
WHERE r.bridge = 'T'
  AND r.name <> ''
  AND r.fclass NOT IN ('cycleway', 'footway', 'path', 'steps', 'pedestrian', 'track')
  AND ST_Intersects(r.geom, wisla.geom)
  AND ST_Intersects(r.geom, waw.geom)
ORDER BY r.name;
