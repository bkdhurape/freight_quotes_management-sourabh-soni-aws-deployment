from company.models.company_logistic_info import CompanyLogisticInfo
from company.models.company import Company
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from exceptions import CompanyLogisticInfoException, CompanyLogisticInfoError
from utils.responses import error_response
from functools import wraps


def validate_company_logistics_info(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not CompanyLogisticInfo.objects.filter(company=kwargs['company_id'], id=kwargs['company_logistic_id']).exists():
            # raise ValidationError('Id does not exists')
            raise CompanyLogisticInfoException(
                CompanyLogisticInfoError.COMPANY_LOGISTIC_INFO_NOT_FOUND)
        return function(*args, **kwargs)
    return wrapper



def validate_company(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not Company.objects.filter(id=kwargs['company_id']).exists():
            return error_response(data="company not found")
        return function(*args, **kwargs)
    return wrapper
