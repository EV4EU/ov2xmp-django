# Generated by Django 5.0.2 on 2024-05-04 17:24

import django.contrib.postgres.fields
import ov2xmp.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TariffElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_components', django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(default=dict, validators=[ov2xmp.validators.JSONSchemaValidator(limit_value={'definitions': {'TariffDimensionType': {'description': 'An enumeration.', 'enum': ['ENERGY', 'FLAT', 'PARKING_TIME', 'TIME'], 'title': 'TariffDimensionType', 'type': 'string'}}, 'properties': {'price': {'title': 'Price', 'type': 'integer'}, 'step_size': {'title': 'Step Size', 'type': 'integer'}, 'type': {'$ref': '#/definitions/TariffDimensionType'}, 'vat': {'default': 0, 'title': 'Vat', 'type': 'integer'}}, 'required': ['type', 'price', 'step_size'], 'title': 'PriceComponent', 'type': 'object'})]), size=None)),
                ('restrictions', django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(default=dict, validators=[ov2xmp.validators.JSONSchemaValidator(limit_value={'definitions': {'DayOfWeek': {'description': 'An enumeration.', 'enum': ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'], 'title': 'DayOfWeek', 'type': 'string'}, 'ReservationRestrictionType': {'description': 'An enumeration.', 'enum': ['RESERVATION', 'RESERVATION_EXPIRES'], 'title': 'ReservationRestrictionType', 'type': 'string'}}, 'properties': {'day_of_week': {'$ref': '#/definitions/DayOfWeek'}, 'end_date': {'title': 'End Date', 'type': 'string'}, 'end_time': {'title': 'End Time', 'type': 'string'}, 'max_current': {'title': 'Max Current', 'type': 'integer'}, 'max_duration': {'title': 'Max Duration', 'type': 'integer'}, 'max_kwh': {'title': 'Max Kwh', 'type': 'integer'}, 'max_power': {'title': 'Max Power', 'type': 'integer'}, 'min_current': {'title': 'Min Current', 'type': 'integer'}, 'min_duration': {'title': 'Min Duration', 'type': 'integer'}, 'min_kwh': {'title': 'Min Kwh', 'type': 'integer'}, 'min_power': {'title': 'Min Power', 'type': 'integer'}, 'reservation': {'$ref': '#/definitions/ReservationRestrictionType'}, 'start_date': {'title': 'Start Date', 'type': 'string'}, 'start_time': {'title': 'Start Time', 'type': 'string'}}, 'title': 'TariffRestrictions', 'type': 'object'})]), blank=True, default=list, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('country_code', models.CharField(default='GR', max_length=2)),
                ('party_id', models.CharField(default='DEF', max_length=3)),
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('currency', models.CharField(default='EUR', max_length=3)),
                ('type', models.CharField(choices=[('AD_HOC_PAYMENT', 'Ad Hoc Payment'), ('PROFILE_CHEAP', 'Profile Cheap'), ('PROFILE_FAST', 'Profile Fast'), ('PROFILE_GREEN', 'Profile Green'), ('REGULAR', 'Regular')], default='REGULAR', max_length=15)),
                ('tariff_alt_text', django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(), size=None)),
                ('min_price', models.JSONField(blank=True, null=True)),
                ('max_price', models.JSONField(blank=True, null=True)),
                ('start_date_time', models.DateTimeField(blank=True, null=True)),
                ('end_date_time', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField()),
                ('elements', models.ManyToManyField(to='ocpi.tariffelement')),
            ],
        ),
    ]
