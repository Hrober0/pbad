-- J05: Wymień nazwy budynków stojących na terenie Łazienek Królewskich.
-- Kolumna kluczowa: name (zbiór). Łazienki to park w landuse, powtórzony z tym samym
-- osm_id w pois_a — obie drogi dają ten sam wynik. ST_Within i ST_Intersects też
-- dają tu tyle samo, bo budynki leżą w całości wewnątrz parku.
WITH lazienki AS (
    SELECT geom FROM gis_osm_landuse_a_free
    WHERE name = 'Łazienki Królewskie' AND fclass = 'park'
)
SELECT DISTINCT b.name
FROM gis_osm_buildings_a_free b, lazienki
WHERE ST_Intersects(b.geom, lazienki.geom)
  AND b.name <> ''
ORDER BY b.name;
