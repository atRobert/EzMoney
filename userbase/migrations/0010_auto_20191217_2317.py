# Generated by Django 2.2.5 on 2019-12-18 07:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userbase', '0009_auto_20191217_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='userincome',
            name='after_tax',
            field=models.IntegerField(default=50),
        ),
        migrations.AddField(
            model_name='userincome',
            name='monthly_living',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='userincome',
            name='random_expense',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='userincome',
            name='weekly_food',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='userincome',
            name='weekyl_travel',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='usergoal',
            name='save_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 15, 7, 17, 53, 477980, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userpay',
            name='date_added',
            field=models.DateField(default=datetime.datetime(2019, 12, 18, 7, 17, 53, 477980, tzinfo=utc)),
        ),
    ]
