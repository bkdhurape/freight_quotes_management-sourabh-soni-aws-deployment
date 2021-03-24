from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from exceptions.department_exceptions import DepartmentException, DepartmentError
from freight.freight_manager import FreightManager
from utils.base_models import StatusBase


class DepartmentManager(FreightManager):
    """Department Data manager used for doing db operation."""

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise DepartmentException(DepartmentError.DEPARTMENT_NOT_FOUND)

    @classmethod
    def find_by_ids(cls, id):
        if isinstance(id, list):
            return cls.objects.filter(id__in=id)
        else:
            return cls.objects.get(id=id)


class DepartmentServiceManager(models.Manager):
    
    def delete_department(self, company_id, department_id):
        
        active_user = apps.get_model('customer', 'Customer').objects.filter(department=department_id, status=StatusBase.ACTIVE)
        if active_user.exists():
            return False
        else:
            department_object = self.model.objects.get(company_id=company_id, id=department_id)
            department_object.status = StatusBase.INACTIVE
            department_object.save()
            return True