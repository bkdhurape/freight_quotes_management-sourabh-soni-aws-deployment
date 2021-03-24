# Generated by Django 2.2.7 on 2020-01-02 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('country', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='system', max_length=512)),
                ('updated_by', models.CharField(default='system', max_length=512)),
                ('name', models.CharField(max_length=256)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='country.Country')),
            ],
            options={
                'db_table': 'states',
            },
        ),
    ]
