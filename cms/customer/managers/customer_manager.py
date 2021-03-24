from address.models.address import Address
from company.models.company import Company
from company.models.company_logistic_info import CompanyLogisticInfo
from company.models.organization import Organization
from currency.models.currency_profile import CurrencyProfile
from department.models.department import Department
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from exceptions.customer_exceptions import CustomerException, CustomerError
from freight.freight_manager import FreightManager
from notification.managers.email_manager import EmailNotification
from utils.helpers import generate_token_data, encode_password
import datetime


class CustomerManager(FreightManager):
    """Customer Data manager used for doing db operation."""

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise CustomerException(CustomerError.CUSTOMER_NOT_FOUND)

    @classmethod
    def find_by_ids(cls, id):
        try:
            if isinstance(id, list):
                return cls.objects.filter(id__in=id)
            else:
                return cls.objects.get(id=id)
        except ObjectDoesNotExist:
            raise CustomerException(CustomerError.CUSTOMER_NOT_FOUND)


class CustomerServiceManager(models.Manager):
    """Customer model manager"""
    department_list = ['Accounts', 'Logistics',
                       'Purchase', 'Supply_chain', 'Management']

    def _create_company(self, **kwargs):
        """
        Create new company along with its default departments.
        :param **kwargs: dict: Company model parameters.
        :return: company object
        """
        company_obj = Company(**kwargs)
        company_obj.save()
        departments = [Department(name=name, company=company_obj, type=0) for name in self.department_list]
        Department.objects.bulk_create(departments)
        return company_obj

    def registration(self, customer_details, company_details=None, additional_details=None):
        """
        Manager method for registration of new customer.
        :param customer_details:
        :param company_details:
        :param additional_details:
        :return:
        """
        # Organization creation.
        organization = Organization.objects.create(name=customer_details['company_name'])

        # Company creation.
        company_info = {}
        if company_details:
            company_info = company_details['company_info']
        company_info['organization'] = organization
        company_info['user_type'] = 'customer'
        company_info['name'] = customer_details['company_name']
        company_obj = self._create_company(**company_info)
        del customer_details['company_name']

        # Customer creation
        token_hash, token = generate_token_data(customer_details['email'])  # Generate token from email
        customer_details['registration_token'] = token
        customer_details['token_date'] = datetime.datetime.now()
        customer_details['password'] = encode_password(customer_details['password'])

        customer_details['home_company'] = company_obj
        customer_details['is_super_admin'] = True
        customer_obj = self.model(**customer_details)
        customer_obj.save()
        customer_obj.company.add(company_obj)
        customer_obj.department.add(company_obj.department_set.get(name='Management'))

        # Company Logistic info / Currency Profile creation
        default_currency = customer_details['home_country'].currency_code
        company_logistics = {'company': company_obj,
                             'annaul_logistic_spend_currency': default_currency,
                             'annual_revenue': None}

        currency_profile = {'company': company_obj,
                            'air_currency': default_currency,
                            'lcl_currency': default_currency,
                            'fcl_currency': default_currency}

        currency_profile.update(additional_details['currency_profile_details'] if additional_details else {})
        company_logistics.update(additional_details['company_logistics'] if additional_details else {})
        CompanyLogisticInfo.objects.create(**company_logistics)

        # Currency Profile for Company.
        # For Company
        currency_profile['entity_type'] = 'company'
        currency_profile['entity_id'] = company_obj.id
        currency_profile['company'] = company_obj
        CurrencyProfile.objects.create(**currency_profile)

        # For Customer
        currency_profile['entity_type'] = 'customer'
        currency_profile['entity_id'] = customer_obj.id
        CurrencyProfile.objects.create(**currency_profile)

        # Address creation.
        address_details = company_details.get('address_details', {}) if company_details else {}
        address_details['entity_type'] = 'company'
        address_details['entity_id'] = company_obj.id
        if not address_details.get('country'):
            address_details['country'] = customer_details['home_country']
        address_obj = Address(**address_details)
        address_obj.save()

        # Create activation link
       
        absolute_link = settings.FRONTEND_URL + '/activation/customer/' + str(company_obj.id) + '/' + token_hash
        EmailNotification.verification_email(customer_details,absolute_link)
        return absolute_link
