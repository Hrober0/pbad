-- J02: Ile przedszkoli w Warszawie nie ma żadnego parku w promieniu 500 metrów?
-- Kolumna kluczowa: liczba. Parki tylko z landuse (zasada A4), przedszkola z obu tabel,
-- bez filtra po nazwie, bo liczymy, a nie wypisujemy.
WITH waw AS (
    SELECT geom FROM gis_osm_adminareas_a_free
    WHERE fclass = 'admin_level6' AND name = 'Warszawa'
),
przedszkola AS (
    SELECT osm_id, geom FROM gis_osm_pois_free WHERE fclass = 'kindergarten'
    UNION ALL
    SELECT osm_id, geom FROM gis_osm_pois_a_free WHERE fclass = 'kindergarten'
)
SELECT count(DISTINCT p.osm_id) AS liczba_przedszkoli
FROM przedszkola p, waw
WHERE ST_Intersects(p.geom, waw.geom)
  AND NOT EXISTS (
      SELECT 1 FROM gis_osm_landuse_a_free park
      WHERE park.fclass = 'park'
        AND ST_DWithin(p.geom::geography, park.geom::geography, 500)
  );
