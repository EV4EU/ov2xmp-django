from ocpp.routing import on
from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call_result, call
import ocpp.v201.enums as ocpp_enums
import ocpp.v201.datatypes as ocpp_datatypes
from ocpp.v201.enums import Action

from chargepoint.models import Chargepoint as ChargepointModel
from idtag.models import IdTag as idTagModel
from transaction.models import Transaction as TransactionModel
from transaction.models import TransactionStatus
from connector.models import Connector as ConnectorModel
from reservation.models import Reservation as ReservationModel
from statusnotification.models import Statusnotification as StatusnotificationModel
from sampledvalue.models import Sampledvalue as SampledvalueModel

from uuid import uuid4
from datetime import datetime, timezone
from django.utils import timezone
from datetime import datetime
import json
from channels.layers import get_channel_layer
from django.db import DatabaseError
import logging
from django.db.models import Max

channel_layer = get_channel_layer()

async def broadcast_metervalues(message):
    message = json.dumps(message)
    if channel_layer is not None:
        await channel_layer.group_send("metervalues_updates", {"type": "websocket.send", "text": message})


class ChargePoint201(cp):
    ##########################################################################################################################
    ###################  HANDLE INCOMING OCPP MESSAGES #######################################################################
    ##########################################################################################################################

    @on(Action.boot_notification)
    def on_boot_notification(self, charging_station, reason, **kwargs):

        charge_point_serial_number = charging_station.get("serial_number", None)
        chargepoint_model = charging_station["model"]
        firmware_version = charging_station["firmware_version"]
        chargepoint_vendor = charging_station["vendor_name"]

        ChargepointModel.objects.filter(pk=self.id).update(
            chargepoint_model = chargepoint_model, 
            chargepoint_vendor = chargepoint_vendor,
            chargepoint_serial_number = charge_point_serial_number,
            firmware_version = firmware_version
        ) 

        return call_result.BootNotification(
            current_time=datetime.now(timezone.utc).isoformat(),
            interval=10,
            status=ocpp_enums.RegistrationStatusEnumType.accepted,
        )
    

    @on(Action.heartbeat)
    def on_heartbeat(self):
        current_cp = ChargepointModel.objects.filter(pk=self.id).get()
        current_cp.last_heartbeat = datetime.now(timezone.utc)
        current_cp.save()

        return call_result.Heartbeat(
            current_time=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S") + "Z"
        )


    @on(Action.status_notification)
    def on_status_notification(self, timestamp, connector_status, evse_id, connector_id, **kwargs):
        current_cp = ChargepointModel.objects.filter(pk=self.id).get()
        if connector_id != 0:
            try:
                connector_to_update = ConnectorModel.objects.filter(chargepoint=current_cp, connectorid=connector_id).get()
                connector_to_update.connector_status = connector_status
                connector_to_update.save()
            except ConnectorModel.DoesNotExist:
                connector_to_update = None
                ConnectorModel.objects.create(
                    uuid = uuid4(),
                    connectorid = connector_id,
                    connector_status = connector_status,
                    chargepoint = current_cp
                )
            else:
                connector_to_update = None
                current_cp.chargepoint_status = connector_status
                current_cp.save()
            
        StatusnotificationModel.objects.create(
            connector = connector_to_update,
            chargepoint = current_cp,
            error_code = kwargs.get('error_code', None),
            info = kwargs.get('info', None),
            status_reported = connector_status,
            timestamp = kwargs.get('timestamp', datetime.now(timezone.utc)),
            vendor_id = kwargs.get('vendor_id', None),
            vendor_error_code = kwargs.get('vendor_error_code', None)
        )

        return call_result.StatusNotification()

    ##########################################################################################################################
    #################### ACTIONS INITIATED BY THE CSMS #######################################################################
    ##########################################################################################################################

    # Reset
    async def reset(self, reset_type):
        request = call.Reset(type = reset_type)
        response = await self.call(request)
        if response is not None:
            return {"status": response.status}
        else:
            return {"status": None}
    
