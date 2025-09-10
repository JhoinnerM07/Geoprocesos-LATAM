update "{esquema_mavvial}"."{capa_mavvial}"
SET generadora = null;

WITH generadoras_contadas AS (
  SELECT
    id_mavvial,
    generadora,
    COUNT(*) AS cantidad
  FROM "{esquema_placa}"."{capa_placa}"
  WHERE generadora ~ '^\d+$'
  GROUP BY id_mavvial, generadora
),
modas_filtradas AS (
  SELECT DISTINCT ON (id_mavvial)
    id_mavvial,
    generadora::integer AS generadora_moda
  FROM generadoras_contadas
  WHERE cantidad >= 3
  ORDER BY id_mavvial, cantidad DESC,  -- más repeticiones primero
           CASE WHEN generadora = '0' THEN -1 ELSE generadora::integer END DESC
),
updateable AS (
  SELECT
    m.id_capa,
    f.generadora_moda
  FROM "{esquema_mavvial}"."{capa_mavvial}" m
  JOIN modas_filtradas f ON m.id_capa = f.id_mavvial
)
UPDATE "{esquema_mavvial}"."{capa_mavvial}" m
SET generadora = u.generadora_moda::text
FROM updateable u
WHERE m.id_capa = u.id_capa;
