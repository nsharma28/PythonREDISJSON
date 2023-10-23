from fastapi import Request, Response
import json
from fastapi_utils.inferring_router import InferringRouter
import os
from models.samplemodel import SampleModel
from service.dataservice import DataService



router = InferringRouter(prefix="/data")


class CityRouter:
    @router.post("/insert",tags=["raw/data"])
    async def get(request:Request):
            try:
                return Response.data(DataService.get())
            except Exception as ex:
                return Response.error(ex)
            
    @router.post("/insertsample",tags=["raw/data"])
    async def getsample(request:Request,SampleModel:SampleModel):
            try:
                return Response.data(DataService.insert(SampleModel))
            except Exception as ex:
                return Response.error(ex)