# Generated by Django 3.2.7 on 2021-09-27 18:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20210923_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 29, 18, 48, 24, 885248, tzinfo=utc)),
        ),
    ]