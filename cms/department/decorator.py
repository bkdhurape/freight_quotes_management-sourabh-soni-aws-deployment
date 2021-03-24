from department.models.department import Department
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from exceptions.department_exceptions import DepartmentException, DepartmentError
from functools import wraps
from utils.base_models import StatusBase


def validate_department_info(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not Department.objects.filter(company=kwargs['company_id'], id=kwargs['department_id'], status=StatusBase.ACTIVE).exists():
            # raise ValidationError('Id does not exists')
            raise DepartmentException(
                DepartmentError.DEPARTMENT_NOT_FOUND)
        return function(*args, **kwargs)
    return wrapper
