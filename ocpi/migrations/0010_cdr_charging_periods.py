# Generated by Django 5.1.7 on 2025-03-16 13:33

import django.contrib.postgres.fields
import ov2xmp.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocpi', '0009_remove_cdr_charging_periods_remove_cdr_tariffs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cdr',
            name='charging_periods',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(default=dict, validators=[ov2xmp.validators.JSONSchemaValidator(limit_value={'definitions': {'CdrDimension': {'properties': {'type': {'$ref': '#/definitions/CdrDimensionType'}, 'volume': {'title': 'Volume', 'type': 'number'}}, 'required': ['type', 'volume'], 'title': 'CdrDimension', 'type': 'object'}, 'CdrDimensionType': {'description': 'An enumeration.', 'enum': ['CURRENT', 'ENERGY', 'ENERGY_EXPORT', 'ENERGY_IMPORT', 'MAX_CURRENT', 'MIN_CURRENT', 'MAX_POWER', 'MIN_POWER', 'PARKING_TIME', 'POWER', 'RESERVATION_TIME', 'STATE_OF_CHARGE', 'TIME'], 'title': 'CdrDimensionType', 'type': 'string'}}, 'properties': {'dimensions': {'$ref': '#/definitions/CdrDimension'}, 'start_date_time': {'title': 'Start Date Time', 'type': 'string'}, 'tariff_id': {'title': 'Tariff Id', 'type': 'string'}}, 'required': ['start_date_time', 'dimensions'], 'title': 'ChargingPeriod', 'type': 'object'})]), default=[{}], size=None),
            preserve_default=False,
        ),
    ]
