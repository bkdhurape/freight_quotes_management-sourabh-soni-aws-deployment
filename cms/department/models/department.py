from company.models.company import Company
from department.managers.department_manager import DepartmentManager, DepartmentServiceManager
from django.contrib.postgres.fields import CICharField
from django.db import models
from utils.base_models import StatusBase


class Department(StatusBase, DepartmentManager):
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING)

    name = CICharField(max_length=255)

    DEFAULT = 0
    CUSTOM = 1

    TYPE_CHOICES = (
        (DEFAULT, 'Default'),
        (CUSTOM, 'Custom')
    )
    type = models.IntegerField(choices=TYPE_CHOICES, default=CUSTOM)

    objects = models.Manager()  # The default manager.
    services = DepartmentServiceManager()

    class Meta:
        db_table = 'departments'
        unique_together = (('company', 'name'))

    def __str__(self):
        return self.name
