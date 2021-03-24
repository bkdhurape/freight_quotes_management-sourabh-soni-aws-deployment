from django.core.exceptions import ValidationError
from rest_framework.response import Response
from company.models.company import Company
from utils.responses import error_response
from functools import wraps
from rest_framework import status
from quote.models.quote import Quote
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from exceptions.quote_exceptions import QuoteException, QuoteError
from functools import wraps
from utils.base_models import StatusBase
from django.db.models import Q


def validate_company(function):
    """
    Decorator to check if company is valid or not
    :param function:
    :type function:
    :return:
    :rtype:
    """
    @wraps(function)
    def wrap(*args, **kwargs):
        if not Company.objects.filter(id=kwargs['company_id']).exists():
            return error_response(data="Invalid company.", status_code=status.HTTP_403_FORBIDDEN)
        return function(*args, **kwargs)

    return wrap


def validate_quote_info(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not Quote.objects.filter(~Q(status=StatusBase.INACTIVE), company=kwargs['company_id'], id=kwargs['quote_id']).exists():
            raise QuoteException(
                QuoteError.QUOTE_NOT_FOUND)
        return function(*args, **kwargs)
    return wrapper
