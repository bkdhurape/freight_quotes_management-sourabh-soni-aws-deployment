from django.contrib.postgres.fields import ArrayField
from django.db import models
from entity.models.entity import Entity
from port.models.port import Port
from product.managers.product_manager import ProductManager
from utils.base_models import StatusBase
import hashlib


class Product(StatusBase, ProductManager):

    TRANSPORT_MODE_CHOICES = [
        ('Air', 'Air'),
        ('FCL', 'FCL'),
        ('LCL', 'LCL'),
    ]

    id = models.AutoField(primary_key=True, editable=False)
    entity = models.ForeignKey(Entity, blank=False, on_delete=models.DO_NOTHING)
    name = models.CharField(default=None, max_length=255)
    transport_modes = ArrayField(models.CharField(max_length=255, choices=TRANSPORT_MODE_CHOICES, default=None, null=False))
    airports = models.ManyToManyField(Port, blank=True, related_name='product_airports', db_table='product_airports')
    seaports = models.ManyToManyField(Port, blank=True, db_table='product_seaports')

    class Meta:
        db_table = 'products'
        unique_together = (('entity', 'name')) 

    def __str__(self):
        return self.name
