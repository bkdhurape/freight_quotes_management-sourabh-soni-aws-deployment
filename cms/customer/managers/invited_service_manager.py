from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from exceptions.invited_vendor_exceptions import InvitedVendorException, InvitedVendorError
from freight.freight_manager import FreightManager


class InvitedVendorManager(FreightManager):
    """Invited Vendo Data manager used for doing db operation."""

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise InvitedVendorException(InvitedVendorError.INVITED_VENDOR_NOT_FOUND)


class InvitedServiceManager(models.Manager):

    def delete(self, company_id, customer_id, id):
        """
        Delete the invited vendor by customer
        :param company_id:
        :type company_id:
        :param customer_id:
        :type customer_id:
        :param id:
        :type id:
        :return:
        :rtype:
        """
        invited_vendor = self.model.objects.filter(customer_company=company_id, customer=customer_id, id=id)
        if invited_vendor:
            invited_vendor.delete()
        return True

