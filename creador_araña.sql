DROP TABLE IF EXISTS "{esquema_placa}"."araña";

CREATE TABLE "{esquema_placa}"."araña" AS
SELECT 
    ST_MakeLine(
        p.geom::geometry(Point, 4326), 
        ST_ClosestPoint(f.geom, p.geom)
    )::geometry(LineString, 4326) AS geom
FROM "{esquema_placa}"."{capa_placa}" p
JOIN "{esquema_mavvial}"."{capa_mavvial}" f
  ON p."{campo_llave_placa}" = f."{campo_llave_mavvial}";
  
  
create index idx_geom_araña on "{esquema_placa}"."araña" using gist (geom);
