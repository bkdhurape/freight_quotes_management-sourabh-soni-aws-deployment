# Generated by Django 2.2.5 on 2020-02-13 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_merge_20200122_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='company',
            field=models.ManyToManyField(blank=True, db_table='customer_companies', related_name='customer_companies', to='company.Company'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='department',
            field=models.ManyToManyField(blank=True, db_table='customer_departments', to='department.Department'),
        ),
    ]
