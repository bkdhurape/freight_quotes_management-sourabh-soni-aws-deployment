from address.models.address import Address
from address.services.address_service import AddressService
from company.models import Company, Organization
from company.serializers import CompanySerializer
from company.services.organization_service import OrganizationService
from company.services.company_logistic_info_service import CompanyLogisticInfoService
from company.validations import CompanyValidation
from country.models.country import Country
from department.services.department_service import DepartmentService
from exceptions import CompanyException, CompanyError, AddressException, AddressError, OrganizationError, OrganizationException
from rest_framework.exceptions import ValidationError


class CompanyManageService:
    def __init__(self, data):
        self.data = data

    # check company exist or not

    def is_company_name_exists(self):
        company = Company.find_by(multi=True, name=self.data['name'])
        if company.count():
            return True

        return False

    # create organization or assign existing organization to company

    def get_organization(self):
        if 'organization' not in (
                self.data) or self.data['organization'] == '':
            organization_service = OrganizationService(data=self.data)
            organization = organization_service.create()
        else:
            organization = Organization.find_by(pk=self.data['organization'])

        return organization

    def validate_company(self):
        company_exists = self.is_company_name_exists()
        if company_exists:
            raise CompanyException(CompanyError.COMPANY_EXISTS)

    # create address or update in company

    def create_or_update_address(self, address_data, company_id, action = None):

        address_data.update({
            'entity_id': company_id,
            'entity_type': 'company',
            'address1': address_data['street']

        })
        address_service = AddressService(data=address_data)
        if action == 'update':
            address_service.check_country(entity_id=company_id, entity_type = 'company', id=address_data['id'])

        return address_service

    # check address_details

    def check_address_details(self):
        if 'address_details' not in self.data:
            raise AddressException(AddressError.ADDRESS_IS_REQUIRED)
        if 'street' not in (self.data['address_details']) or self.data['address_details']['street'] == ''or self.data['address_details']['street'] is None:
            raise AddressException(AddressError.STREET_IS_REQUIRED)

    # validate gst,cin,pan,iec if country is india and in customer registration customer type is importer_or_exporter the only validate iec

    def check_is_country_india(self, type):
        country_id = Country.objects.only('id').get(code='IN').id
        if ('country' in self.data['address_details'] and self.data['address_details']['country'] == country_id):
            if 'gst' not in self.data or self.data['gst'] == "" or self.data['gst'] is None:
                raise CompanyException(CompanyError.GST_IS_REQURIED)
            if 'cin' not in self.data or self.data['cin'] == "" or self.data['cin'] is None:
                raise CompanyException(CompanyError.CIN_IS_REQURIED)
            if 'pan' not in self.data or self.data['pan'] == "" or self.data['pan'] is None:
                raise CompanyException(CompanyError.PAN_IS_REQURIED)
            if ('customer_type' in self.data and self.data['customer_type'] == 'importer_or_exporter' and type == 'customer'):
                if 'iec' not in self.data or self.data['iec'] == "" or self.data['iec'] is None:
                    raise CompanyException(CompanyError.IEC_IS_REQURIED)
            else:
                self.data['iec'] = None
        else:
            self.data['gst'], self.data['cin'], self.data['pan'], self.data['iec'] = None, None, None, None

    # create company and organization

    def create(self):
        organization = self.get_organization()
        self.data['organization'] = organization.id

        if 'type' in self.data and self.data['type'] == 'vendor':
            user_type = self.data['type']
            company_id = self.create_vendor_company(
                user_type=user_type, organization=organization)
        else:
            company_id = self.create_customer_company(organization)

        return company_id

    '''check organization is exists'''

    def create_customer_company(self, organization):
        if (('industry' in self.data) and ('business_activity' in self.data)):

            # check address_details
            self.check_address_details()
            # check country is india or not and validate gst,pan,cin,gst if country is india
            self.check_is_country_india(type='customer')
            CompanyValidation.validate_industry(
                self.data['industry'], self.data['industry_other'])
            CompanyValidation.validate_business_activity(
                self.data['business_activity'], self.data['business_activity_other'])

            company_serializer = CompanySerializer(data=self.data)
            if company_serializer.is_valid(raise_exception=True):
                company_id = (company_serializer.save()).id
            # saving a address

            address_data = self.create_or_update_address(
                self.data['address_details'], company_id)
            address_data.create()

        else:
            company = Company(
                name=self.data['name'], organization=organization)
            company.save()
            company_id = company.id
            address_details = {
                'country': self.data['home_country'], 'street': None}
            address_data = self.create_or_update_address(
                address_details, company_id)
            address_data.create()

        if 'home_country' in self.data:
            country_id = self.data['home_country']
        else:
            country_id = self.data['address_details']['country']

        # Saving company logistic info
        CompanyLogisticInfoService.create(
            data=self.data, company_id=company_id, country_id=country_id)

        # creating departments
        department_service = DepartmentService(data={})
        department_service.create(company_id=company_id)

        return company_id

    def create_vendor_company(self, user_type, organization):
        self.check_address_details()
        if 'incorporation_year' in self.data:
            self.check_is_country_india(type='vendor')

        company_serializer = CompanySerializer(data=self.data)
        if company_serializer.is_valid(raise_exception=True):
            company_id = (company_serializer.save()).id

        # saving a address
        address_data = self.create_or_update_address(
            self.data['address_details'], company_id)
        address_data.create()
        country_id = self.data['address_details']['country']

        '''Saving company logistic info'''
        CompanyLogisticInfoService.create(
            data=self.data, company_id=company_id, country_id=country_id)

        return company_id

    # check organization is exists
    def check_organization(self, company_id):
        company = Company.find_by(id=company_id)
        company_serializer = CompanySerializer(company)
        if company_serializer.data['organization'] != self.data['organization']:
            raise OrganizationException(
                OrganizationError.ORGANIZATION_NOT_FOUND)

    # update company details

    def update(self, company_id):
        if 'organization' not in (self.data) or self.data['organization'] == '':
            raise OrganizationException(
                OrganizationError.ORGANIZATION_REQUIRED)
        self.check_organization(company_id=company_id)
        organization = self.get_organization()
        self.data['organization'] = organization.id
        company = Company.find_by(id=company_id)
        company_serializer = CompanySerializer(company, data=self.data)

        # check address_details
        self.check_address_details()
        self.data['id'] = company_id
        if ('industry' in self.data):
            CompanyValidation.validate_industry(
                self.data['industry'], self.data['industry_other'])
        if ('business_activity' in self.data):
            CompanyValidation.validate_business_activity(
                self.data['business_activity'], self.data['business_activity_other'])

        # To call function update_company_address for edit address
        address_update_data = self.create_or_update_address(
            company_id=company_id, address_data=self.data['address_details'], action = 'update')
        address_id = self.data['address_details']['id']

        address_update_data.update(
            entity_type='company', entity_id=company_id, id=address_id)
        type = 'customer' if self.data['type'] == 'customer' else 'vendor'
        # check country is india or not and validate gst,pan,cin,gst if country is india
        self.check_is_country_india(type=type)
        if company_serializer.is_valid(raise_exception=True):
            company_serializer.save()
