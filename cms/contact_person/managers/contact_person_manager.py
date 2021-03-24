from django.core.exceptions import ObjectDoesNotExist
from exceptions import ContactPersonException, ContactPersonError
from freight.freight_manager import FreightManager

class ContactPersonManager(FreightManager):
    #Contact Person Data manager used for doing db operation.

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise ContactPersonException(ContactPersonError.CONTACT_PERSON_NOT_FOUND)
