# first match the data type If the value type is a matched and shown a error then return it types of value else return blank or defult data type.
class MyConvert:
    @staticmethod
    def to_string(value) -> str:
        if value is None:
            return ""
        try:
            return str(value)
        except Exception: 
            return ""

    def to_int(value) -> int:
        if value is None:
            return 0
        try:
            return int(value)
        except Exception:
            return 0

    def to_float(value) -> float:
        if value is None:
            return 0.0
        try:
            return float(value)
        except Exception:
            return 0.0
    
    def to_bool(value) -> bool:
        if value is None:
            return False
        try:
            return bool(value)
        except Exception:
            return False
    
    def to_list(value) -> list:
        if value is None:
            return []
        try:
            return list(value)
        except Exception:
            return []
    
    def to_dict(value) -> dict:
        if value is None:
            return {}
        try:
            return dict(value)
        except Exception:
            return {}

        

