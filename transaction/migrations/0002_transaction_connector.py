# Generated by Django 4.2 on 2023-07-31 23:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0001_initial'),
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='connector',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='connector.connector'),
        ),
    ]
