from django.contrib import admin
from ocpi.models import Cdr, Tariff, TariffElement

# Register your models here.
admin.site.register(Cdr)
admin.site.register(Tariff)
admin.site.register(TariffElement)