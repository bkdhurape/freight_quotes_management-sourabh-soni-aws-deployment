from django.core.exceptions import ObjectDoesNotExist
from exceptions import EnquiryManagementException, EnquiryManagementError
from freight.freight_manager import FreightManager


class CompanyExpertiseManager(FreightManager):
    """CompanyExpertise Data manager used for doing db operation."""

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise EnquiryManagementException(
                EnquiryManagementError.COMPANY_EXPERTISE_NOT_FOUND)