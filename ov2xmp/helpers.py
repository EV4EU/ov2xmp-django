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


from rest_framework_simplejwt.authentication import JWTAuthentication  
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from typing import Callable
from django.db.models.manager import BaseManager
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='fields', type=OpenApiTypes.STR),
            OpenApiParameter(name='paginate', type=OpenApiTypes.BOOL)
        ]
    )
)
class CustomListApiView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class: Callable
    queryset: BaseManager
    pagination_class = LimitOffsetPagination

    def get(self, request):
        fields = request.GET.get('fields', None)
        paginate = request.GET.get('paginate', False)
        filtered_queryset = self.filter_queryset(self.queryset)
        if paginate:
            paginated_queryset = self.paginate_queryset(queryset=filtered_queryset)
            if paginated_queryset is not None:
                if fields is not None:
                    fields = fields.split(',')
                    data = list(paginated_queryset.values(*fields))
                    return Response(self.get_paginated_response(data))
                else:
                    data = self.get_serializer(paginated_queryset, many=True).data
                    return self.get_paginated_response(data)
            else:
                return Response(data="You selected to paginate, but pagination is disabled", status=403)
        else:
            if fields is not None:
                fields = fields.split(',')
                data = list(filtered_queryset.values(*fields))
                return Response(data)
            else:
                return Response(data=self.serializer_class(filtered_queryset.all(), many=True).data)

class CustomListCreateApiView(CustomListApiView, CreateAPIView):
    pass