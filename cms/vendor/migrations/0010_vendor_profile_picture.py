# Generated by Django 2.2.5 on 2020-12-03 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0009_auto_20201130_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='vendor/images/%Y/%m/%d/'),
        ),
    ]
