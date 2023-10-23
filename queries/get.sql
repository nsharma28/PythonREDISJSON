SELECT      c.id,
            c.name
FROM        master.property  AS c
WHERE       c.id IN (%(property_id)s)
    AND     c.is_active = True
ORDER BY    c.name
