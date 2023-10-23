from pydantic import BaseModel
from fastapi_camelcase import CamelModel

class SampleModel(CamelModel,BaseModel):
    id:int = 0
    name:str = ''
    is_active:bool = 1
    
class searchModel(CamelModel,BaseModel):
    property_id:str = ''
