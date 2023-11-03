from common.config_param import config_dict

class Sql():

    def __init__(self,key):
        
        config_params = config_dict['connections'][key]

        connection_string = config_params['connectionString']
        self.__provider = config_params['provider']

        if self.__provider  == 'postgresql':
            from common.rdb_dal.postgresql import PostgresSql
            __class = PostgresSql

        elif self.__provider  == 'mssql':
            from common.rdb_dal.mssql import SqlServer
            __class = SqlServer
        

        self.__instance = __class(connection_string)
        
    def open_connection(self):
        return self.__instance.open_connection()
    
    def start_transaction(self,connection_obj):
        self.__instance.start_transaction(connection_obj)
        
    def close_connection(self,connection_obj):
        self.__instance.close_connection(connection_obj)
    
    def commit_transaction(self,connection_obj):
        self.__instance.commit_transaction(connection_obj)
    
    def rollback_transaction(self,connection_obj):
        self.__instance.rollback_transaction(connection_obj)

    def execute(self,connection_obj,query,param_dict =None):
        """ Execute DML Commands  
            Query      ->   INSERT INTO TABLE_NAME (column_1,column_2...[n]) 
                            VALUES (%(key_name_1)s, %(key_name_2)s)
            param_dict - >  {"key_name_1": value ,"key_name_1": value }
                
        Args:
            query (String)          : Sql query to execute
            param_dict (Dictonery)  : If Query do have parameters then it contain the key and its associate value.Defaults to None

        Returns:
            [int]: Return 0 if successfully executed the query
        """

        if param_dict != None and self.__provider in ['trino'] and isinstance(param_dict,dict):
            query,param_dict = self.create_sql_query_param_for_trino(query,param_dict)

        return  self.__instance.execute(connection_obj,query,param_dict)
    
    def execute_batch(self,connection_obj,query,param_dict =None):
        """ Execute DML Commands in batch for faster insert 
            Query      ->   INSERT INTO TABLE_NAME (column_1,column_2...[n]) 
                            VALUES (%(key_name_1)s, %(key_name_2)s)
            param_dict - >  {"key_name_1": value ,"key_name_1": value }
                
        Args:
            query (String)          : Sql query to execute
            param_dict (Dictonery)  : If Query do have parameters then it contain the key and its associate value.Defaults to None

        Returns:
            [int]: Return 0 if successfully executed the query
        """

        if param_dict != None and self.__provider in ['trino'] and isinstance(param_dict,dict):
            query,param_dict = self.create_sql_query_param_for_trino(query,param_dict)
            
        #connection_obj = self.__instance.open_connection()

        return  self.__instance.execute_batch(connection_obj,query,param_dict)

    def execute_value(self,query,param_dict = None):
        """ Execute a SQL Command and  returns a single row of data from the database.
            Example:
                Query  -> SELECT COUNT(*) FROM TABLE_NAME
                Output -> [{"count" : value}]

                Query  -> SELECT max(price) FROM TABLE_NAME
                Output -> [{"max" : value}]

        Args:
            query (String)          : Sql query to execute
            param_dict (Dictonery)  : If Query do have parameters then it contain the key and its associate value. Defaults to None.

        Returns:
            [Any]: Single value of any datatype
        """
        if param_dict != None and self.__provider in ['trino'] and isinstance(param_dict,dict):
            query,param_dict = self.create_sql_query_param_for_trino(query,param_dict)

        return self.__instance.execute_value(query,param_dict)
        

    def execute_record(self,model_type,query,param_dict = None):
        """ Execute SQL Command and  return  single raw data from the database.

            Example:      
                Query      -> SELECT ID FROM TABLE_NAME WHERE capacity = %"(capacity)"s
                param_dict -> {"capacity": value ,"name": value }
    
        Args:
            model_type(class)       : BaseModel type for the services
            query (String)          : Sql query to execute
            param_dict (Dictonery)  : If Query do have parameters then it contain the key and its associate value. Defaults to None.

        Returns:
            [List] : List of object[model_type]
        """
        if param_dict != None and self.__provider in ['trino'] and isinstance(param_dict,dict):
            query,param_dict = self.create_sql_query_param_for_trino(query,param_dict)

        return self.__instance.execute_record(query,param_dict,model_type)

    def execute_list(self,model_type,query,param_dict = None):
        """Execute a SQL Command and  returns a set of rows from the database

        Args:
            model_type(class)       : BaseModel type for the services
            query (String)          : Sql query to execute
            param_dict (Dictonery)  : If Query do have parameters then it contain the key and its associate value. Defaults to None.

        Returns:
            [List] : List of object[model_type]
        """
        if param_dict != None and self.__provider in ['trino'] and isinstance(param_dict,dict):
            query,param_dict = self.create_sql_query_param_for_trino(query,param_dict)

        return self.__instance.execute_list(query,param_dict,model_type)
    
    def create_sql_query_param_for_trino(self,query,param_dict):
        """_summary_

        Args:
            sql_query (_type_): _description_
            param (_type_): _description_

        Returns:
            _type_: _description_
        """
        #Replace key been defined in params dict with its values in query string
        for x in param_dict.keys():
            query = query.replace(f'%({x})s',str(param_dict[x]))

        #Static value defined
        #!Note : param_dict has not required anymore and defined as None
        param_dict = None 
        return query,param_dict
