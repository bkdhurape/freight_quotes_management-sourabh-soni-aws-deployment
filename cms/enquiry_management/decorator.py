from enquiry_management.models.company_expertise import CompanyExpertise
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from exceptions import EnquiryManagementException, EnquiryManagementError
from functools import wraps
from utils.base_models import StatusBase

def validate_company_expertise_id(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not CompanyExpertise.objects.filter(company=kwargs['company_id'], id=kwargs['expertise_id'], status=StatusBase.ACTIVE).exists():
            raise EnquiryManagementException(EnquiryManagementError.COMPANY_EXPERTISE_NOT_FOUND)
        return function(*args, **kwargs)
    return wrapper
