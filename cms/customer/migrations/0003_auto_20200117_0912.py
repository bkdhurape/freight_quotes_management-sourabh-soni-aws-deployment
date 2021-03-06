# Generated by Django 2.2.5 on 2020-01-17 09:12

import customer.validations
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20200115_1214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='contact_no_dial_code',
        ),
        migrations.AlterField(
            model_name='customer',
            name='contact_no',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True, validators=[customer.validations.CustomerValidation.validate_contact_no]),
        ),
    ]
