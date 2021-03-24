# Generated by Django 2.2.5 on 2020-02-27 07:18

from django.db import migrations, models
import django.db.models.deletion
import entity.managers.entity_manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0007_auto_20200221_0641'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='system', max_length=512)),
                ('updated_by', models.CharField(default='system', max_length=512)),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=255)),
                ('is_shipper', models.BooleanField(default=False)),
                ('is_consignee', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='company.Company')),
            ],
            options={
                'db_table': 'entities',
                'unique_together': {('company', 'name')},
            },
            bases=(models.Model, entity.managers.entity_manager.EntityManager),
        ),
    ]
