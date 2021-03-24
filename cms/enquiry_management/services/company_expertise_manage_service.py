from commodity.models.commodity import Commodity
from company.models.company import Company
from country.models.country import Country
from enquiry_management.models.company_expertise import CompanyExpertise
from enquiry_management.serializers import CompanyExpertiseSerializer
from exceptions import EnquiryManagementException, EnquiryManagementError
from utils.base_models import StatusBase,QuoteChoice


class CompanyExpertiseManageService:

    def __init__(self, data):
        self.data = data

    def create(self, company_id):

        Company.find_by(status=StatusBase.ACTIVE, id=company_id)
        self.data['company'] = company_id
        company_expertise_serializer = CompanyExpertiseSerializer(
            data=self.data)

        # this function validate the transport mode required fields
        self.validate_transport_mode_required_fields()

        if company_expertise_serializer.is_valid(raise_exception=True):
            company_expertise_serializer.save()

        return True

    def update(self,company_id, id):

        Company.find_by(status=StatusBase.ACTIVE, id=company_id)
        self.data['company'] = company_id
        company_expertise = CompanyExpertise.find_by(company_id=company_id, id=id)

        company_expertise_serializer = CompanyExpertiseSerializer(company_expertise,
            data=self.data)

        # this function validate the transport mode required fields
        self.validate_transport_mode_required_fields()

        if  company_expertise_serializer.is_valid(raise_exception=True):
            company_expertise_serializer.save()

        return True


    def validate_transport_mode_required_fields(self):

        # For FCL container type is required otherwise for air,air Courier,lcl  it should be blank
        if self.data['transport_mode'] in ['FCLI', 'FCLE', 'FCLTC']:
            self.data['temperature_controlled'] = None
            if('container_type' not in self.data or not self.data['container_type']):
                raise EnquiryManagementException(
                    EnquiryManagementError.COMPANY_EXPERTISE_CONTAINER_TYPE_REQUIRED)
        else:
            self.data['container_type'] = []

        # For Third country from_trade_lanes and to_trade_lanes are required and instant_quotes default value false
        if self.data['transport_mode'] in ['ATC', 'ACTC', 'FCLTC', 'LCLTC']:
            self.data['trade_lanes'] = []
            if 'instant_quotes' not in self.data or not self.data['instant_quotes']:
                self.data['instant_quotes'] = False

            if (('from_trade_lanes' not in self.data or 'to_trade_lanes' not in self.data) or not self.data['from_trade_lanes'] or not self.data['to_trade_lanes']):
                raise EnquiryManagementException(
                    EnquiryManagementError.COMPANY_EXPERTISE_THIRD_COUNTRY)

        # For import and Export trade_lanes is required
        if self.data['transport_mode'] in ['AI', 'AE', 'ACI', 'ACE', 'LCLI', 'LCLE', 'FCLI', 'FCLE']:
            self.data['from_trade_lanes'] = []
            self.data['to_trade_lanes'] = []
            if ('trade_lanes' not in self.data or not self.data['trade_lanes']):
                raise EnquiryManagementException(
                    EnquiryManagementError.COMPANY_EXPERTISE_TRADE_LANES_REQUIRED)

        #  set default value true for air,air Courier,lcl import/export/third_country ,if some one set null from backend for hacking purpose
        if self.data['transport_mode'] in ['AI', 'AE', 'ATC', 'ACE', 'ACI', 'ACTC', 'LCLI', 'LCLE', 'LCLTC'] and ('temperature_controlled' not in self.data or not self.data['temperature_controlled']):
            self.data['temperature_controlled'] = True

    # create default enquiry management
    def create_default_enquiry_management(self, company_id, transport_modes,weight,weight_unit):

        commodity = list(Commodity.objects.values_list('id', flat=True).order_by('id'))

        country = list(Country.find_by(multi=True).values_list('id', flat=True).order_by('id'))

        container_type=list(dict(QuoteChoice.CONTAINER_TYPE_CHOICES))

        company_expertise_data = {}

        for transport_mode in transport_modes:

            if transport_mode in ['FCLI', 'FCLE', 'FCLTC']:
                company_expertise_data.update(
                    {'container_type': container_type})

            if transport_mode in ['ATC', 'FCLTC', 'LCLTC', 'ACTC']:
                company_expertise_data.update(
                    {'to_trade_lanes': country, 'from_trade_lanes': country})

            if transport_mode in ['AI', 'FCLI', 'LCLI', 'ACI', 'AE', 'FCLE', 'LCLE', 'ACE']:
                company_expertise_data.update({'trade_lanes': country})

            company_expertise_data.update({
                'transport_mode': transport_mode,
                'company': company_id,
                'commodity': commodity,
                'weight':weight,
                'weight_unit':weight_unit
            })
            company_expertise_service = CompanyExpertiseManageService(
                data=company_expertise_data)
            company_expertise_service.create(company_id=company_id)