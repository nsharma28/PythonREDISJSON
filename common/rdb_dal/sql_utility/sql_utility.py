# Relative import 
from common.rdb_dal.common_utility.common_functions import *

# Library Import
from abc import ABC, abstractmethod


class SqlAbstract(ABC):
    
    @abstractmethod
    def open_connection(): pass
    
    @abstractmethod
    def close_connection(): pass
    
    @abstractmethod
    def execute(): pass

    @abstractmethod
    def execute_value(): pass 

    @abstractmethod
    def execute_record(): pass 

    @abstractmethod
    def execute_list(): pass 


class SqlUtility(SqlAbstract):
    
    def __init__(self,provider = None) :
        self.__provider = provider

    def close_connection(self,connection_obj):
        """Close the sources connection

        Args:
            connection_obj (Object): sources connection object

        Raises:
            CloseConnectionError: Raise when connection is not closed or giving error due to any reasons

        Returns:
            [string]: If Exception is raise then return string message else Nothing will return
        """
        connection_obj.close()     
    
    def execute(self,query_string,param_dict):
        """ Execute SQL Command  Update , Insert or Delete operations. It doesn't return any data from the database.

        Args:
            query_string (String)   : SQL query 
            param_dict (Dictonery)  : If Query do have parameters then it contain the key and its associate value

        Raises:
            QueryExecutionError: Raise when it failed to execute the query

        Returns:
            [string| Integer]: If Exception is raise then return string message else return 0 for successfully function run
        """
        try:
            connection_obj = self.open_connection()
            return execute_dml(connection_obj,query_string,param_dict)
        finally:
            self.close_connection(connection_obj)
    

    def execute_value(self,query_string,param_dict):
        """ Execute a SQL Command and  returns a single value from the database.

        Args:
            query_string (String)   : Sql query
            param_dict (Dictonery)  : If Query do have parameters then it contain the key and its associate value

        Raises:
            QueryOutputEmpty     : Raise when query return nothing
            QueryExecutionFailed : Raise when query failed to execute 

        Returns:
            [ANY]: It can return any type of value depending upon the query
        """
        try:
            connection_obj = self.open_connection()
            result = retrieve_sql_database_record(connection_obj,query_string,param_dict)
            if len(result) > 0 : 
                return  result
        finally:
            self.close_connection(connection_obj)
        
    def execute_record(self,query_string,param_dict,model_type):
        """ Execute a SQL Command that  return  single raw  values from the database

        Args:
            query_string (String)   : SQL query
            param_dict (Dictonery)  : If Query do have parameters then it contain the key and its associate value
            model_type(class)       : BaseModel type for the services

        Raises:
            InsertExecutionError: Raise when query failed for any reasons

        Returns:
            [List] : List of object[model_type]
        """
        try:
            connection_obj = self.open_connection()
            return retrieve_sql_database_record(
                connection_obj, query_string, param_dict, model_type=model_type
            )
        finally:
            self.close_connection(connection_obj)

    
    def execute_list(self,query_string,param_dict,model_type):
        """ Execute a SQL Command and  returns a set of rows from the database.

        Args:
            query_string (String)   : SQL query
            param_dict (Dictonery)  : If Query do have parameters then it contain the key and its associate value
            model_type(class)       : BaseModel type for the services

        Raises:
            QueryExecutionError       : Raise when it failed to execute the query
            ResultDataConversionError : Raise when data conversion failed

        Returns:
            [List] : List of object[model_type]
        """
        try:
            connection_obj = self.open_connection()
            return retrieve_sql_database_record(
                connection_obj, query_string, param_dict, model_type=model_type
            )
        finally:
            self.close_connection(connection_obj)

