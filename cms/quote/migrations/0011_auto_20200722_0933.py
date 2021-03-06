# Generated by Django 2.2.5 on 2020-07-22 09:33

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0010_auto_20200714_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='is_depreference',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='is_preference',
        ),
        migrations.AlterField(
            model_name='quote',
            name='expected_arrival_date',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.date(2020, 7, 22))]),
        ),
        migrations.AlterField(
            model_name='quote',
            name='expected_delivery_date',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.date(2020, 7, 22))]),
        ),
        migrations.AlterField(
            model_name='quote',
            name='quote_deadline',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.date(2020, 7, 22))]),
        ),
    ]
