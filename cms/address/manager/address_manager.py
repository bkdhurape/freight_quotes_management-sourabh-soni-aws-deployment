from django.core.exceptions import ObjectDoesNotExist
from exceptions import AddressException, AddressError
from freight.freight_manager import FreightManager


class AddressManager(FreightManager):
    '''Address Data manager used for doing db operation.'''
    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise AddressException(AddressError.ADDRESS_NOT_FOUND)
        