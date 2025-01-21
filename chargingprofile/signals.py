from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Chargingprofile


@receiver(post_save, sender=Chargingprofile)
def update_chargingprofile_on_connector(sender, instance, created, **kwargs):
    # Search connectors that have this chargingprofile

    # setchargingprofile to all connectors  (celery beat)

    pass