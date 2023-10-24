import logging,uuid,json,sys
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timezone
from multipledispatch import dispatch
import sentry_sdk,traceback
from common.MyConvert import MyConvert
from common.config_param import config_dict as config_dict
from common.rdb_dal.sql import Sql

configDict = MyConvert.to_dict(config_dict.get("log"))

try:
    log_path = MyConvert.to_string(configDict.get("logPath"))
    logger_name = MyConvert.to_string(configDict.get("loggerName"))
    log_format = MyConvert.to_string(configDict.get("logFormat"))
    log_level = logging.INFO
    when = MyConvert.to_string(configDict.get("logFilehandlertime"))
    log_interval = MyConvert.to_int(configDict.get("logInterval"))
    backup_count = MyConvert.to_int(configDict.get("backupCount"))
    logging.basicConfig(level=log_level)
    logger_instance = logging.getLogger(logger_name)
    logger_instance_file_handler = TimedRotatingFileHandler(
        log_path,
        when=when,
        interval=log_interval,
        backupCount=backup_count,
    )
    logger_instance.setLevel(log_level)
    logger_instance_file_handler.setFormatter(Formatter(log_format))
    logger_instance.addHandler(logger_instance_file_handler)
except Exception as e:
    print(e)   
class Log:
    def __init__(self):
        self.enable_write_info=MyConvert.to_bool(configDict.get("enableWriteInfo"))
        self.enable_write_error=MyConvert.to_bool(configDict.get("enableWriteError"))
        self.enable_insert_error=MyConvert.to_bool(configDict.get("enableInsertError"))
        self.sentry_enable=MyConvert.to_bool(MyConvert.to_dict(configDict.get("sentry")).get("enable"))
        self.sentry_dsn=MyConvert.to_string(MyConvert.to_dict(configDict.get("sentry")).get("dsn"))
        self.sentry_environment=MyConvert.to_string(MyConvert.to_dict(configDict.get("sentry")).get("environment"))
        self.sentry_release=MyConvert.to_string(MyConvert.to_dict(configDict.get("sentry")).get("release"))
        self.sql_instance = Sql('errorLog')
    @dispatch(str)
    def write(self, message):
        try:
            if self.enable_write_info:
                logger_instance.info(message)
        except Exception as ex:
            print(ex)
    @dispatch(Exception)
    def write(self, exceptions):
        errorId = ""
        try:
            exception = "".join(traceback.format_exception(type(
                exceptions).__name__, exceptions, exceptions.__traceback__)).replace("\n", "")
            errorId = self.sentry_report_log(exceptions)
            if not errorId:
                errorId = str(uuid.uuid4())
            if self.enable_write_error:
                final_exception=str(sys.exc_info()[1]) +  ": " + exception
                logger_instance.error(final_exception)
            if self.enable_insert_error:
                self.insert_error_log(errorId, exception)
        except Exception as ex:
            print(ex)
        return errorId
    def sentry_report_log(self, exception):
        print("writeing Log in sentry")
        if self.sentry_enable:
           sentry_sdk.init(
                self.sentry_dsn,
                environment=self.sentry_environment,
                release=self.sentry_release
           )
           return sentry_sdk.capture_message(exception)
        return ""
    def insert_error_log(self, errorId, exception):
        if self.enable_insert_error:
            print("sql error id::",errorId)
            self.insert_data(errorId, exception)
        return errorId
    def insert_data(self, errorId, exception):
        sql_query = "insert into osm_master.dfe_error_reports(id,name,description,email,error,app_name,user_id,report_datetime) values(%(errorid)s,%(name)s,%(description)s,%(email)s,%(error)s,%(app_name)s,%(user_id)s,%(reportdatetime)s)"
        param_dict={
                "errorid":errorId,
                "name":"",
                "description":"",
                "email":"",
                "error":exception,
                "app_name":"",
                "user_id":0,
                "reportdatetime":datetime.utcnow()}
        self.sql_instance.execute(sql_query,param_dict)
        print("inserted exception in table successfully")
    @dispatch(str)
    async def write_async(self, message):
        try:
            if self.enable_write_info:
                logger_instance.info(message)
        except Exception as ex:
            print(ex)
    @dispatch(Exception)
    async def write_async(self, exception):
        print("in async function")
        errorId = ""
        try:
            exceptions = "".join(traceback.format_exception(type(
            exception).__name__, exception, exception.__traceback__)).replace("\n", "")
            errorId = self.sentry_report_log(exception)
            if not errorId:
                errorId = str(uuid.uuid4())
            if self.enable_write_error:
                final_exception=str(sys.exc_info()[1]) +  ": " + exceptions
                logger_instance.error(final_exception)
            if self.enable_insert_error:
                await self.insert_errorlog_async(errorId, exceptions)
        except Exception as ex:
            print(ex)
        return errorId
    async def insert_errorlog_async(self, errorId, exception):
            print("insert errorlog async called")
            self.insert_data(errorId, exception)
class ErrorEntity:
    def setdefaulvalue(self):
        id = 0
        errorid = ""
        name = ""
        description = ""
        email = ""
        error = ""
        userid = 0
        isreportbyuser = "false"
        createdatetime = datetime.now(timezone.utc)
        reportdatetime = datetime.now(timezone.utc)
    def __init__(self):
        self.setdefaulvalue()
