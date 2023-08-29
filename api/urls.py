from django.urls import path
from chargepoint.views import ChargepointApiView, ChargepointDetailApiView
from connector.views import ConnectorApiView, ConnectorDetailApiView
from chargingprofile.views import ChargingprofileApiView, ChargingprofileDetailApiView
from idtag.views import IdtagApiView, IdtagDetailApiView
from tasks.views import TasksApiView, TasksDetailApiView
from api.views import *
from location.views import LocationApiView, LocationDetailApiView
from reservation.views import ReservationApiView, ReservationDetailApiView
from statusnotification.views import StatusnotificationDetailApiView
from transaction.views import TransactionApiView, TransactionDetailApiView
from sampledvalue.views import SampledvalueDetailApiView

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('redoc/', SpectacularRedocView.as_view(), name='redoc'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('chargepoint/', ChargepointApiView.as_view()),
    path('chargepoint/<str:chargepoint_id>/', ChargepointDetailApiView.as_view()),

    path('connector/', ConnectorApiView.as_view()),
    path('connector/<str:chargepoint_id>/', ConnectorDetailApiView.as_view()),

    path('chargingprofile/', ChargingprofileApiView.as_view()),
    path('chargingprofile/<str:chargingprofile_id>/', ChargingprofileDetailApiView.as_view()),

    path('idtag/', IdtagApiView.as_view()),
    path('idtag/<str:id_token>/', IdtagDetailApiView.as_view()),

    path('task/', TasksApiView.as_view()),
    path('task/<str:task_id>/', TasksDetailApiView.as_view()),

    path('location/', LocationApiView.as_view()),
    path('location/<str:location_uuid>/', LocationDetailApiView.as_view()),

    path('reservation/', ReservationApiView.as_view()),
    path('reservation/<str:chargepoint_id>/', ReservationDetailApiView.as_view()),

    path('transaction/', TransactionApiView.as_view()),
    path('transaction/<int:transaction_id>/', TransactionDetailApiView.as_view()),

    path('sampledvalue/<str:transaction_id>/', SampledvalueDetailApiView.as_view()),

    path('statusnotification/<str:chargepoint_id>/', StatusnotificationDetailApiView.as_view()),

    path('ocpp16/reset/', Ocpp16ResetApiView.as_view()),
    path('ocpp16/remotestarttransaction/', Ocpp16RemoteStartTrasactionApiView.as_view()),
    path('ocpp16/remotestoptransaction/', Ocpp16RemoteStopTrasactionApiView.as_view()),
    path('ocpp16/reservenow/', Ocpp16ReserveNowApiView.as_view()),
    path('ocpp16/cancelreservation/', Ocpp16CancelReservationApiView.as_view()),
    path('ocpp16/changeavailaility/', Ocpp16ChangeAvailabilityApiView.as_view()),
    path('ocpp16/changeconfiguration/', Ocpp16ChangeConfigurationApiView.as_view()),
    path('ocpp16/clearcache/', Ocpp16ClearCacheApiView.as_view()),
    path('ocpp16/unlockconnector/', Ocpp16UnlockConnectorApiView.as_view()),
    path('ocpp16/getconfiguration/', Ocpp16GetConfigurationApiView.as_view()),
    path('ocpp16/getcompositeschedule/', Ocpp16GetCompositeScheduleApiView.as_view()),
    path('ocpp16/clearchargingprofile/', Ocpp16ClearChargingProfileApiView.as_view()),
    path('ocpp16/setchargingprofile/', Ocpp16SetChargingProfileApiView.as_view()),
    path('ocpp16/getdiagnostics/', Ocpp16GetDiagnosticsApiView.as_view()),
    path('ocpp16/updatefirmware/', Ocpp16UpdateFirmwareApiView.as_view()),
    path('ocpp16/triggermessage/', Ocpp16TriggerMessageApiView.as_view()),
    path('ocpp16/getlocallistversion/', Ocpp16GetLocalListVersionApiView.as_view()),
    path('ocpp16/sendlocallist/', Ocpp16SendLocalListApiView.as_view()),
]