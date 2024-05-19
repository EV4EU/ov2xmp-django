# Generated by Django 5.0.2 on 2024-05-08 00:47

import ov2xmp.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0004_location_latitude_location_longitude'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='street_address',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='location',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='location',
            name='longitude',
        ),
        migrations.AddField(
            model_name='location',
            name='coordinates',
            field=models.JSONField(default={'latitude': '3.729944', 'longitude': '51.047599'}, validators=[ov2xmp.validators.JSONSchemaValidator(limit_value={'properties': {'latitude': {'title': 'Latitude', 'type': 'number'}, 'longitude': {'title': 'Longitude', 'type': 'number'}}, 'required': ['latitude', 'longitude'], 'title': 'GeoLocation', 'type': 'object'})]),
            preserve_default=False,
        ),
    ]
