SELECT      c.id,
            c.name
FROM        osm_master.propert  AS c
WHERE       c.id IN %(property_id)s)
    AND     c.is_active = True
ORDER BY    c.name