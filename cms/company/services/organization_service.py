from company.models import Organization
from company.serializers import OrganizationSerializer
from company.services.company_service import CompanyService
from exceptions import OrganizationError, OrganizationException
from utils.base_models import StatusBase

class OrganizationService:
    def __init__(self, data):
        self.data = data

    '''To create organization'''

    def create(self):
        organization_serializer = OrganizationSerializer(data=self.data)
        if organization_serializer.is_valid(raise_exception=True):
            organization = organization_serializer.save()
        return organization

    '''to  get all organization data'''
    def get_all():
        organization = Organization.find_by(multi=True,
                                            status=StatusBase.ACTIVE)
        organization_serializer = OrganizationSerializer(organization,
                                                         many=True)
        return organization_serializer.data

    '''check organization is exist'''

    def check_organization_exist(self, organization_id):
        organization = Organization.find_by(multi=True, id=organization_id)
        if not organization:
            raise OrganizationException(
                OrganizationError.ORGANIZATION_NOT_FOUND)

    '''get company data based on organization id'''

    def get(self,
            organization_id,
            fields=None):
        self.check_organization_exist(organization_id=organization_id)
        company_service = CompanyService(data=self.data)
        companies = company_service.get(
            organization=organization_id, fields=fields)

        return companies


