SELECT      
            c.file_timestamp
FROM        dbt_source.filefeedstore_ptnf  AS c
WHERE       c.mls_name IN (%(mls_name)s)
ORDER BY    c.id DESC
LIMIT 1