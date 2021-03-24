from company.models.company import Company
from enquiry_management.models.company_expertise import CompanyExpertise
from enquiry_management.serializers import CompanyExpertiseSerializer
from exceptions import EnquiryManagementException, EnquiryManagementError
from utils.base_models import StatusBase
from utils.responses import get_paginated_data


class CompanyExpertiseService:

    def __init__(self, data):
        self.data = data

    def get(self, company_id, **kwargs):

        Company.find_by(id=company_id, status=StatusBase.ACTIVE)

        company_expertise = CompanyExpertise.find_by(
            multi=True, status=StatusBase.ACTIVE, company=company_id, **kwargs)

        if 'id' in kwargs and not company_expertise:
            raise EnquiryManagementException(EnquiryManagementError.COMPANY_EXPERTISE_NOT_FOUND)

        id = kwargs['id'] if 'id' in kwargs else None
        company_expertise_paginated_data = get_paginated_data(
            CompanyExpertiseSerializer,company_expertise, self.data, id)

        return company_expertise_paginated_data

    # Delete company expertise details based on company id and company expertise id

    def delete(self, company_id, id):
        Company.find_by(id=company_id, status=StatusBase.ACTIVE)
        company_expertise_data = CompanyExpertise.find_by(
            company=company_id, id=id)

        company_expertise_data.delete()
