from freight.freight_manager import FreightManager
from django.core.exceptions import ObjectDoesNotExist
from exceptions.currency_exceptions import CurrencyException, CurrencyError


class CurrencyManager(FreightManager):
    """Currency Data manager used for doing db operation."""

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise CurrencyException(CurrencyError.CURRENCY_NOT_FOUND)

    @classmethod
    def find_by_ids(cls, id):
        if isinstance(id, list):
            return cls.objects.filter(id__in=id)
        else:
            return cls.objects.get(id=id)
