from fastapi import Request, Response
import json
from fastapi_utils.inferring_router import InferringRouter
import os
from models.samplemodel import *
from service.dataservice import DataService
from common.Response import *



router = InferringRouter(prefix="/data")


class CityRouter:
    @router.post("/get",tags=["raw/data"])
    async def get(request:Request, searchModel:searchModel):
            try:
                return Response.data(DataService.get(searchModel))
            except Exception as ex:
                return Response.error(ex)
            
    @router.post("/insertsample",tags=["raw/data"])
    async def insertsample(request:Request,SampleModel:SampleModel):
            try:
                return Response.data(DataService.insert(SampleModel))
            except Exception as ex:
                return Response.error(ex)
            
    @router.post("/insertmls",tags=["raw/data"])
    async def insertmls(request:Request,mlsType:mlsType):
            try:
                return Response.data(DataService.insertData(mlsType))
            except Exception as ex:
                return Response.error(ex)
