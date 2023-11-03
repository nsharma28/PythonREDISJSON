from fastapi import status
import traceback
from common.logs.log import Log

class Response():

    @staticmethod
    def data(data):
        errorId =  ""
        exceptions = None
        return dict(errorId = errorId, exceptions = exceptions, data = data, status = status.HTTP_200_OK)

    @staticmethod
    def error(exceptions):
        log = Log()
        errorId =  log.write(exceptions)
        exceptions = "".join(traceback.format_exception(type(
            exceptions).__name__, exceptions, exceptions.__traceback__)).replace("\n", "")
        data = None
        return dict(errorId = errorId, exceptions = exceptions, data = data, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    async def error_async(exceptions):
        log = Log()
        errorId =  await log.write_async(exceptions)
        exceptions = "".join(traceback.format_exception(type(
            exceptions).__name__, exceptions, exceptions.__traceback__)).replace("\n", "")
        data = None
        return dict(errorId = errorId, exceptions = exceptions, data = data, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


    @staticmethod
    def unauthenticate():
        errorId =  ""
        exceptions = None
        data="Invalid token or expired token."
        return dict(errorId = errorId, exceptions = exceptions, data = data, status = status.HTTP_401_UNAUTHORIZED)


    @staticmethod
    def unauthorize():
        errorId =  ""
        exceptions = None
        data="User doesn't have permission to access this resource"
        return dict(errorId = errorId, exceptions = exceptions, data = data, status = status.HTTP_401_UNAUTHORIZED)
        
