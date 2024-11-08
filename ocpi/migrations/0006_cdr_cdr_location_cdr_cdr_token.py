# Generated by Django 5.0.2 on 2024-06-15 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idtag', '0001_initial'),
        ('location', '0008_location_substation_id'),
        ('ocpi', '0005_alter_tariffelement_restrictions'),
    ]

    operations = [
        migrations.AddField(
            model_name='cdr',
            name='cdr_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='location.location'),
        ),
        migrations.AddField(
            model_name='cdr',
            name='cdr_token',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='idtag.idtag'),
        ),
    ]