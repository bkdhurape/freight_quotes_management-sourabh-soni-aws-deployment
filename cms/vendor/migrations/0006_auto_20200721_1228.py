# Generated by Django 2.2.5 on 2020-07-21 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_auto_20200403_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='forgot_password_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='forgot_password_link',
            field=models.CharField(default=None, max_length=1024, null=True),
        ),
    ]