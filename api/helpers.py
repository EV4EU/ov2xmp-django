from datetime import datetime
from uuid import UUID
from decimal import Decimal
from pydantic.main import BaseModel


def convert_special_types(obj):
    """
    Helper function that serializes Python dictionaries with nested non-serializable Python object, including Pydantic objects 
    It recursively traverses through a dictionary or list, and converts datetime to string via 
    isoformat(), UUID to string, Decimal to float, etc.
    """
    if isinstance(obj, dict):
        return {key: convert_special_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_special_types(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, UUID):
        return str(obj)
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, BaseModel):
        return obj.dict()
    else:
        return obj
