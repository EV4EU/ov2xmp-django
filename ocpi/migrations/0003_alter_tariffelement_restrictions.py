# Generated by Django 5.0.2 on 2024-06-11 11:14

import django.contrib.postgres.fields
import ov2xmp.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocpi', '0002_alter_tariff_id_alter_tariff_last_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tariffelement',
            name='restrictions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(default=dict, validators=[ov2xmp.validators.JSONSchemaValidator(limit_value={'definitions': {'DayOfWeek': {'description': 'An enumeration.', 'enum': ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'], 'title': 'DayOfWeek', 'type': 'string'}, 'ReservationRestrictionType': {'description': 'An enumeration.', 'enum': ['RESERVATION', 'RESERVATION_EXPIRES'], 'title': 'ReservationRestrictionType', 'type': 'string'}}, 'properties': {'day_of_week': {'$ref': '#/definitions/DayOfWeek'}, 'end_date': {'title': 'End Date', 'type': 'string'}, 'end_time': {'title': 'End Time', 'type': 'string'}, 'max_current': {'title': 'Max Current', 'type': 'integer'}, 'max_duration': {'title': 'Max Duration', 'type': 'integer'}, 'max_kwh': {'title': 'Max Kwh', 'type': 'integer'}, 'max_power': {'title': 'Max Power', 'type': 'integer'}, 'min_current': {'title': 'Min Current', 'type': 'integer'}, 'min_duration': {'title': 'Min Duration', 'type': 'integer'}, 'min_kwh': {'title': 'Min Kwh', 'type': 'integer'}, 'min_power': {'title': 'Min Power', 'type': 'integer'}, 'reservation': {'$ref': '#/definitions/ReservationRestrictionType'}, 'start_date': {'title': 'Start Date', 'type': 'string'}, 'start_time': {'title': 'Start Time', 'type': 'string'}}, 'title': 'TariffRestrictions', 'type': 'object'})]), blank=True, default=None, size=None),
        ),
    ]
