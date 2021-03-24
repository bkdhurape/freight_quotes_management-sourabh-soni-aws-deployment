from freight.freight_manager import FreightManager
from django.core.exceptions import ObjectDoesNotExist
from exceptions import AddressException, AddressError


class StateManager(FreightManager):
    """State Data manager used for doing db operation."""

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise AddressException(AddressError.STATE_NOT_FOUND)
