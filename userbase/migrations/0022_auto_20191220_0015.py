# Generated by Django 2.2.5 on 2019-12-20 08:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userbase', '0021_auto_20191217_2346'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergoal',
            name='current_date',
            field=models.DateField(default=datetime.datetime(2019, 12, 20, 8, 15, 49, 663443, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='usergoal',
            name='save_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 17, 8, 15, 49, 663443, tzinfo=utc)),
        ),
    ]
