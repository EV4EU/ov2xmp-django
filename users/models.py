import pytz
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from timezone_field import TimeZoneField
from connector.models import ConnectorType
from django.contrib.postgres.fields import ArrayField
from creditcards.models import CardNumberField, CardExpiryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    timezone = TimeZoneField(default='Europe/Athens')
    chargepoint_sockets = ArrayField(models.CharField(max_length=21, choices=ConnectorType.choices, null=True), default=list, blank=True)
    cc_number = CardNumberField(null=True, blank=True)
    cc_expirydate = CardExpiryField(null=True, blank=True)
    tariff_preference = models.FloatField(null=True, default=None, blank=True)


    def __str__(self):
        return f'{self.user.username} Profile'


class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)