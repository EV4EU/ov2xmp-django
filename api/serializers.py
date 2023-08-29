from rest_framework import serializers
from ocpp.v16 import enums as ocppv16_enums
from enum import Enum


class CSMS_MESSAGE_CODE(Enum):
    CHARGING_STATION_DOES_NOT_EXIST = "Charging Station does not exist"
    CHARGING_PROFILE_DOES_NOT_EXIST = "Charging Profile does not exist"
    RESPONSE_RECEIVED = 200
    TASK_SUBMITTED = "Task has been submitted successfully"


class OcppCommandSerializer(serializers.Serializer):
    chargepoint_id = serializers.CharField(max_length=255)
    sync = serializers.BooleanField(required=False, default=True) # type: ignore
    class Meta:
        fields = "__all__"


class Ocpp16ResetSerializer(OcppCommandSerializer):
    reset_type = serializers.ChoiceField(choices=tuple(member.value for member in ocppv16_enums.ResetType))


class Ocpp16RemoteStartTransactionSerializer(OcppCommandSerializer):
    connector_id = serializers.IntegerField(default=None)
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
    charging_rate_unit_type = serializers.ChoiceField(required=False, choices=tuple(member.value for member in ocppv16_enums.ChargingRateUnitType))


class Ocpp16ClearChargingProfileSerializer(OcppCommandSerializer):
    charging_profile_id = serializers.IntegerField(required=False)
    connector_id = serializers.IntegerField(required=False)
    charging_profile_purpose_type = serializers.ChoiceField(required=False, choices=tuple(member.value for member in ocppv16_enums.ChargingProfilePurposeType))
    stack_level = serializers.IntegerField(required=False)    


class Ocpp16SetChargingProfileSerializer(OcppCommandSerializer):
    connector_id = serializers.IntegerField()
    charging_profile_id = serializers.IntegerField()


class Ocpp16GetDiagnosticsSerializer(OcppCommandSerializer):
    location = serializers.CharField(max_length=2000)
    retries = serializers.IntegerField(required=False)
    retry_interval = serializers.IntegerField(required=False)
    start_time = serializers.DateTimeField(required=False)
    stop_time = serializers.DateTimeField(required=False)


class Ocpp16UpdateFirmwareSerializer(OcppCommandSerializer):
    location = serializers.CharField(max_length=2000)
    retries = serializers.IntegerField(required=False)
    retrieve_date = serializers.DateTimeField()
    retry_interval = serializers.IntegerField(required=False)


class Ocpp16TriggerMessasgeSerializer(OcppCommandSerializer):
    requested_message = serializers.ChoiceField(required=False, choices=tuple(member.value for member in ocppv16_enums.MessageTrigger))
    connector_id = serializers.IntegerField(required=False)


class Ocpp16SendLocalListSerializer(OcppCommandSerializer):
    list_version = serializers.IntegerField()
    local_authorization_list = serializers.ListField(required=False, default=list())
    update_type = serializers.ChoiceField(choices=tuple(member.value for member in ocppv16_enums.UpdateType))
