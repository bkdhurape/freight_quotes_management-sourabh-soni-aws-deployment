from company.models.company import Company
from entity.managers.entity_manager import EntityManager
from django.db import models
from utils.base_models import StatusBase
import hashlib


class Entity(StatusBase, EntityManager):

    id = models.AutoField(primary_key=True, editable=False)
    company = models.ForeignKey(
        Company, blank=False, on_delete=models.DO_NOTHING)
    name = models.CharField(default=None, max_length=255)
    is_shipper = models.BooleanField(default=False)
    is_consignee = models.BooleanField(default=False)

    class Meta:
        db_table = 'entities'
        unique_together = (('company', 'name'))

    def __str__(self):
        return self.name
