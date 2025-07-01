from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from ocpp_rest.serializers import *
from ocpp_rest.tasks import *
from ov2xmp.helpers import CSMS_MESSAGE_CODE
from rest_framework_simplejwt.authentication import JWTAuthentication  


class Ocpp16ResetApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp16ResetSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send a Reset command (hard or soft)
        '''

        serializer = Ocpp16ResetSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_reset_task(serializer.data["chargepoint_id"], serializer.data["reset_type"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_reset_task.delay(serializer.data["chargepoint_id"], serializer.data["reset_type"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16RemoteStartTrasactionApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp16RemoteStartTransactionSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send a Remote Start Transaction command
        '''

        serializer = Ocpp16RemoteStartTransactionSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_remote_start_transaction(serializer.data["chargepoint_id"], request.data["connector_id"], request.data["id_tag"], request.data.get("charging_profile", None))
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_remote_start_transaction.delay(serializer.data["chargepoint_id"], request.data["connector_id"], request.data["id_tag"], request.data.get("charging_profile", None)) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16RemoteStopTrasactionApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp16RemoteStopTransactionSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send a Remote Stop Transaction command
        '''

        serializer = Ocpp16RemoteStopTransactionSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_remote_stop_transaction(serializer.data["chargepoint_id"], serializer.data["transaction_id"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_remote_stop_transaction.delay(serializer.data["chargepoint_id"], serializer.data["transaction_id"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16ReserveNowApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp16ReserveNowSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send a Reserve Now command
        '''

        serializer = Ocpp16ReserveNowSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_reserve_now(serializer.data["chargepoint_id"], serializer.data["connector_id"], serializer.data["id_tag"], serializer.data["expiry_date"], serializer.data["reservation_id"]) 
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_reserve_now.delay(serializer.data["chargepoint_id"], serializer.data["connector_id"], serializer.data["id_tag"], serializer.data["expiry_date"], serializer.data["reservation_id"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16CancelReservationApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp16CancelReservationSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send a Cancel Reservation command
        '''

        serializer = Ocpp16CancelReservationSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_cancel_reservation(serializer.data["chargepoint_id"], serializer.data["reservation_id"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_cancel_reservation.delay(serializer.data["chargepoint_id"], serializer.data["reservation_id"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16ChangeAvailabilityApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp16ChangeAvailabilitySerializer

    def post(self, request, *args, **kwargs):
        '''
        Send a Change Availability command
        '''

        serializer = Ocpp16ChangeAvailabilitySerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_change_availability(serializer.data["chargepoint_id"], serializer.data["connector_id"], serializer.data["availability_type"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_change_availability.delay(serializer.data["chargepoint_id"], serializer.data["connector_id"], serializer.data["availability_type"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16ChangeConfigurationApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp16ChangeConfigurationSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send a Change Configuration command
        '''

        serializer = Ocpp16ChangeConfigurationSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_change_configuration(serializer.data["chargepoint_id"], serializer.data["key"], serializer.data["value"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_change_configuration.delay(serializer.data["chargepoint_id"], serializer.data["key"], serializer.data["value"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16ClearCacheApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = OcppCommandSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send a Clear Cache command
        '''

        serializer = OcppCommandSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_clear_cache(serializer.data["chargepoint_id"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_clear_cache.delay(serializer.data["chargepoint_id"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16UnlockConnectorApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp16UnlockConnectorSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send an Unlock Connector command
        '''

        serializer = Ocpp16UnlockConnectorSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_unlock_connector(serializer.data["chargepoint_id"], serializer.data["connector_id"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_unlock_connector.delay(serializer.data["chargepoint_id"], serializer.data["connector_id"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16GetConfigurationApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp16GetConfigurationSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send a Get Configuration command
        '''

        serializer = Ocpp16GetConfigurationSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_get_configuration(serializer.data["chargepoint_id"], serializer.data["keys"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_get_configuration.delay(serializer.data["chargepoint_id"], serializer.data["keys"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16GetCompositeScheduleApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp16GetCompositeScheduleSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send a Get Composite Schedule command
        '''

        serializer = Ocpp16GetCompositeScheduleSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_get_composite_schedule_task(serializer.data["chargepoint_id"], serializer.data["connector_id"], serializer.data["duration"], serializer.data["charging_rate_unit_type"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_get_composite_schedule_task.delay(serializer.data["chargepoint_id"], serializer.data["connector_id"], serializer.data["duration"], serializer.data["charging_rate_unit_type"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16ClearChargingProfileApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp16ClearChargingProfileSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send a Clear Charging Profile command
        '''

        serializer = Ocpp16ClearChargingProfileSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_clear_charging_profile_task(serializer.data["chargepoint_id"], serializer.data["charging_profile_id"], serializer.data["connector_id"], serializer.data["charging_profile_purpose_type"], serializer.data["stack_level"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_clear_charging_profile_task.delay(serializer.data["chargepoint_id"], serializer.data["charging_profile_id"], serializer.data["connector_id"], serializer.data["charging_profile_purpose_type"], serializer.data["stack_level"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class Ocpp16SetChargingProfileApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp16SetChargingProfileSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send a Set Charging Profile command
        '''

        serializer = Ocpp16SetChargingProfileSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_set_charging_profile_task(serializer.data["chargepoint_id"], serializer.data["connector_id"], serializer.data["charging_profile_id"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_set_charging_profile_task.delay(serializer.data["chargepoint_id"], serializer.data["connector_id"], serializer.data["charging_profile_id"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16GetDiagnosticsApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp16GetDiagnosticsSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send a Get Diagnostics command
        '''

        serializer = Ocpp16GetDiagnosticsSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_get_diagnostics_task(serializer.data["chargepoint_id"], serializer.data["location"], serializer.data.get("retries", None), serializer.data.get("retry_interval", None), serializer.data.get("start_time", None), serializer.data.get("stop_time", None))
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_get_diagnostics_task.delay(serializer.data["chargepoint_id"], serializer.data["location"], serializer.data["retries"], serializer.data["retry_interval"], serializer.data["start_time"], serializer.data["stop_time"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16UpdateFirmwareApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp16UpdateFirmwareSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send an Update Firmware command
        '''

        serializer = Ocpp16UpdateFirmwareSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_update_firmware_task(serializer.data["chargepoint_id"], serializer.data["location"], serializer.data.get("retries", None), serializer.data["retrieve_date"], serializer.data.get("retry_interval", None))
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_update_firmware_task.delay(serializer.data["chargepoint_id"], serializer.data["location"], serializer.data.get("retries", None), serializer.data["retrieve_date"], serializer.data.get("retry_interval", None))  # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16TriggerMessageApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp16TriggerMessasgeSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send a Trigger Message command
        '''

        serializer = Ocpp16TriggerMessasgeSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_trigger_message_task(serializer.data["chargepoint_id"], serializer.data["requested_message"], serializer.data.get("connector_id", None))
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_trigger_message_task.delay(serializer.data["chargepoint_id"], serializer.data["requested_message"], serializer.data.get("connector_id", None))  # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16GetLocalListVersionApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = OcppCommandSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send a Get Local List Version command
        '''

        serializer = OcppCommandSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_get_local_list_version_task(serializer.data["chargepoint_id"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_get_local_list_version_task.delay(serializer.data["chargepoint_id"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16SendLocalListApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp16SendLocalListSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send a Send Local List command
        '''

        serializer = Ocpp16SendLocalListSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_get_local_list_version_task(serializer.data["chargepoint_id"], serializer.data["list_version"], serializer.data["local_authorization_list"], serializer.data["update_type"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_get_local_list_version_task.delay(serializer.data["chargepoint_id"], serializer.data["list_version"], serializer.data["local_authorization_list"], serializer.data["update_type"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

###################################################################################################################################
###################################################################################################################################
###################################################################################################################################

class Ocpp201ResetApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp201ResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = Ocpp201ResetSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp201_reset(serializer.data["chargepoint_id"], serializer.data["reset_type"], serializer.data["evse_id"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp201_reset.delay(serializer.data["chargepoint_id"], serializer.data["reset_type"], serializer.data["evse_id"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp201ClearCacheApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = OcppCommandSerializer

    def post(self, request, *args, **kwargs):
        serializer = OcppCommandSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp201_clear_cache(serializer.data["chargepoint_id"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp201_clear_cache.delay(serializer.data["chargepoint_id"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Ocpp201ChangeAvailabilityApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp201ChangeAvailabilitySerializer

    def post(self, request, *args, **kwargs):
        serializer = Ocpp201ChangeAvailabilitySerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp201_change_availability(serializer.data["chargepoint_id"], serializer.data["operational_status"], serializer.data["evse_id"], serializer.data["connector_id"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp201_change_availability.delay(serializer.data["chargepoint_id"], serializer.data["operational_status"], serializer.data["evse_id"], serializer.data["connector_id"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp201ClearChargingProfileApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp201ClearChargingProfileSerializer

    def post(self, request, *args, **kwargs):
        serializer = Ocpp201ClearChargingProfileSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp201_clear_charging_profile(serializer.data["chargepoint_id"], serializer.data["charging_profile_id"], serializer.data["charging_profile_criteria"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp201_clear_charging_profile.delay(serializer.data["chargepoint_id"], serializer.data["charging_profile_id"], serializer.data["charging_profile_criteria"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp201ClearDisplayMessageApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp201ClearChargingProfileSerializer

    def post(self, request, *args, **kwargs):
        serializer = Ocpp201ClearChargingProfileSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp201_clear_display_message(serializer.data["chargepoint_id"], serializer.data["id"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp201_clear_display_message.delay(serializer.data["chargepoint_id"], serializer.data["id"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp201GetChargingProfilesApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp201GetChargingProfilesSerializer

    def post(self, request, *args, **kwargs):
        serializer = Ocpp201GetChargingProfilesSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp201_get_charging_profile(serializer.data["chargepoint_id"], serializer.data["request_id"], serializer.data["evse_id"], serializer.data["charging_profile"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp201_get_charging_profile.delay(serializer.data["chargepoint_id"], serializer.data["request_id"], serializer.data["evse_id"], serializer.data["charging_profile"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp201GetDisplayMessagesApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp201GetDisplayMessagesSerializer

    def post(self, request, *args, **kwargs):
        serializer = Ocpp201GetDisplayMessagesSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp201_get_display_messages(serializer.data["chargepoint_id"], serializer.data["request_id"], serializer.data["id"], serializer.data["priority"], serializer.data["state"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp201_get_display_messages.delay(sserializer.data["chargepoint_id"], serializer.data["request_id"], serializer.data["id"], serializer.data["priority"], serializer.data["state"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp201RequestStartTransactionApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp201RequestStartTransactionSerializer

    def post(self, request, *args, **kwargs):
        serializer = Ocpp201RequestStartTransactionSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp201_request_start_transaction(serializer.data["chargepoint_id"], serializer.data["id_token"], serializer.data["evse_id"], serializer.data["remote_start_id"], serializer.data["charging_profile_id"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp201_request_start_transaction.delay(serializer.data["chargepoint_id"], serializer.data["id_token"], serializer.data["evse_id"], serializer.data["remote_start_id"], serializer.data["charging_profile_id"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp201RequestStopTransactionApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp201RequestStopTransactionSerializer

    def post(self, request, *args, **kwargs):
        serializer = Ocpp201RequestStopTransactionSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp201_request_stop_transaction(serializer.data["chargepoint_id"], serializer.data["transaction_id"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp201_request_stop_transaction.delay(serializer.data["chargepoint_id"], serializer.data["transaction_id"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp201SetChargingProfileApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp201SetChargingProfileSerializer

    def post(self, request, *args, **kwargs):
        serializer = Ocpp201SetChargingProfileSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp201_set_charging_profile(serializer.data["chargepoint_id"], serializer.data["evse_id"], serializer.data["charging_profile_id"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp201_set_charging_profile.delay(serializer.data["chargepoint_id"], serializer.data["evse_id"], serializer.data["charging_profile_id"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp201SetDisplayMessageApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp201SetDisplayMessageSerializer

    def post(self, request, *args, **kwargs):
        serializer = Ocpp201SetDisplayMessageSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp201_set_display_message(serializer.data["chargepoint_id"], serializer.data["message"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp201_set_display_message.delay(serializer.data["chargepoint_id"], serializer.data["message"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp201UnlockConnectorApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Ocpp201UnlockConnectorSerializer

    def post(self, request, *args, **kwargs):
        serializer = Ocpp201UnlockConnectorSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp201_unlock_connector(serializer.data["chargepoint_id"], serializer.data["evse_id"], serializer.data["connector_id"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp201_unlock_connector.delay(serializer.data["chargepoint_id"], serializer.data["evse_id"], serializer.data["connector_id"]) # type: ignore
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
