from pydantic import BaseModel
from fastapi_camelcase import CamelModel

class SampleModel(CamelModel,BaseModel):
    id:int = 0
    name:str = ''