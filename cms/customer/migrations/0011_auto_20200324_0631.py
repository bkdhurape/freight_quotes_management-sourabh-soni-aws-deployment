# Generated by Django 2.2.5 on 2020-03-24 06:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_merge_20200217_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='landline_no',
            field=models.CharField(blank=True, default=None, max_length=12, null=True, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.RegexValidator(regex='\\d{10}')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='landline_no_dial_code',
            field=models.CharField(blank=True, default=None, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(default=None, max_length=255, validators=[django.core.validators.MinLengthValidator(4), django.core.validators.RegexValidator(regex='^[A-Za-z]+[A-Za-z\\d\\._\\s]+$')]),
        ),
    ]
