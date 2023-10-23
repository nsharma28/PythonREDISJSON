__property_get_file = open("queries/get.sql", 'r')
property_get_by_id_query = __property_get_file.read()
__property_get_file.close()

__propert_insert_file = open("queries/insert.sql", 'r')
propert_insert_query = __propert_insert_file.read()
__propert_insert_file.close()