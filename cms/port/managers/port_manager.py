from django.core.exceptions import ObjectDoesNotExist
from exceptions.port_exceptions import PortException, PortError
from freight.freight_manager import FreightManager


class PortManager(FreightManager):
    # Vendor Data manager used for doing db operation.

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise PortException(PortError.PORT_NOT_FOUND)
