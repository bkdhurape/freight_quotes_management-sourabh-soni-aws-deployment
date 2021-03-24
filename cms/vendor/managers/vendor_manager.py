from address.models.address import Address
from commodity.models.commodity import Commodity
from company.models.company import Company
from company.models.company_logistic_info import CompanyLogisticInfo
from company.models.organization import Organization
from country.models.country import Country
from currency.models.currency_profile import CurrencyProfile
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from enquiry_management.models.company_expertise import CompanyExpertise
from exceptions.vendor_exceptions import VendorException, VendorError
from freight.freight_manager import FreightManager
from utils.base_models import StatusBase,QuoteChoice
from utils.helpers import generate_token_data, encode_password
import datetime


class VendorManager(FreightManager):
    # Vendor Data manager used for doing db operation.

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise VendorException(VendorError.VENDOR_NOT_FOUND)

    @classmethod
    def find_by_ids(cls, id):
        try:
            if isinstance(id, list):
                return cls.objects.filter(id__in=id)
            else:
                return cls.objects.get(id=id)
        except ObjectDoesNotExist:
            raise VendorException(VendorError.VENDOR_NOT_FOUND)


class VendorServiceManager(models.Manager):
    
    def _create_company(self, **kwargs):
        """
        :param **kwargs: dict: Company model parameters.
        :return: company object
        """
        company_obj = Company(**kwargs)
        company_obj.save()
        return company_obj

    def registration(self, vendor_details, address_details):

        # Organization creation.
        organization = Organization.objects.create(name=vendor_details['company_name'])

        # Company creation.
        company_info = {} 
        company_info['organization'] = organization
        company_info['user_type'] = 'vendor'
        company_info['name'] = vendor_details['company_name']
        company_obj = self._create_company(**company_info)
        del vendor_details['company_name']

        # Validate vendor type and assign
        country = address_details['country']
        country_code = country.code

        if vendor_details['vendor_type'] == 'freight_forwarder' and country_code != 'IN':
            vendor_details['vendor_type'] = 'foreign_agent'

        # Vendor creation
        token_hash, token = generate_token_data(vendor_details['email'])  # Generate token from email
        vendor_details['registration_token'] = token
        vendor_details['token_date'] = datetime.datetime.now()
        vendor_details['password'] = encode_password(vendor_details['password'])

        vendor_details['home_company'] = company_obj
        vendor_details['is_super_admin'] = True
        vendor_obj = self.model(**vendor_details)
        vendor_obj.save()
        vendor_obj.company.add(company_obj)
        
        # Enquiry management creation based on vendor type and company id
        if (vendor_details['vendor_type'] == 'freight_forwarder' or vendor_details['vendor_type'] == 'foreign_agent'):
            transport_modes = ['AI', 'AE', 'LCLI', 'LCLE', 'FCLI','FCLE', 'ACI', 'ACE', 'ATC', 'ACTC', 'LCLTC', 'FCLTC']

        elif (vendor_details['vendor_type'] == 'courier'):
            transport_modes = ['ACI', 'ACE', 'ACTC']

        elif(vendor_details['vendor_type'] == 'customs' or vendor_details['vendor_type'] == 'transport_only'):
            transport_modes = ['AI', 'AE', 'LCLI', 'LCLE', 'FCLE', 'FCLI']

        # Creation of Company expertise based on transport modes, weight, weight_unit
        commodity = list(Commodity.objects.values_list('id', flat=True).order_by('id'))
        country = list(Country.objects.values_list('id', flat=True).order_by('id'))
        container_type=list(dict(QuoteChoice.CONTAINER_TYPE_CHOICES))
        company_expertise_data = {}
        for transport_mode in transport_modes:

            if transport_mode in ['FCLI', 'FCLE', 'FCLTC']:
                company_expertise_data.update(
                    {'container_type': container_type,
                     'temperature_controlled':None
                    })

            if transport_mode in ['ATC', 'FCLTC', 'LCLTC', 'ACTC']:
                company_expertise_data.update(
                    {'instant_quotes': False})

            company_expertise_data.update({
                'transport_mode': transport_mode,
                'company': company_obj
            }) 

            company_expertise_object = CompanyExpertise(company_id = company_obj.id, **company_expertise_data)
            company_expertise_object.save()
            
            company_expertise_object.commodity.set(commodity)

            if transport_mode in ['ATC', 'FCLTC', 'LCLTC', 'ACTC']:
                company_expertise_object.to_trade_lanes.set(country)
                company_expertise_object.from_trade_lanes.set(country)

            if transport_mode in ['AI', 'FCLI', 'LCLI', 'ACI', 'AE', 'FCLE', 'LCLE', 'ACE']:
                company_expertise_object.trade_lanes.set(country)


        # Company Logistic info / Currency Profile creation
        default_currency = address_details['country'].currency_code
        company_logistics = {'company': company_obj,
                             'annual_logistic_spend': None,
                             'annual_revenue_currency': default_currency}
        currency_profile = {'company': company_obj,
                            'air_currency': default_currency,
                            'lcl_currency': default_currency,
                            'fcl_currency': default_currency}

        currency_profile.update(**currency_profile)
        company_logistics.update(**company_logistics)
        CompanyLogisticInfo.objects.create(**company_logistics)


        # Currency Profile for Company.
        # For Company
        currency_profile['entity_type'] = 'company'
        currency_profile['entity_id'] = company_obj.id
        currency_profile['company'] = company_obj
        CurrencyProfile.objects.create(**currency_profile)

        # For Vendor
        currency_profile['entity_type'] = 'vendor'
        currency_profile['entity_id'] = vendor_obj.id
        CurrencyProfile.objects.create(**currency_profile)

        # Address creation.
        address_details['entity_type'] = 'company'
        address_details['entity_id'] = company_obj.id
        address_obj = Address(**address_details)
        address_obj.save()
        