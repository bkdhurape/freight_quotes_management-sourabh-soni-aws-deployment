from django.core.exceptions import ObjectDoesNotExist
from exceptions.vendor_exceptions import VendorException, VendorError
from freight.freight_manager import FreightManager


class VendorCompaniesModeManager(FreightManager):
    # Vendor Companies Mode Manager Data manager used for doing db operation.

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise VendorException(VendorError.VENDOR_EXPERTISE_TRANSPORT_MODE_NOT_FOUND)
