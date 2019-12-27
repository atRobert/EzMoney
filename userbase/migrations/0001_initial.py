# Generated by Django 2.2.5 on 2019-12-16 08:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income_type', models.CharField(choices=[('salary', 'Salary'), ('hourly', 'Hourly')], max_length=32)),
                ('pay_cycle', models.CharField(choices=[('weekly', 'Weekly'), ('biweekly', 'Biweekly'), ('twice', 'Twice a month'), ('monthly', 'Monthly')], max_length=32)),
                ('income_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('current_savings', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('save_percent', models.IntegerField(default=50)),
                ('save_date', models.DateField(default=datetime.datetime(2020, 1, 15, 8, 27, 31, 468291, tzinfo=utc))),
                ('goal_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
