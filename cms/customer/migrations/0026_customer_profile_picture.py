# Generated by Django 2.2.5 on 2020-12-03 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0025_auto_20201130_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='customer/images/%Y/%m/%d/'),
        ),
    ]