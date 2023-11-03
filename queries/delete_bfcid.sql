delete from dbt_source.property_ptnf
where BFCID = any (%s);