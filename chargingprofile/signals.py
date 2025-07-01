from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from chargingprofile.models import Chargingprofile16
from connector.models import Connector
from ocpp_rest.tasks import ocpp16_set_charging_profile_task


@receiver(post_save, sender=Chargingprofile16)
def update_chargingprofile_on_connector(sender, instance, created, **kwargs):
    # Search connectors that have this chargingprofile
    this_chargingprofile_id = instance.chargingprofile_id

    all_connectors = Connector.objects.all()
    connectors_to_update = []

    for _connector in all_connectors:
        _chargingprofiles = _connector.charging_profile
        if _chargingprofiles is not None:
            for _chargingprofile in _chargingprofiles:
                if _chargingprofile == this_chargingprofile_id:
                    connectors_to_update.append(_connector.uuid)
    
    # setchargingprofile to all connectors
    for _connector in connectors_to_update:
        connector_obj = Connector.objects.get(uuid=_connector.uuid)
        task = ocpp16_set_charging_profile_task.delay(connector_obj.chargepoint.chargepoint_id, connector_obj.connectorid, this_chargingprofile_id)
        