# Generated by Django 2.2.5 on 2020-04-23 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0002_auto_20200423_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='status',
            field=models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active'), (2, 'Pending')], default=2),
        ),
    ]