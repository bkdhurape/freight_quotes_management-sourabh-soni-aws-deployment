from company.managers.organization_manager import OrganizationManager
from django.db import models
from utils.base_models import StatusBase



class Organization(StatusBase,OrganizationManager):
    name = models.CharField(max_length=512)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'organizations'
