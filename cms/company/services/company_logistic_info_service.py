from company.models import CompanyLogisticInfo
from company.serializers import CompanyLogisticInfoSerializer
from country.models.country import Country
from currency.models.currency_profile import CurrencyProfile
from currency.services.currency_profile_service import CurrencyProfileService
from django.core.exceptions import ObjectDoesNotExist
from exceptions import CompanyLogisticInfoException, CompanyLogisticInfoError
from utils.base_models import StatusBase


class CompanyLogisticInfoService:
    def __init__(self, data):
        self.data = data

    def details_and_currency_profile(company_id, company_logistic_info):

        # currency profile get
        currency_profile = CurrencyProfileService.get_currency_profile(
            entity_type='company', entity_id=company_id)
        result = {
            'additional_details': company_logistic_info,
            'currency_profile_detail': currency_profile[0]
        }
        return result
    # '''get logistic detail details based on company id  and company logistic id'''

    def get_details(company_id, id):
        company_logistic_info = CompanyLogisticInfo.find_by(
            status=StatusBase.ACTIVE, company_id=company_id, id=id)
        company_logistic_info_serializer = CompanyLogisticInfoSerializer(
            company_logistic_info)
        company_logistic_data = company_logistic_info_serializer.data

        return CompanyLogisticInfoService.details_and_currency_profile(company_id, company_logistic_data)

    # '''get logistic detail details based on company id'''

    def get(company_id):

        company_logistic_info = CompanyLogisticInfo.find_by(
            status=StatusBase.ACTIVE, company_id=company_id)
        if not company_logistic_info:
            raise CompanyLogisticInfoException(
                CompanyLogisticInfoError.COMPANY_LOGISTIC_INFO_NOT_FOUND)

        company_logistic_info_serializer = CompanyLogisticInfoSerializer(
            company_logistic_info)
        company_logistic_data = company_logistic_info_serializer.data
        return CompanyLogisticInfoService.details_and_currency_profile(company_id, company_logistic_data)

    '''To create logistic info for a company'''
    def create(data, company_id, country_id):
        data['company'] = company_id
        country = Country.objects.get(pk=country_id)
        home_country_currency = country.currency_code


        '''Based on home country set  default annual logistic spend currency'''
        data.update({"annaul_logistic_spend_currency": data['annaul_logistic_spend_currency']}) if 'annaul_logistic_spend_currency' in data and data['annaul_logistic_spend_currency'] else data.update(
            {"annaul_logistic_spend_currency": home_country_currency, "annual_revenue_currency":home_country_currency})

        company_logistic_info_serializer = CompanyLogisticInfoSerializer(
            data=data)
        if company_logistic_info_serializer.is_valid(raise_exception=True):
            company_logistic_info_serializer.save()

        '''Saving company currency information'''
        CurrencyProfileService.set_currency(
            data, company_id, 'company', company_id, country_id)

    def delete(company_id):
        company_logistic_info = CompanyLogisticInfo.find_by(
            company_id=company_id, multi=False, join=False)
        company_logistic_info.status = StatusBase.INACTIVE
        company_logistic_info.save()

    def update_company_currency_profile(data, company_id):
        if 'currency_profile_detail' in data and data['currency_profile_detail']:
            req_currency_profile_data = data['currency_profile_detail']
            req_currency_profile_data.update(
                {'entity_type': 'company', 'entity_id': company_id, 'company': company_id})
            currency_id = list(CurrencyProfile.find_by(multi=True, company=company_id,
                                                       entity_id=company_id, entity_type="company").values_list('id', flat=True))[0]
            currency_profile_service = CurrencyProfileService(
                data=req_currency_profile_data)
            currency_profile_service.update(
                entity_type='company', entity_id=company_id, id=currency_id)

    def update(data, company_id, id):
        data['company'] = company_id
        
        '''set default value '''
        CompanyLogisticInfoService.set_default_company_logistic_fields(data)

        company_logistic_info = CompanyLogisticInfo.find_by(
            status=StatusBase.ACTIVE, company_id=company_id, id=id)
        company_logistic_info_serializer = CompanyLogisticInfoSerializer(
            company_logistic_info, data=data)
        if company_logistic_info_serializer.is_valid(raise_exception=True):
            company_logistic_info_serializer.save()
        CompanyLogisticInfoService.update_company_currency_profile(
            data=data, company_id=company_id)

    def set_default_company_logistic_fields(data):
        if 'annual_logistic_spend' not in data or data['annual_logistic_spend'] == "" or data['annual_logistic_spend'] is None:
            data['annual_logistic_spend'] = 0

        if 'annual_air_shipments' not in data or data['annual_air_shipments'] == "" or data['annual_air_shipments'] is None:
            data['annual_air_shipments'] = 0

        if 'annual_lcl_shipments' not in data or data['annual_lcl_shipments'] == "" or data['annual_lcl_shipments'] is None:
            data['annual_lcl_shipments'] = 0

        if 'annual_fcl_shipments' not in data or data['annual_fcl_shipments'] == "" or data['annual_fcl_shipments'] is None:
            data['annual_fcl_shipments'] = 0

        if 'annual_air_volume' not in data or data['annual_air_volume'] == "" or data['annual_air_volume'] is None:
            data['annual_air_volume'] = 0

        if 'annual_lcl_volume' not in data or data['annual_lcl_volume'] == "" or data['annual_lcl_volume'] is None:
            data['annual_lcl_volume'] = 0

        if 'annual_fcl_volume' not in data or data['annual_fcl_volume'] == "" or data['annual_fcl_volume'] is None:
            data['annual_fcl_volume'] = 0
