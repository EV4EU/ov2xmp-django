# Generated by Django 4.2 on 2023-08-02 13:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('heartbeat', '0002_rename_chargepoint_id_heartbeat_chargepoint'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='heartbeat',
            name='id',
        ),
        migrations.AddField(
            model_name='heartbeat',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
