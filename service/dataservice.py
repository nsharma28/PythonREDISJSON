from models.samplemodel import *
from common.rdb_dal.sql import Sql
from config import sql_query
from common.MyConvert import *


class DataService:
    def get(searchModel:searchModel())->list[SampleModel]:
        sql = Sql('default')
        return sql.execute_list(SampleModel,sql_query.property_get_by_id_query, MyConvert.to_dict(searchModel))
    
    
    def insert(SampleModel:SampleModel()):
        sql = Sql('default')
        return sql.execute(sql_query.propert_insert_query, MyConvert.to_dict(SampleModel))
