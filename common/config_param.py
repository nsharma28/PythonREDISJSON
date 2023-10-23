from common.MyConvert import MyConvert
import json 
try:
    config_dict=MyConvert.to_dict(json.load(open("config/config.json")))
except Exception as exception:
    config_dict={}
configLog = MyConvert.to_dict(config_dict.get("log"))
conn_string = MyConvert.to_dict(MyConvert.to_dict(config_dict.get("connections")).get("loginUserRedis")).get("connectionString")
database = MyConvert.to_dict(MyConvert.to_dict(config_dict.get("connections")).get("loginUserRedis")).get("provider")
ignoreToken = MyConvert.to_bool(config_dict.get("ignoreToken"))
