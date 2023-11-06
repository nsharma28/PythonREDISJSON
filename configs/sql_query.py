__property_get_file = open("queries/get.sql", 'r')
property_get_by_id_query = __property_get_file.read()
__property_get_file.close()

__insert_file = open("queries/insert.sql", 'r')
insert_query = __insert_file.read()
__insert_file.close()

__property_insert_file = open("queries/insert_properties.sql", 'r')
property_insert_query = __property_insert_file.read()
__property_insert_file.close()

__feature_insert_file = open("queries/insert_feature.sql", 'r')
feature_insert_query = __feature_insert_file.read()
__feature_insert_file.close()

__lastread_insert_file = open("queries/insert_lastreadfile.sql", 'r')
lastread_insert_query = __lastread_insert_file.read()
__lastread_insert_file.close()

__lastread_get_file = open("queries/get_lastreadfile.sql", 'r')
lastread_get_query = __lastread_get_file.read()
__lastread_get_file.close()

__bcfid_delete_file = open("queries/delete_bfcid.sql", 'r')
bcfid_delete_query = __bcfid_delete_file.read()
__bcfid_delete_file.close()

_media_insert_file = open("queries/insert_media.sql", 'r')
media_insert_query = _media_insert_file.read()
_media_insert_file.close()

__user_insert_file = open("queries/insert_user.sql", 'r')
user_insert_query = __user_insert_file.read()
__user_insert_file.close()

__openhouse_insert_file = open("queries/insert_openhouse.sql", 'r')
openhouse_insert_query = __openhouse_insert_file.read()
__openhouse_insert_file.close()
