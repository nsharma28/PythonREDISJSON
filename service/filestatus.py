import json
import os
from common.MyConvert import MyConvert
from models.samplemodel import *
from common.rdb_dal.sql import Sql
from configs import sql_query

class FileReadStatus:
    def __init__(self):
        self.last_proccesed_file = {}
        
    def getLastReadFile(self, mls_type:mlsType):
        sql = Sql('default')
        return sql.execute_value(sql_query.lastread_get_query, MyConvert.to_dict(mls_type))
    
    def insertLastReadFile(self,connecton_obj, lastreadfilemodel:lastReadFile):
        sql = Sql('default')
        return sql.execute(connecton_obj,sql_query.lastread_insert_query,MyConvert.to_dict(lastreadfilemodel))
    