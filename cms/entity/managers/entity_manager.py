from django.core.exceptions import ObjectDoesNotExist
from exceptions.entity_exceptions import EntityException, EntityError
from freight.freight_manager import FreightManager


class EntityManager(FreightManager):
    # Vendor Data manager used for doing db operation.

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise EntityException(EntityError.ENTITY_NOT_FOUND)
