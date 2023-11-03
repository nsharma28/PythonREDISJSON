

def retrieve_sql_database_record(connection_obj,query_string,param_dict,model_type = None):
    """ Execute the SQL COMMAND and convert the row data as  LIST ->  DataFrame 

    Args:
        connection_obj (Object) :  Trino connection object
        query_string (String)   : Sql query to execute
        param_dict (Dictonery)  : If Query do have parameters then it contain the key and its associate value
        model_type(class)       : BaseModel type for the services.By default None


    Returns:
        [List] : List of object[model_type]
    """
    
    cursor = connection_obj.cursor() # Open the cursor.
    if param_dict is None:
        cursor.execute(query_string) # Execute command 
    else:
        cursor.execute(query_string,param_dict) # Execute command 

    # Get the column name from description 
    column_name = [x[0] for x in cursor.description]
    query_data = []
    while True:
        data = cursor.fetchone() # Return single query
        if data is None:
            break

        if model_type is None:
            query_data.append(
                {
                    column: data[index]
                    for index, column in enumerate(column_name)
                }
            )
        else:
            # Transform to dict and append into the list
            query_data.append(
                model_type(
                    **{
                        column: data[index]
                        for index, column in enumerate(column_name)
                    }
                )
            ) 

    return query_data


def execute_dml(connection_obj,query_string,param_dict):
    """ Execute SQL Command  Update , Insert or Delete operations. It doesn't return any data from the database

    Args:
        connection_obj (Object) : Connection object
        query_string (String)   : Sql query 
        param_dict (Dictonery)  : If Query do have parameters then it contain the key and its associate value

    Returns:
        Integer: Return 0 if query successfully executed
    """
    cursor = connection_obj.cursor() # Open the cursor.

    if param_dict is None:
        cursor.execute(query_string)
    else:
        cursor.execute(query_string,param_dict) # Execute the update/delete/insert
    connection_obj.commit() #Commit changes
    return 0

def execute_dml_batch(connection_obj,query_string,param_dict):
    """ Execute SQL Command  Update , Insert or Delete operations. It doesn't return any data from the database

    Args:
        connection_obj (Object) : Connection object
        query_string (String)   : Sql query 
        param_dict (Dictonery)  : If Query do have parameters then it contain the key and its associate value

    Returns:
        Integer: Return 0 if query successfully executed
    """
    cursor = connection_obj.cursor() # Open the cursor.
    
    

    if param_dict is None:
        cursor.executemany(query_string)
    else:
        cursor.executemany(query_string,param_dict) # Execute the update/delete/insert
    #connection_obj.commit() #Commit changes
    return 0

