from customer.models.customer import Customer
from utils.responses import error_response
from functools import wraps
from rest_framework import status


def validate_customer_company(function):
    """
    Decorator to check if company is valid or not
    :param function:
    :type function:
    :return:
    :rtype:
    """
    @wraps(function)
    def wrap(*args, **kwargs):
        if not Customer.objects.filter(id=kwargs['id'], home_company_id=kwargs['company_id']).exists():
            return error_response(data="This customer does not belong to this company.",
                                  status_code=status.HTTP_403_FORBIDDEN)
        return function(*args, **kwargs)

    return wrap
