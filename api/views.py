from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import *
from .tasks import *
from drf_spectacular.openapi import AutoSchema


class Ocpp16ResetApiView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Ocpp16ResetSerializer
    schema = AutoSchema()

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
                return Response({"success": True, "status": "Task has been submitted successfully", "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16RemoteStartTrasactionApiView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Ocpp16RemoteStartTransactionSerializer
    schema = AutoSchema()

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
                return Response({"success": True, "status": "Task has been submitted successfully", "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16RemoteStopTrasactionApiView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Ocpp16RemoteStopTransactionSerializer
    schema = AutoSchema()

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
                return Response({"success": True, "status": "Task has been submitted successfully", "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16ReserveNowApiView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Ocpp16ReserveNowSerializer
    schema = AutoSchema()

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
                return Response({"success": True, "status": "Task has been submitted successfully", "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16CancelReservationApiView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Ocpp16CancelReservationSerializer
    schema = AutoSchema()

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
                return Response({"success": True, "status": "Task has been submitted successfully", "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16ChangeAvailabilityApiView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Ocpp16ChangeAvailabilitySerializer
    schema = AutoSchema()

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
                return Response({"success": True, "status": "Task has been submitted successfully", "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16ChangeConfigurationApiView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Ocpp16ChangeConfigurationSerializer
    schema = AutoSchema()

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
                return Response({"success": True, "status": "Task has been submitted successfully", "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16ClearCacheApiView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OcppCommandSerializer
    schema = AutoSchema()

    def post(self, request, *args, **kwargs):
        '''
        Send a Change Cache command
        '''

        serializer = OcppCommandSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = ocpp16_clear_cache(serializer.data["chargepoint_id"])
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = ocpp16_clear_cache.delay(serializer.data["chargepoint_id"]) # type: ignore
                return Response({"success": True, "status": "Task has been submitted successfully", "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16UnlockConnectorApiView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Ocpp16UnlockConnectorSerializer
    schema = AutoSchema()

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
                return Response({"success": True, "status": "Task has been submitted successfully", "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16GetConfigurationApiView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Ocpp16GetConfigurationSerializer
    schema = AutoSchema()

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
                return Response({"success": True, "status": "Task has been submitted successfully", "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16GetCompositeScheduleApiView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Ocpp16GetCompositeScheduleSerializer
    schema = AutoSchema()

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
                return Response({"success": True, "status": "Task has been submitted successfully", "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16ClearChargingProfileApiView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Ocpp16ClearChargingProfileSerializer
    schema = AutoSchema()

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
                return Response({"success": True, "status": "Task has been submitted successfully", "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class Ocpp16SetChargingProfileApiView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Ocpp16SetChargingProfileSerializer
    schema = AutoSchema()

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
                return Response({"success": True, "status": "Task has been submitted successfully", "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16GetDiagnosticsApiView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Ocpp16GetDiagnosticsSerializer
    schema = AutoSchema()

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
                return Response({"success": True, "status": "Task has been submitted successfully", "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16UpdateFirmwareApiView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Ocpp16UpdateFirmwareSerializer
    schema = AutoSchema()

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
                return Response({"success": True, "status": "Task has been submitted successfully", "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16TriggerMessageApiView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Ocpp16TriggerMessasgeSerializer
    schema = AutoSchema()

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
                return Response({"success": True, "status": "Task has been submitted successfully", "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
