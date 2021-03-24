from django.core.exceptions import ObjectDoesNotExist
from exceptions.vendor_type_exceptions import VendorTypeException, VendorTypeError
from freight.freight_manager import FreightManager


class VendorTypeManager(FreightManager):
    # Vendor Data manager used for doing db operation.

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise VendorTypeException(VendorTypeError.VENDOR_TYPE_NOT_FOUND)

    @classmethod
    def find_by_ids(cls, id):
        try:
            if isinstance(id, list):
                return cls.objects.filter(id__in=id)
            else:
                return cls.objects.get(id=id)
        except ObjectDoesNotExist:
            raise VendorTypeException(VendorTypeError.VENDOR_TYPE_NOT_FOUND)
