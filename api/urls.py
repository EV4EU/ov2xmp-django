from django.urls import path, include
from chargepoint.views import ChargepointApiView, ChargepointDetailApiView
from connector.views import ConnectorApiView, ConnectorDetailApiView
from chargingprofile.views import Chargingprofile16ApiView, Chargingprofile16DetailApiView
from chargingprofile.views import Chargingprofile201ApiView, Chargingprofile201DetailApiView
from idtag.views import IdtagApiView, IdtagDetailApiView
from tasks.views import TasksApiView, TasksDetailApiView
from ocpp_rest.views import *
from location.views import LocationApiView, LocationDetailApiView
from reservation.views import ReservationApiView, ReservationDetailApiView
from statusnotification.views import StatusnotificationDetailApiView, Statusnotification201DetailApiView
from transaction.views import TransactionApiView, TransactionDetailApiView
from sampledvalue.views import SampledvalueDetailApiView
from users.views import UserApiView, UserDetailApiView, UserCreateApiView, MyTokenObtainPairView #, UserProfileDetailApiView
from ocpi.views import TariffApiView, TariffDetailApiView, TariffElementApiView, TariffElementDetailApiView, CdrApiView, CdrDetailApiView
from dso_rest.views import DsoSignalApiView, DsoSignalDetailApiView
from mailsending.views import SendEmailView
from users.views import RequestPasswordReset
from users.views import ResetPassword
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('redoc/', SpectacularRedocView.as_view(), name='redoc'),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('chargepoint/', ChargepointApiView.as_view()),
    path('chargepoint/<str:chargepoint_id>/', ChargepointDetailApiView.as_view()),

    path('connector/', ConnectorApiView.as_view()),
    path('connector/<str:uuid>/', ConnectorDetailApiView.as_view()),

    path('chargingprofile16/', Chargingprofile16ApiView.as_view()),
    path('chargingprofile16/<str:chargingprofile_id>/', Chargingprofile16DetailApiView.as_view()),

    path('chargingprofile201/', Chargingprofile201ApiView.as_view()),
    path('chargingprofile201/<str:chargingprofile_id>/', Chargingprofile201DetailApiView.as_view()),

    path('user/create/', UserCreateApiView.as_view()),
    path('user/', UserApiView.as_view()),
    path('user/<str:username>/', UserDetailApiView.as_view()),
    path('user/password-reset/request/', RequestPasswordReset.as_view()),
    path('user/password-reset/submit/', ResetPassword.as_view()),


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

    path('tariff/', TariffApiView.as_view()),
    path('tariff/<str:id>/', TariffDetailApiView.as_view()),
    path('tariffelement/', TariffElementApiView.as_view()),
    path('tariffelement/<int:id>/', TariffElementDetailApiView.as_view()),

    path('cdr/', CdrApiView.as_view()),
    path('cdr/<str:id>/', CdrDetailApiView.as_view()),

    path('sampledvalue/<str:transaction_id>/', SampledvalueDetailApiView.as_view()),

    path('statusnotification/<str:chargepoint_id>/', StatusnotificationDetailApiView.as_view()),
    path('statusnotification201/<str:chargepoint_id>/', Statusnotification201DetailApiView.as_view()),
    
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

    path('ocpp201/reset/', Ocpp201ResetApiView.as_view()),
    path('ocpp201/changeavailability/', Ocpp201ChangeAvailabilityApiView.as_view()),
    path('ocpp201/clearcache/', Ocpp201ClearCacheApiView.as_view()),
    path('ocpp201/clearchargingprofile/', Ocpp201ClearChargingProfileApiView.as_view()),
    path('ocpp201/cleardisplaymessage/', Ocpp201ClearDisplayMessageApiView.as_view()),
    path('ocpp201/getchargingprofiles/', Ocpp201GetChargingProfilesApiView.as_view()),
    path('ocpp201/getdisplaymessages/', Ocpp201GetDisplayMessagesApiView.as_view()),
    path('ocpp201/requeststarttransaction/', Ocpp201RequestStartTransactionApiView.as_view()),
    path('ocpp201/requeststoptransaction/', Ocpp201RequestStopTransactionApiView.as_view()),
    path('ocpp201/setchargingprofile/', Ocpp201SetChargingProfileApiView.as_view()),
    path('ocpp201/setdisplaymessage/', Ocpp201SetDisplayMessageApiView.as_view()),
    path('ocpp201/unlockconnector/', Ocpp201UnlockConnectorApiView.as_view()),

    path('dso/signal/', DsoSignalApiView.as_view()),
    path('dso/signal/<int:id>/', DsoSignalDetailApiView.as_view()),
    
    path('mailsending/', SendEmailView.as_view(), name='mailsending'),
]