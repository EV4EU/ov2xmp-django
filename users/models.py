import pytz
from django.db import models
from django.contrib.auth.models import User
# pip install django-timezone-field --> Deprecated
from timezone_field import TimeZoneField
from chargepoint.models import ChargepointSocket
from django.contrib.postgres.fields import ArrayField
from creditcards.models import CardNumberField, CardExpiryField
from chargepoint.models import get_chargepointsocket_default


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    timezone = TimeZoneField(default='Europe/Athens')
    chargepoint_sockets = ArrayField(models.CharField(max_length=10, choices=ChargepointSocket.choices), default=get_chargepointsocket_default)
    cc_number = CardNumberField(null=True, blank=True)
    cc_expirydate = CardExpiryField(null=True, blank=True)


    def __str__(self):
        return f'{self.user.username} Profile'
