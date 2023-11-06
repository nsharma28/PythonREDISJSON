from typing import List
from pydantic import BaseModel
from fastapi_camelcase import CamelModel

class SampleModel(CamelModel,BaseModel):
    id:int = 0
    name:str = ''
    is_active:bool = 1
    
class searchModel(CamelModel,BaseModel):
    property_id:str = ''
    
class mlsType(CamelModel,BaseModel):
    mls_name:str = ''
    
class lastReadFile(CamelModel,BaseModel):
    mls_name:str = ''
    file_name:str = ''
    file_timestamp:str = ''
    
class deleteModel(CamelModel,BaseModel):
    bfcid_array:List[str]
    
class dataStatsModel(CamelModel,BaseModel):
    totalRecordsProcessed: int = 0
    totalMissingLatLongRecords: int = 0
    totalErrorRecords: int = 0
