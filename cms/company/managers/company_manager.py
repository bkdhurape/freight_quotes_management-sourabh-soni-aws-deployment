from address.models.address import Address
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from exceptions import CompanyException, CompanyError
from freight.freight_manager import FreightManager


class CompanyManager(FreightManager):
    ''' company Data manager used for doing db operation.'''
    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise CompanyException(CompanyError.COMPANY_NOT_FOUND)


class CompanyServiceManager(models.Manager):
    """Customer model manager"""
    department_list = ['Accounts', 'Logistics',
                       'Purchase', 'Supply_chain', 'Management']

    def add_company(self, company_details, address_details):

        # add company.
        company_obj = self.model.objects.create(**company_details)

        # If type is customer then, five default department will be created
        if company_details['user_type'] == 'customer':
            departments = [apps.get_model('department', 'Department')(name=name, company=company_obj, type=0)
                        for name in self.department_list]
            apps.get_model('department', 'Department').objects.bulk_create(
                departments)

        # add Address.
        address_details['entity_type'] = 'company'
        address_details['entity_id'] = company_obj.id
        Address.objects.create(**address_details)


        # Company Logistic info creation based on company id and user type
        default_currency = address_details['country'].currency_code
        company_logistics = {}
        if company_details['user_type'] == 'customer':
            annaul_logistic_spend_currency = default_currency
            annual_revenue_currency = None
            company_logistics.update({'annual_revenue':None})

        if company_details['user_type'] == 'vendor':
            annual_revenue_currency = default_currency
            annaul_logistic_spend_currency = None
            company_logistics.update({'annual_logistic_spend':None})
       
        company_logistics.update({'company': company_obj,
                             'annaul_logistic_spend_currency': annaul_logistic_spend_currency,
                             'annual_revenue_currency': annual_revenue_currency})

        apps.get_model('company', 'CompanyLogisticInfo').objects.create(**company_logistics)

        # Currency Profile for Company creation.
        currency_profile = {'company': company_obj,
                            'air_currency': default_currency,
                            'lcl_currency': default_currency,
                            'fcl_currency': default_currency,
                            'entity_type': 'company',
                            'entity_id': company_obj.id}

        apps.get_model('currency', 'CurrencyProfile').objects.create(
            **currency_profile)

    def update_company(self, company_details, address_details, id):
        company_obj = self.model.objects.get(id=id)

        for company_detail in company_details:
            setattr(company_obj, company_detail, company_details[company_detail])
        company_obj.save()

        # Address updation.
        address_details['entity_type'] = 'company'
        address_details['entity_id'] = id
        Address.objects.filter(entity_type='company',
                               entity_id=id).update(**address_details)
