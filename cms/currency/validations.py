from company.models.company import Company
from exceptions.company_exceptions import CompanyException, CompanyError
from exceptions.currency_exceptions import CurrencyException, CurrencyError
from utils.base_models import StatusBase


class CurrencyValidation:

    # Validate companies currency
    def validate_companies_currency(request_data, organization_id):
        company_list = list(Company.find_by(multi=True, organization=organization_id, status=StatusBase.ACTIVE).values_list('id', flat=True))

        if ('user_companies_currency' not in request_data) or (not request_data['user_companies_currency']):
            raise CurrencyException(CurrencyError.COMPANIES_CURRENCY_REQUIRED)

        currency_fields = ['air_currency', 'lcl_currency', 'fcl_currency']
        for company in request_data['user_companies_currency']:
            if int(list(company.keys())[0]) not in company_list:
                raise CompanyException(CompanyError.COMPANY_NOT_FOUND)
            for key, value in (list(company.values())[0]).items():
                if (key not in currency_fields) or (not value):
                    raise CurrencyException(CurrencyError.COMPANIES_CURRENCY_REQUIRED)
