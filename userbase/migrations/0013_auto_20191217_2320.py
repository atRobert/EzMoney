# Generated by Django 2.2.5 on 2019-12-18 07:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userbase', '0012_auto_20191217_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergoal',
            name='save_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 15, 7, 20, 12, 812262, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userpay',
            name='date_added',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
