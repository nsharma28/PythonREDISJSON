class OpenConnectionError(Exception):
    def __init__(self):
        self.msg = "Failed to create connection"

    def __str__(self):
        return (self.msg)

class CloseConnectionError(Exception):
    def __init__(self):
        self.msg = "Failed to close connection"
        
    def __str__(self):
        return (self.msg)

class QueryExecutionError(Exception):
    def __init__(self):
        self.msg = "Invalid query"
        
    def __str__(self):
        return (self.msg)

class QueryOutputError(Exception):
    def __init__(self):
        self.msg = "Query does not return any value"
        
    def __str__(self):
        return (self.msg)

class ResultDataConversionError(Exception):
    def __init__(self):
        self.msg = "Query data conversion failed"
        
    def __str__(self):
        return (self.msg)

class InsertExecutionError(Exception):
    def __init__(self):
        self.msg = "Insertion Failed"
        
    def __str__(self):
        return (self.msg)
    

