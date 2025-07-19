from rest_framework import serializers
from ocpp.v16 import enums as ocppv16_enums
from ocpp.v201 import enums as ocppv201_enums
from rest_framework_dataclasses.serializers import DataclassSerializer
from ocpp.v201 import datatypes as ocppv201_datatypes
import random

class OcppCommandSerializer(serializers.Serializer):
    chargepoint_id = serializers.CharField(max_length=255)
    sync = serializers.BooleanField(required=False, default=True)
    class Meta:
        fields = "__all__"


class Ocpp16ResetSerializer(OcppCommandSerializer):
    reset_type = serializers.ChoiceField(choices=tuple(member.value for member in ocppv16_enums.ResetType))


class Ocpp16RemoteStartTransactionSerializer(OcppCommandSerializer):
    connector_id = serializers.IntegerField(required=False, default=None)
    charging_profile_id = serializers.IntegerField(required=False, default=None)
    id_tag = serializers.CharField(max_length=255)


class Ocpp16RemoteStopTransactionSerializer(OcppCommandSerializer):
    transaction_id = serializers.IntegerField()


class Ocpp16ReserveNowSerializer(OcppCommandSerializer):
    connector_id = serializers.IntegerField(required=False, default=None)
    id_tag = serializers.CharField(max_length=255)
    expiry_date = serializers.DateTimeField()
    reservation_id = serializers.IntegerField(required=False, default=None)


class Ocpp16CancelReservationSerializer(OcppCommandSerializer):
    reservation_id = serializers.IntegerField()


class Ocpp16ChangeAvailabilitySerializer(OcppCommandSerializer):
    connector_id = serializers.IntegerField()
    availability_type = serializers.ChoiceField(choices=tuple(member.value for member in ocppv16_enums.AvailabilityType))


class Ocpp16ChangeConfigurationSerializer(OcppCommandSerializer):
    key = serializers.CharField(max_length=50)
    value = serializers.CharField(max_length=500)

#class Ocpp16ClearCache(OcppCommandSerializer):

class Ocpp16UnlockConnectorSerializer(OcppCommandSerializer):
    connector_id = serializers.IntegerField()


class Ocpp16GetConfigurationSerializer(OcppCommandSerializer):
    keys = serializers.ListField(child=serializers.CharField(max_length=50), required=False, default=None)


class Ocpp16GetCompositeScheduleSerializer(OcppCommandSerializer):
    connector_id = serializers.IntegerField()
    duration = serializers.IntegerField()
    charging_rate_unit_type = serializers.ChoiceField(required=False, default=None, choices=tuple(member.value for member in ocppv16_enums.ChargingRateUnitType))


class Ocpp16ClearChargingProfileSerializer(OcppCommandSerializer):
    charging_profile_id = serializers.IntegerField(required=False, default=None)
    connector_id = serializers.IntegerField(required=False, default=None)
    charging_profile_purpose = serializers.ChoiceField(required=False, default=None, choices=tuple(member.value for member in ocppv16_enums.ChargingProfilePurposeType))
    stack_level = serializers.IntegerField(required=False, default=None)    


class Ocpp16SetChargingProfileSerializer(OcppCommandSerializer):
    connector_id = serializers.IntegerField()
    charging_profile_id = serializers.IntegerField()


class Ocpp16GetDiagnosticsSerializer(OcppCommandSerializer):
    location = serializers.CharField(max_length=2000)
    retries = serializers.IntegerField(required=False, default=None)
    retry_interval = serializers.IntegerField(required=False, default=None)
    start_time = serializers.DateTimeField(required=False, default=None)
    stop_time = serializers.DateTimeField(required=False, default=None)


class Ocpp16UpdateFirmwareSerializer(OcppCommandSerializer):
    location = serializers.CharField(max_length=2000)
    retries = serializers.IntegerField(required=False, default=None)
    retrieve_date = serializers.DateTimeField()
    retry_interval = serializers.IntegerField(required=False, default=None)


class Ocpp16TriggerMessasgeSerializer(OcppCommandSerializer):
    requested_message = serializers.ChoiceField(choices=tuple(member.value for member in ocppv16_enums.MessageTrigger))
    connector_id = serializers.IntegerField(required=False, default=None)


class Ocpp16SendLocalListSerializer(OcppCommandSerializer):
    list_version = serializers.IntegerField()
    local_authorization_list = serializers.ListField(required=False, default=list())
    update_type = serializers.ChoiceField(choices=tuple(member.value for member in ocppv16_enums.UpdateType))


###################################################################################################################################
## Serializers for OCPP 2.0.1 dataclasses

class ChargingProfileCriterionTypeSerializer(DataclassSerializer):
    class Meta:
        dataclass = ocppv201_datatypes.ChargingProfileCriterionType

class IdTokenTypeSerializer(DataclassSerializer):
    class Meta:
        dataclass = ocppv201_datatypes.IdTokenType

class ChargingProfileTypeSerializer(DataclassSerializer):
    class Meta:
        dataclass = ocppv201_datatypes.ChargingProfileType

class MessageInfoTypeSerializer(DataclassSerializer):
    class Meta:
        dataclass = ocppv201_datatypes.MessageInfoType

###################################################################################################################################
## OCPP 2.0.1 Operations

class Ocpp201ResetSerializer(OcppCommandSerializer):
    reset_type = serializers.ChoiceField(choices=tuple(member.value for member in ocppv201_enums.ResetEnumType))
    evse_id = serializers.IntegerField(required=False, default=None)


class Ocpp201ChangeAvailabilitySerializer(OcppCommandSerializer):
    operational_status = serializers.ChoiceField(choices=tuple(member.value for member in ocppv201_enums.OperationalStatusEnumType))
    evse_id = serializers.IntegerField(required=False, default=None)
    connector_id = serializers.IntegerField(required=False, default=None)


class Ocpp201ClearChargingProfileSerializer(OcppCommandSerializer):
    charging_profile_id = serializers.IntegerField()
    charging_profile_criteria = ChargingProfileCriterionTypeSerializer(required=False, default=None)


class Ocpp201ClearDisplayMessageSerializer(OcppCommandSerializer):
    id = serializers.IntegerField()


class Ocpp201GetChargingProfilesSerializer(OcppCommandSerializer):
    request_id = serializers.IntegerField()
    evse_id = serializers.IntegerField(required=False, default=None)
    charging_profile = ChargingProfileCriterionTypeSerializer()


class Ocpp201GetDisplayMessagesSerializer(OcppCommandSerializer):
    request_id = serializers.IntegerField()
    id = serializers.ListField(child=serializers.IntegerField(), required=False, default=None)
    priority = serializers.ChoiceField(choices=tuple(member.value for member in ocppv201_enums.MessagePriorityEnumType), required=False, default=None)
    state = serializers.ChoiceField(choices=tuple(member.value for member in ocppv201_enums.MessageStateEnumType), required=False, default=None)


class Ocpp201RequestStartTransactionSerializer(OcppCommandSerializer):
    id_token = IdTokenTypeSerializer()
    evse_id = serializers.IntegerField(required=False, default=None)
    remote_start_id = serializers.IntegerField(required=False, default=random.randint(1, 99999))
    charging_profile_id = serializers.IntegerField(required=False, default=None)


class Ocpp201RequestStopTransactionSerializer(OcppCommandSerializer):
    transaction_id = serializers.CharField()


class Ocpp201SetChargingProfileSerializer(OcppCommandSerializer):
    evse_id = serializers.IntegerField()
    charging_profile_id = serializers.IntegerField()


class Ocpp201SetDisplayMessageSerializer(OcppCommandSerializer):
    message = MessageInfoTypeSerializer()


class Ocpp201UnlockConnectorSerializer(OcppCommandSerializer):
    evse_id = serializers.IntegerField()
    connector_id = serializers.IntegerField()
