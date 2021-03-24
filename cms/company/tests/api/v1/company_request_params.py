from country.models.country import Country
from django.conf import settings


class CompanyRequestParams:

    @staticmethod
    def api_url():
        return settings.API_HOST

    def create_company_with_invalid_industry_and_business_activity_params():
        request_response = CompanyRequestParams.create_company_valid_response()
        request_response['industry'] = ["consumer_goods_or_fmcg_2", "engineering_and_manufacturing", "retail"]
        request_response['business_activity'] = ["manufacturer_2", "supplier", "wholesaler"]
        return request_response

    def create_company_with_invalid_industry_and_business_activity_null_params():
        request_response = CompanyRequestParams.create_company_valid_response()
        request_response['name'] = 'company_o1cA'
        request_response['industry'] = None
        request_response['business_activity'] = None
        return request_response
