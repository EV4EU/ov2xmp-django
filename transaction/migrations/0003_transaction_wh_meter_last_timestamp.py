# Generated by Django 4.2.4 on 2023-08-21 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_transaction_connector'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='wh_meter_last_timestamp',
            field=models.DateTimeField(default='2023-08-21T09:57:09.441864'),
            preserve_default=False,
        ),
    ]
