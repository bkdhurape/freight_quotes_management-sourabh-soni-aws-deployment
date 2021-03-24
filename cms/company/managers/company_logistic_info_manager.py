from currency.models.currency_profile import CurrencyProfile
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from exceptions import CompanyLogisticInfoException, CompanyLogisticInfoError
from freight.freight_manager import FreightManager


class CompanyLogisticInfoManager(FreightManager):
    '''Company logistic Data manager used for doing db operation.'''
    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise CompanyLogisticInfoException(
                CompanyLogisticInfoError.COMPANY_LOGISTIC_INFO_NOT_FOUND)


class CompanyAdditionalDetailServiceManager(models.Manager):

    def update_additional_detail(self, company_id, id, company_logistics, currency_profile_details):

        # Update company logistics
        self.model.objects.filter(id=id).update(**company_logistics)

        # Update Currency profile details
        currency_profile_details.update(
            {'entity_type': 'company', 'entity_id': company_id})
        CurrencyProfile.objects.filter(
            company=company_id).update(**currency_profile_details)
