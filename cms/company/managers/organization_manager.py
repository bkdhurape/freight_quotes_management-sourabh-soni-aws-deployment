from django.core.exceptions import ObjectDoesNotExist
from exceptions import OrganizationException, OrganizationError
from freight.freight_manager import FreightManager


class OrganizationManager(FreightManager):
    '''Company Data manager used for doing db operation.'''
    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise OrganizationException(
                OrganizationError.ORGANIZATION_NOT_FOUND)
