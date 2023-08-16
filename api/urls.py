from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from chargepoint.views import ChargepointApiView, ChargepointDetailApiView
from connector.views import ConnectorApiView, ConnectorDetailApiView
from chargingprofile.views import ChargingprofileApiView, ChargingprofileDetailApiView
from idtag.views import IdtagApiView, IdtagDetailApiView
from tasks.views import TasksApiView, TasksDetailApiView
from api.views import *
from location.views import LocationApiView, LocationDetailApiView
from reservation.views import ReservationApiView, ReservationDetailApiView
from statusnotification.views import StatusnotificationApiView, StatusnotificationSearchApiView
from transaction.views import TransactionApiView, TransactionDetailApiView, TransactionSearchApiView

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('redoc/', SpectacularRedocView.as_view(), name='redoc'),

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
    path('location/<str:location_id>/', LocationDetailApiView.as_view()),

    path('reservation/', ReservationApiView.as_view()),
    path('reservation/<str:reservation_id>/', ReservationDetailApiView.as_view()),

    path('statusnotification/<str:statusnotification_id>/', StatusnotificationApiView.as_view()),
    path('statusnotification/search/<str:chargepoint_id>/', StatusnotificationSearchApiView.as_view()),

    path('transaction/', TransactionApiView.as_view()),
    path('transaction/<str:transaction_id>/', TransactionDetailApiView.as_view()),
    path('transaction/search/<str:chargepoint_id>/', TransactionSearchApiView.as_view()),

    path('ocpp16/reset/', Ocpp16ResetApiView.as_view()),
    path('ocpp16/remotestarttransaction', Ocpp16RemoteStartTrasactionApiView.as_view()),
    path('ocpp16/remotestoptransaction', Ocpp16RemoteStopTrasactionApiView.as_view()),
    path('ocpp16/reservenow', Ocpp16ReserveNowApiView.as_view()),
    path('ocpp16/cancelreservation', Ocpp16CancelReservationApiView.as_view()),
    path('ocpp16/changeavailaility', Ocpp16ChangeAvailabilityApiView.as_view()),
    path('ocpp16/changeconfiguration', Ocpp16ChangeConfigurationApiView.as_view()),
    path('ocpp16/clearcache', Ocpp16ClearCacheApiView.as_view()),
    path('ocpp16/unlockconnector', Ocpp16UnlockConnectorApiView.as_view()),
    path('ocpp16/getconfiguration', Ocpp16GetConfigurationApiView.as_view()),
    path('ocpp16/getcompositeschedule', Ocpp16GetCompositeScheduleApiView.as_view()),
    path('ocpp16/clearchargingprofile', Ocpp16ClearChargingProfileApiView.as_view()),
    path('ocpp16/setchargingprofile', Ocpp16SetChargingProfileApiView.as_view()),
    path('ocpp16/getdiagnostics', Ocpp16GetDiagnosticsApiView.as_view()),
]