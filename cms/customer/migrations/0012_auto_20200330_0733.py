# Generated by Django 2.2.5 on 2020-03-30 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_auto_20200324_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='department',
            field=models.ManyToManyField(db_table='customer_departments', to='department.Department'),
        ),
    ]