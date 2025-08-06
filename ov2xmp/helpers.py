from datetime import datetime, timezone
from uuid import UUID
from decimal import Decimal
from pydantic.main import BaseModel
from enum import Enum


def get_current_utc_string_without_timezone_offset():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3] + "Z"


def convert_datetime_to_string_without_timezone_offset(dt: datetime):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3] + "Z"


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


class CSMS_MESSAGE_CODE(Enum):
    CHARGING_STATION_DOES_NOT_EXIST = "Charging Station does not exist"
    CHARGING_PROFILE_DOES_NOT_EXIST = "Charging Profile does not exist"
    RESPONSE_RECEIVED = 200
    TASK_SUBMITTED = "Task has been submitted successfully"


class MESSAGE_CODE(Enum):
    RESPONSE_RECEIVED = 200
    TASK_SUBMITTED = "Task has been submitted successfully"
