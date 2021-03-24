from contact_person.models.contact_person import ContactPerson
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from exceptions.contact_person_exceptions import ContactPersonException, ContactPersonError
from functools import wraps
from utils.base_models import StatusBase


def validate_contact_info(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not ContactPerson.objects.filter(company=kwargs['company_id'], id=kwargs['contact_person_id'], status=StatusBase.ACTIVE).exists():
            # raise ValidationError('Id does not exists')
            raise ContactPersonException(
                ContactPersonError.CONTACT_PERSON_NOT_FOUND)
        return function(*args, **kwargs)
    return wrapper