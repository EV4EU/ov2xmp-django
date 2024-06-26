# Generated by Django 5.0.2 on 2024-05-07 23:10

import django.contrib.postgres.fields
import django.db.models.deletion
import ov2xmp.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocpi', '0001_initial'),
        ('transaction', '0005_rename_status_transaction_transaction_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tariff',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tariff',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='tariff',
            name='max_price',
            field=models.JSONField(blank=True, default=dict, null=True, validators=[ov2xmp.validators.JSONSchemaValidator(limit_value={'properties': {'excl_vat': {'title': 'Excl Vat', 'type': 'integer'}, 'incl_vat': {'title': 'Incl Vat', 'type': 'integer'}}, 'required': ['excl_vat', 'incl_vat'], 'title': 'Price', 'type': 'object'})]),
        ),
        migrations.AlterField(
            model_name='tariff',
            name='min_price',
            field=models.JSONField(blank=True, default=dict, null=True, validators=[ov2xmp.validators.JSONSchemaValidator(limit_value={'properties': {'excl_vat': {'title': 'Excl Vat', 'type': 'integer'}, 'incl_vat': {'title': 'Incl Vat', 'type': 'integer'}}, 'required': ['excl_vat', 'incl_vat'], 'title': 'Price', 'type': 'object'})]),
        ),
        migrations.AlterField(
            model_name='tariffelement',
            name='price_components',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(default=dict, validators=[ov2xmp.validators.JSONSchemaValidator(limit_value={'definitions': {'TariffDimensionType': {'description': 'An enumeration.', 'enum': ['ENERGY', 'FLAT', 'PARKING_TIME', 'TIME'], 'title': 'TariffDimensionType', 'type': 'string'}}, 'properties': {'price': {'title': 'Price', 'type': 'number'}, 'step_size': {'title': 'Step Size', 'type': 'integer'}, 'type': {'$ref': '#/definitions/TariffDimensionType'}, 'vat': {'default': 0.0, 'title': 'Vat', 'type': 'number'}}, 'required': ['type', 'price', 'step_size'], 'title': 'PriceComponent', 'type': 'object'})]), size=None),
        ),
        migrations.CreateModel(
            name='ChargingPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date_time', models.DateTimeField()),
                ('dimensions', models.JSONField(default=dict, validators=[ov2xmp.validators.JSONSchemaValidator(limit_value={'definitions': {'CdrDimensionType': {'description': 'An enumeration.', 'enum': ['CURRENT', 'ENERGY', 'ENERGY_EXPORT', 'ENERGY_IMPORT', 'MAX_CURRENT', 'MIN_CURRENT', 'MAX_POWER', 'MIN_POWER', 'PARKING_TIME', 'POWER', 'RESERVATION_TIME', 'STATE_OF_CHARGE', 'TIME'], 'title': 'CdrDimensionType', 'type': 'string'}}, 'properties': {'type': {'$ref': '#/definitions/CdrDimensionType'}, 'volume': {'title': 'Volume', 'type': 'number'}}, 'required': ['type', 'volume'], 'title': 'CdrDimension', 'type': 'object'})])),
                ('tariff_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ocpi.tariff')),
            ],
        ),
        migrations.CreateModel(
            name='Cdr',
            fields=[
                ('country_code', models.CharField(default='GR', max_length=2)),
                ('party_id', models.CharField(default='DEF', max_length=3)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_date_time', models.DateTimeField()),
                ('end_date_time', models.DateTimeField()),
                ('auth_method', models.CharField(choices=[('AUTH_REQUEST', 'Auth Request'), ('COMMAND', 'Command'), ('WHITELIST', 'Whitelist')], max_length=15)),
                ('authorization_reference', models.CharField(blank=True, max_length=36, null=True)),
                ('meter_id', models.CharField(blank=True, max_length=3, null=True)),
                ('total_cost', models.JSONField(default=dict, validators=[ov2xmp.validators.JSONSchemaValidator(limit_value={'properties': {'excl_vat': {'title': 'Excl Vat', 'type': 'integer'}, 'incl_vat': {'title': 'Incl Vat', 'type': 'integer'}}, 'required': ['excl_vat', 'incl_vat'], 'title': 'Price', 'type': 'object'})])),
                ('total_fixed_cost', models.JSONField(default=dict, validators=[ov2xmp.validators.JSONSchemaValidator(limit_value={'properties': {'excl_vat': {'title': 'Excl Vat', 'type': 'integer'}, 'incl_vat': {'title': 'Incl Vat', 'type': 'integer'}}, 'required': ['excl_vat', 'incl_vat'], 'title': 'Price', 'type': 'object'})])),
                ('total_energy', models.FloatField()),
                ('total_energy_cost', models.JSONField(default=dict, validators=[ov2xmp.validators.JSONSchemaValidator(limit_value={'properties': {'excl_vat': {'title': 'Excl Vat', 'type': 'integer'}, 'incl_vat': {'title': 'Incl Vat', 'type': 'integer'}}, 'required': ['excl_vat', 'incl_vat'], 'title': 'Price', 'type': 'object'})])),
                ('total_time', models.FloatField()),
                ('total_time_cost', models.JSONField(default=dict, validators=[ov2xmp.validators.JSONSchemaValidator(limit_value={'properties': {'excl_vat': {'title': 'Excl Vat', 'type': 'integer'}, 'incl_vat': {'title': 'Incl Vat', 'type': 'integer'}}, 'required': ['excl_vat', 'incl_vat'], 'title': 'Price', 'type': 'object'})])),
                ('total_parking_time', models.FloatField(blank=True, null=True)),
                ('total_parking_cost', models.JSONField(default=dict, validators=[ov2xmp.validators.JSONSchemaValidator(limit_value={'properties': {'excl_vat': {'title': 'Excl Vat', 'type': 'integer'}, 'incl_vat': {'title': 'Incl Vat', 'type': 'integer'}}, 'required': ['excl_vat', 'incl_vat'], 'title': 'Price', 'type': 'object'})])),
                ('total_reservation_cost', models.JSONField(default=dict, validators=[ov2xmp.validators.JSONSchemaValidator(limit_value={'properties': {'excl_vat': {'title': 'Excl Vat', 'type': 'integer'}, 'incl_vat': {'title': 'Incl Vat', 'type': 'integer'}}, 'required': ['excl_vat', 'incl_vat'], 'title': 'Price', 'type': 'object'})])),
                ('remark', models.CharField(blank=True, max_length=255, null=True)),
                ('credit', models.BooleanField(default=False)),
                ('credit_reference_id', models.CharField(blank=True, max_length=39, null=True)),
                ('home_charging_compensation', models.BooleanField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('session_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.transaction')),
                ('tariffs', models.ManyToManyField(to='ocpi.tariff')),
                ('charging_periods', models.ManyToManyField(to='ocpi.chargingperiod')),
            ],
        ),
    ]
