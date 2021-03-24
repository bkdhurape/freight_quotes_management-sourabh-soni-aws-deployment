from address.services.address_service import AddressService
from branch.models.branch import Branch
from branch.services.branch_service import BranchService
from company.models.company import Company
from company.services.company_manage_service import CompanyManageService
from country.models.country import Country
from currency.models.currency_profile import CurrencyProfile
from currency.services.currency_profile_service import CurrencyProfileService
from currency.validations import CurrencyValidation
from customer.models.invited_vendor import InvitedVendor
from customer.serializers import InvitedVendorSerializer
from customer.services.invited_vendor_service import InvitedVendorService
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from enquiry_management.models.company_expertise import CompanyExpertise
from enquiry_management.services.company_expertise_manage_service import CompanyExpertiseManageService
from exceptions import VendorException, VendorError,VendorTypeException,VendorTypeError,CompanyException, CompanyError
from notification.managers.email_manager import EmailNotification
from utils.base_models import StatusBase
from utils.helpers import generate_token, encode_data, encode_password, decode_data, date_difference_in_hours, generate_token_data
from utils.responses import success_response
from vendor.models.vendor import Vendor
from rest_framework import status
from vendor.models.vendor_companies_mode import VendorCompaniesMode
from vendor.models.vendor_type import VendorType
from vendor.serializers import VendorSerializer, VendorCompaniesModeSerializer
from vendor.services.vendor_service import VendorService
from vendor.services.vendor_type_service import VendorTypeService
from vendor.validation import VendorValidation


class VendorManageService:

    def __init__(self, data):
        self.data = data

    def create_vendor_company(request_data):

        company_exist = Company.find_by(
            multi=True, name=request_data['name'], type='vendor')
        if company_exist:
            raise VendorException(VendorError.CONTACT_ADMIN)

        request_data['type'] = 'vendor'
        company_manage_service = CompanyManageService(data=request_data)
        company_id = company_manage_service.create()
        company = company_id

        return [company]

    def get_or_create_company(request_data):
        if not 'company' in request_data['vendor_details'] and 'company_name' in request_data['vendor_details']:

            company_creation_data = {
                'name': request_data['vendor_details']['company_name'],
                'address_details': request_data['address_details']
            }
            company = VendorManageService.create_vendor_company(
                company_creation_data)

        else:
            company = request_data['vendor_details']['company']

        return company

    # Create vendor & currency profile data
    def create(self, request, company_id, token = None):

        if 'vendor_details' in request:
            req_vendor_data = request['vendor_details']

            invited_vendor_id = 0
            if token is not None:
                decode_invite_data = decode_data(token)
                invited_vendor_id, company_name, email = decode_invite_data.split("__")

            if req_vendor_data['home_company'] is not None:
                if req_vendor_data['home_company'] != company_id:
                    raise CompanyException(CompanyError.COMPANY_NOT_FOUND)

                if not req_vendor_data['supervisor']:
                    raise VendorException(
                        VendorError.VENDOR_SUPERVISOR_REQUIRED)

                # Validate companies currency
                organization_id = list(Company.find_by(multi=True, id=req_vendor_data['home_company'], status=StatusBase.ACTIVE).values_list('organization', flat=True))[0]
                CurrencyValidation.validate_companies_currency(request, organization_id)

                # Validate companies mode
                VendorValidation.validate_companies_mode(request)

            # creating company for a vendor based on data
            request['vendor_details']['company'] = VendorManageService.get_or_create_company(
                request)

            if not request['vendor_details']['home_company'] and request['vendor_details']['company_name']:
                request['vendor_details']['home_company'] = request['vendor_details']['company'][0]
                req_vendor_data['is_super_admin'] = True

            if 'password'  not in req_vendor_data:
                # Generate token from email and type and uuid for add vendor
                token_hash, token = generate_token_data(req_vendor_data['email'],'vendor')
                req_vendor_data['registration_token'] = token
                req_vendor_data['token_date'] = datetime.now()

            req_vendor_data['password'] = encode_password(
                req_vendor_data['password']) if 'password' in req_vendor_data and req_vendor_data['password'] else None

            # Check if branch key exist in vendor data request object
            if 'branch' in req_vendor_data:
                # Check company branch exist or not
                VendorService.company_branch_exist(
                    req_vendor_data['home_company'], req_vendor_data['branch'])

            if ('vendor_type' not in req_vendor_data or not req_vendor_data['vendor_type']):
                raise  VendorTypeException(VendorTypeError.VENDOR_TYPE_IS_REQUIRED)
               
            # calling the vender type  function which create default enquiry mangement based on vendor type
            VendorManageService.create_default_enquiry_management_based_on_vendor_type(self,req_vendor_data['vendor_type'],req_vendor_data['home_company'])


            # Get Country Id By Home Company
            country_id = self.get_country_id(
                request, req_vendor_data['home_company'])

            # Get Country Code By Country Id
            country_code = Country.objects.only('code').get(id=country_id).code

            # Get Vendor Type By Checking Vendor Type and Selected Country
            # req_vendor_data['vendor_type'] = self.get_vendor_type_id(
            #     req_vendor_data['vendor_type'], country_code)

            vendor_serializer = VendorSerializer(data=req_vendor_data)
            if vendor_serializer.is_valid(raise_exception=True):
                vendor_id = (vendor_serializer.save()).id

                if token is not None and invited_vendor_id != 0:
                    self.update_customer_vendor_client(invited_vendor_id = invited_vendor_id, vendor_company_id = request['vendor_details']['home_company'], vendor_id = vendor_id)


                if 'currency_profile_detail' in request:
                    currency_data = request['currency_profile_detail']
                else:
                    currency_data = {}

                if 'user_companies_currency' in request:
                    for company in request['user_companies_currency']:

                        # Set currency profile for vendor
                        CurrencyProfileService.set_currency(
                            request_data=dict((list(company.values())[0]).items()),
                            entity_id=vendor_id, entity_type='vendor',company_id=list(company.keys())[0], country_id=country_id)

                else:
                    currency_data = {}


                    # Set currency profile for vendor
                    CurrencyProfileService.set_currency(
                        request_data=currency_data, entity_id=vendor_id, entity_type='vendor',company_id=request['vendor_details']['home_company'], country_id=country_id)

                # Set companies mode for vendor when add a vendor
                if 'companies_mode' in request:
                    for company_data in request['companies_mode']:
                        request_company_mode = {
                            'vendor': vendor_id,
                            'company': list(company_data.keys())[0],
                            'mode': list(set(list(company_data.values())[0]))
                        }
                        vendor_companies_mode_serializer = VendorCompaniesModeSerializer(data=request_company_mode)
                        if vendor_companies_mode_serializer.is_valid(raise_exception=True):
                            vendor_companies_mode_serializer.save()

            if  'password' in req_vendor_data and req_vendor_data['password'] is not None:
                response= { 'data':None,'status':'success'}

            else:
                link = settings.API_HOST + '/api/v1/profile/'  + token_hash
                response = { 'data': link ,'status':'success'}

            return response


    def update_customer_vendor_client(self, invited_vendor_id, vendor_company_id = None, vendor_id = None):
        invited_vendor = InvitedVendor.find_by(multi = True, id = invited_vendor_id)

        if invited_vendor:
            invited_vendor_serializer = InvitedVendorSerializer(invited_vendor, many = True)

            invited_vendor_data = invited_vendor_serializer.data[0]
            invited_vendor_data.update({ 'vendor': vendor_id, 'vendor_company': vendor_company_id })

            invited_vendor_service = InvitedVendorService(data=invited_vendor_data)
            invited_vendor_service.update(invited_vendor_data['id'])


    # Get vendor type id bry slug
    def get_vendor_type_id(self, vendor_type, country_code):
        vendor_type_service = VendorTypeService({})
        if vendor_type == 'freight-forwarder' and country_code != 'IN':
            vendor_type_id = vendor_type_service.get_vendor_type_id_by_slug(
                slug='foreign-agent')
        else:
            vendor_type_id = vendor_type_service.get_vendor_type_id_by_slug(
                slug=vendor_type)


        return vendor_type_id

    def get_country_id(self, request, company):
        if 'address_details' in request and request['address_details'] and 'country' in request['address_details'] and request['address_details']['country']:
            country_id = request['address_details']['country']
        else:
            address_details = AddressService.get(
                "company", company)
            country_id = address_details['country']['id']

        return country_id

    # Resend activation link to vendor by registered email

    def resend_activation_link(self, email):
        try:
            decoded_email = decode_data(email)
        except Exception as e:
            raise VendorException(VendorError.INVALID_TOKEN_CONTACT_ADMIN)

        vendor = Vendor.find_by(multi=True, email=decoded_email)
        if not vendor:
            raise VendorException(VendorError.VENDOR_NOT_FOUND)

        vendor_serializer = VendorSerializer(vendor, many=True)
        vendor_data = vendor_serializer.data[0]

        if vendor_data['status'] == Vendor.ACTIVE:
            response = {'message':'you are already activated,please login to continue.','status':'success','status_code':status.HTTP_201_CREATED}

        elif vendor_data['status'] == Vendor.PENDING:
            token_hash, token = generate_token_data(decoded_email)
            vendor_data['registration_token'] = token
            vendor_data['token_date'] = datetime.now()

            vendor_service = VendorService(data=vendor_data)
            vendor_service.update(vendor_id=vendor_data['id'])

            link = settings.FRONTEND_URL + '/api/v1/company/' + \
                str(vendor_data['home_company']) + '/vendor/activate/' + token_hash

            # Send activation link in email
            vendor_name = list(vendor.values_list('name', flat=True))[0]
            email_data = {'user_name':vendor_name, 'email':decoded_email, 'link':link }
            EmailNotification.vendor_activation(email_data)
            response = {'status': 'success','message':'Activation link sent successfully','status_code':status.HTTP_200_OK}

        return response

    # Activate vendor by token in activation link.
    def activate_vendor(self, url_token_hash):

        email, token = self.get_vendor_data_from_url(url_token_hash)
        vendor = Vendor.objects.filter(email=email).first()
        if not vendor:
            raise VendorException(VendorError.INVALID_TOKEN_CONTACT_ADMIN)

        vendor_serializer = VendorSerializer(vendor)
        vendor_data = vendor_serializer.data

        if vendor_data['status'] == Vendor.INACTIVE:
            raise VendorException(VendorError.VENDOR_INACTIVE)

        if vendor_data['status'] == Vendor.PENDING:
            if (vendor_data['registration_token'] != token) or (not token):
                raise VendorException(VendorError.INVALID_TOKEN_RESEND_LINK)

            if (vendor_data['registration_token'] == token):
                return self.validate_token_and_activate_vendor(vendor_data,vendor.token_date)

        elif vendor_data['status'] == Vendor.ACTIVE:
            response = {'message':'you are already activated,please login to continue.','status':'success','status_code':status.HTTP_201_CREATED}

        return response

    # Get vendor email and token from url token

    def get_vendor_data_from_url(self, url_token_hash):
        try:
            decoded_token = decode_data(url_token_hash)
        except Exception as e:
            raise VendorException(VendorError.INVALID_TOKEN_CONTACT_ADMIN)

        return decoded_token.split("__")

    '''Validate if vendor activation link expired by token date and activate vendor if token not expired.
    Show appropriate error if token expired.'''

    def validate_token_and_activate_vendor(self, vendor_data,token_date):
        today = timezone.now()
        hours = date_difference_in_hours(token_date, today)

        if hours > int(settings.TOKEN_EXPIRY_LIMIT):
            encoded_email = encode_data(vendor_data['email'])
            response = self.resend_activation_link(encoded_email)
            response = {'data':{settings.REST_FRAMEWORK['NON_FIELD_ERROR_KEY']:['Your activation link has been expired. A new activation link has been sent to '
                                       'your registered email id.']}, 'status':'error'}


        else:
            vendor_data['registration_token'] = None
            vendor_data['token_date'] = None
            vendor_data['status'] = Vendor.ACTIVE

            # Get country, state and city by by company_id
            address_details = AddressService.get(
                "company", vendor_data['home_company'])

            # set city and country id  in default branch creation  if its in address data at the time of vendor registration otherwise set blank
            city=[] if address_details['city'] is None else [address_details['city']['id']]
            state=[] if address_details['state'] is None else [address_details['state']['id']]

            # Creating branch
            branch_data = {'name': 'HQ', 'company': vendor_data['home_company'], 'country': address_details['country']['id'], 'state':state, 'city':city, 'is_head_branch': True}

            branch_service = BranchService(data=branch_data)
            branch_id = branch_service.create()

            vendor_data['branch'] = [branch_id]

            vendor_service = VendorService(data=vendor_data)
            vendor_service.update(vendor_id=vendor_data['id'])
            response = {'status': 'success','message':'Vendor activated successfully','status_code':status.HTTP_200_OK}

        return response

    # check company expertise exist or not in database against vendor company if not then create
    def create_default_enquiry_management_based_on_vendor_type(self,vendor_type,company_id):
        company_expertise = CompanyExpertise.find_by(
            multi=True, status=StatusBase.ACTIVE, company=company_id)

        if not company_expertise:
            # check vendor type  and according to vendor type and transport mode it create default enquiry_management in DB
            if (vendor_type == 'freight-forwarder' or vendor_type == 'foreign-agent'):
                transport_modes = ['AI', 'AE', 'LCLI', 'LCLE', 'FCLI',
                                    'FCLE', 'ACI', 'ACE', 'ATC', 'ACTC', 'LCLTC', 'FCLTC']
                weight=None
                weight_unit=None

            elif (vendor_type == 'courier'):
                transport_modes = ['ACI', 'ACE', 'ACTC']
                weight=0.0
                weight_unit=None

            elif(vendor_type == 'customs' or vendor_type=='transport-only'):
                transport_modes = ['AI', 'AE',
                                    'LCLI', 'LCLE', 'FCLE', 'FCLI']
                weight=None
                weight_unit=None
            else:
                return False

            # calling default enquiry management function for create default enquiry management based on vendor type
            CompanyExpertiseManageService.create_default_enquiry_management(self, company_id, transport_modes, weight, weight_unit)
            

    # Update vendor & currency profile data by vendor ID
    def update(request, company_id, id):

        Company.find_by(id=company_id)
        Vendor.find_by(id=id, home_company=company_id, status=Vendor.ACTIVE)

        if 'vendor_details' in request:
            req_vendor_data = request['vendor_details']
            vendor_service = VendorService(data=req_vendor_data)
            vendor_service.update(vendor_id=id)

        organization_id = list(Company.find_by(multi=True, id=request['vendor_details']['home_company'], status=StatusBase.ACTIVE).values_list('organization', flat=True))[0]
        CurrencyValidation.validate_companies_currency(request, organization_id)
        for company in request['user_companies_currency']:
            request_currency_profile_data = dict((list(company.values())[0]).items())
            CurrencyProfile.objects.filter(entity_type='vendor', entity_id=id,
                company_id=int(list(company.keys())[0])).update(**request_currency_profile_data)

        VendorValidation.validate_companies_mode(request)
        for company in request['companies_mode']:
            request_mode_data = {'mode': list(set(list(company.values())[0]))}
            VendorCompaniesMode.objects.filter(vendor=id, company=list(company.keys())[0]).update(**request_mode_data)


        return True

    def update_vendor_supervisors_mapping(company_id, vendor_id):

        Company.find_by(id=company_id)
        Vendor.find_by(id=vendor_id, home_company=company_id,
                       status=Vendor.ACTIVE)

        # Update vendor status to inactive
        VendorService.delete(vendor_id=vendor_id)

        # Find parent supervisor
        parent_supervisor_list = list(Vendor.find_by(
            multi=True, vendors=vendor_id, status=Vendor.ACTIVE).values_list('id', flat=True))

        # Find child supervisor
        child_supervisors_list = list(Vendor.find_by(
            multi=True, supervisor=vendor_id, status=Vendor.ACTIVE).values_list('id', flat=True))

        # Clear by vendor
        vendor = Vendor.find_by(id=vendor_id)
        vendor.supervisor.clear()

        # Clear by supervisor
        for clear_supervisor_id in child_supervisors_list:
            vendor = Vendor.find_by(id=clear_supervisor_id)
            vendor.supervisor.clear()

        # Find child supervisors company
        for child_superviosr in child_supervisors_list:
            child_superviosr_companies = list(Vendor.find_by(
                multi=True, id=child_superviosr, status=Vendor.ACTIVE).values_list('company', flat=True))
            assign_supervisor_list = list(dict.fromkeys(Vendor.find_by(
                multi=True, company__in=child_superviosr_companies, id__in=parent_supervisor_list, status=Vendor.ACTIVE).values_list('id', flat=True)))

            # Assign suppervisor to a child supervisor
            for assign_supervisor in assign_supervisor_list:
                vendor = Vendor.find_by(id=child_superviosr)
                supervisor = Vendor.find_by(id=assign_supervisor)
                vendor.supervisor.add(supervisor)
