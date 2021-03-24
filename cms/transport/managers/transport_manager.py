from django.core.exceptions import ObjectDoesNotExist
from freight.freight_manager import FreightManager
from exceptions import TransportException, TransportError


class TransportManager(FreightManager):
    """Transport Data manager used for doing db operation."""

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise TransportException(TransportError.TRANSPORT_NOT_FOUND)
