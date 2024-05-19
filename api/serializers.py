from rest_framework import serializers
from enum import Enum


class RelatedFieldAlternative(serializers.PrimaryKeyRelatedField):
    """
    Simple foreign key assignment with nested serializers
    """
    def __init__(self, **kwargs):
        self.serializer = kwargs.pop('serializer', None)
        if self.serializer is not None and not issubclass(self.serializer, serializers.Serializer):
            raise TypeError('"serializer" is not a valid serializer class')

        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False if self.serializer else True

    def to_representation(self, instance):
        if self.serializer:
            return self.serializer(instance, context=self.context).data
        return super().to_representation(instance)


class CSMS_MESSAGE_CODE(Enum):
    CHARGING_STATION_DOES_NOT_EXIST = "Charging Station does not exist"
    CHARGING_PROFILE_DOES_NOT_EXIST = "Charging Profile does not exist"
    RESPONSE_RECEIVED = 200
    TASK_SUBMITTED = "Task has been submitted successfully"
