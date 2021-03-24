from address.services.address_service import AddressService
from company.models.company import Company
from company.serializers import CompanySerializer
from company.services.company_logistic_info_service import CompanyLogisticInfoService
from exceptions import CompanyException, CompanyError
from utils.base_models import StatusBase
from utils.responses import get_paginated_data


class CompanyService:
    def __init__(self, data):
        self.data = data

    '''get company address'''
    def get_address(company_data):
        for company in company_data:
            company_id = int(company['id'])
            address_data = AddressService.get(entity_type='company',
                                              entity_id=company_id)
            if address_data:
                address_data['street'] = address_data.pop('address1')
            company['address_details'] = address_data

    '''get company details'''

    def get(self, fields=None, address_details=None, **kwargs):
        company = Company.find_by(
            multi=True, status=StatusBase.ACTIVE, **kwargs)

        if 'id' in kwargs and not company:
            raise CompanyException(CompanyError.COMPANY_NOT_FOUND)

        id = kwargs['id'] if 'id' in kwargs else None
        company_paginated_data = get_paginated_data(CompanySerializer, company, self.data, id, fields=fields)

        if company_paginated_data or address_details:
            company_data = [company_paginated_data] if 'id' in kwargs else company_paginated_data
            if address_details is not None:
                CompanyService.get_address(company_data=company_data)
            return company_data[0] if 'id' in kwargs else company_data

        else:
            return False

    '''delete company'''
    def delete(company_id):
        company = Company.find_by(id=company_id, status=StatusBase.ACTIVE)
        company.status = StatusBase.INACTIVE
        company.save()
        CompanyLogisticInfoService.delete(company_id=company_id)
