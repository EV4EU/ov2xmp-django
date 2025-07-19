from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from ocpp_rest.serializers import *
from ocpp_rest.tasks import *
from ov2xmp.helpers import CSMS_MESSAGE_CODE
from rest_framework_simplejwt.authentication import JWTAuthentication  
from rest_framework.serializers import Serializer, ReturnDict, ReturnList
from typing import Callable, Union


class OcppApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Serializer
    tasks_function: Callable[[Union[ReturnDict, ReturnList]], dict]

    def post(self, request, *args, **kwargs):
        '''
        Send an OCPP command
        '''

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:  # type: ignore
                task = self.tasks_function(serializer.data)
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = self.tasks_function.delay(serializer.data)
                return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ocpp16ResetApiView(OcppApiView):
    serializer_class = Ocpp16ResetSerializer
    tasks_function = ocpp16_reset_task


class Ocpp16RemoteStartTrasactionApiView(OcppApiView):
    serializer_class = Ocpp16RemoteStartTransactionSerializer
    tasks_function = ocpp16_remote_start_transaction


class Ocpp16RemoteStopTrasactionApiView(OcppApiView):
    serializer_class = Ocpp16RemoteStopTransactionSerializer
    tasks_function = ocpp16_remote_stop_transaction


class Ocpp16ReserveNowApiView(OcppApiView):
    serializer_class = Ocpp16ReserveNowSerializer
    tasks_function = ocpp16_reserve_now


class Ocpp16CancelReservationApiView(OcppApiView):
    serializer_class = Ocpp16CancelReservationSerializer
    tasks_function = ocpp16_cancel_reservation


class Ocpp16ChangeAvailabilityApiView(OcppApiView):
    serializer_class = Ocpp16ChangeAvailabilitySerializer
    tasks_function = ocpp16_change_availability


class Ocpp16ChangeConfigurationApiView(OcppApiView):
    serializer_class = Ocpp16ChangeConfigurationSerializer
    tasks_function = ocpp16_change_configuration


class Ocpp16ClearCacheApiView(OcppApiView):
    serializer_class = OcppCommandSerializer
    tasks_function = ocpp16_clear_cache


class Ocpp16UnlockConnectorApiView(OcppApiView):
    serializer_class = Ocpp16UnlockConnectorSerializer
    tasks_function = ocpp16_unlock_connector


class Ocpp16GetConfigurationApiView(OcppApiView):
    serializer_class = Ocpp16GetConfigurationSerializer
    tasks_function = ocpp16_get_configuration


class Ocpp16GetCompositeScheduleApiView(OcppApiView):
    serializer_class = Ocpp16GetCompositeScheduleSerializer
    tasks_function = ocpp16_get_composite_schedule_task


class Ocpp16ClearChargingProfileApiView(OcppApiView):
    serializer_class = Ocpp16ClearChargingProfileSerializer
    tasks_function = ocpp16_clear_charging_profile_task


class Ocpp16SetChargingProfileApiView(OcppApiView):
    serializer_class = Ocpp16SetChargingProfileSerializer
    tasks_function = ocpp16_set_charging_profile_task


class Ocpp16GetDiagnosticsApiView(OcppApiView):
    serializer_class = Ocpp16GetDiagnosticsSerializer
    tasks_function = ocpp16_get_diagnostics_task


class Ocpp16UpdateFirmwareApiView(OcppApiView):
    serializer_class = Ocpp16UpdateFirmwareSerializer
    tasks_function = ocpp16_update_firmware_task


class Ocpp16TriggerMessageApiView(OcppApiView):
    serializer_class = Ocpp16TriggerMessasgeSerializer
    tasks_function = ocpp16_trigger_message_task


class Ocpp16GetLocalListVersionApiView(OcppApiView):
    serializer_class = OcppCommandSerializer
    tasks_function = ocpp16_get_local_list_version_task


class Ocpp16SendLocalListApiView(OcppApiView):
    serializer_class = Ocpp16SendLocalListSerializer
    tasks_function = ocpp16_send_local_list_task


###################################################################################################################################
###################################################################################################################################
###################################################################################################################################

class Ocpp201ResetApiView(OcppApiView):
    serializer_class = Ocpp201ResetSerializer
    tasks_function = ocpp201_reset


class Ocpp201ClearCacheApiView(OcppApiView):
    authentication_classes = [JWTAuthentication]
    serializer_class = OcppCommandSerializer
    tasks_function = ocpp201_clear_cache


class Ocpp201ChangeAvailabilityApiView(OcppApiView):
    serializer_class = Ocpp201ChangeAvailabilitySerializer
    tasks_function = ocpp201_change_availability


class Ocpp201ClearChargingProfileApiView(OcppApiView):
    serializer_class = Ocpp201ClearChargingProfileSerializer
    tasks_function = ocpp201_clear_charging_profile


class Ocpp201ClearDisplayMessageApiView(OcppApiView):
    serializer_class = Ocpp201ClearChargingProfileSerializer
    tasks_function = ocpp201_clear_display_message


class Ocpp201GetChargingProfilesApiView(OcppApiView):
    serializer_class = Ocpp201GetChargingProfilesSerializer
    tasks_function = ocpp201_get_charging_profile


class Ocpp201GetDisplayMessagesApiView(OcppApiView):
    serializer_class = Ocpp201GetDisplayMessagesSerializer
    tasks_function = ocpp201_get_display_messages


class Ocpp201RequestStartTransactionApiView(OcppApiView):
    serializer_class = Ocpp201RequestStartTransactionSerializer
    tasks_function = ocpp201_request_start_transaction


class Ocpp201RequestStopTransactionApiView(OcppApiView):
    serializer_class = Ocpp201RequestStopTransactionSerializer
    tasks_function = ocpp201_request_stop_transaction


class Ocpp201SetChargingProfileApiView(OcppApiView):
    serializer_class = Ocpp201SetChargingProfileSerializer
    tasks_function = ocpp201_set_charging_profile


class Ocpp201SetDisplayMessageApiView(OcppApiView):
    serializer_class = Ocpp201SetDisplayMessageSerializer
    tasks_function = ocpp201_set_display_message


class Ocpp201UnlockConnectorApiView(OcppApiView):
    serializer_class = Ocpp201UnlockConnectorSerializer
    tasks_function = ocpp201_unlock_connector
