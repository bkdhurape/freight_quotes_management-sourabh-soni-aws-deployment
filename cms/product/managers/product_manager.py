from django.core.exceptions import ObjectDoesNotExist
from exceptions.product_exceptions import ProductException, ProductError
from freight.freight_manager import FreightManager


class ProductManager(FreightManager):
    # Vendor Data manager used for doing db operation.

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise ProductException(ProductError.PRODUCT_NOT_FOUND)
