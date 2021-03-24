from currency.models.currency_profile import CurrencyProfile
from currency.services.currency_profile_service import CurrencyProfileService
from currency.validations import CurrencyValidation
from customer.services.customer_service import CustomerService
from customer.serializers import CustomerSerializer
from customer.models.customer import Customer
from company.models.company import Company
from company.services.company_manage_service import CompanyManageService
from country.models.country import Country
from datetime import datetime, timedelta
from django.utils import timezone
from department.models.department import Department
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from exceptions import CustomerException, CustomerError
from exceptions.currency_exceptions import CurrencyException, CurrencyError
from notification.managers.email_manager import EmailNotification
from utils.base_models import StatusBase
from utils.constants import FreightConstant
from utils.responses import success_response
from rest_framework import status
from utils.helpers import Diff, generate_token, encode_data, encode_password, decode_data, date_difference_in_hours, generate_token_data
import jwt


class CustomerManageService:

    def __init__(self, data):
        self.data = data

    def create_customer_company(request_data):
        company_exist = Company.find_by(multi=True, name=request_data['name'])
        if company_exist:
            raise CustomerException(CustomerError.CONTACT_ADMIN)

        company_manage_service = CompanyManageService(
            data=request_data)
        company_id = company_manage_service.create()
        company = company_id
        # set department of super admin user
        department = CustomerManageService.get_department_id(company_id)

        return [company], [department]

    def get_or_create_company(request_data):
        if 'company_details' in request_data and request_data['company_details']:
            request_data['company_details']['name'] = request_data['customer_details']['company_name']
            request_data['company_details']['customer_type'] = request_data['customer_details']['customer_type']
            request_data['currency_profile_detail'] = {} if 'currency_profile_detail' not in request_data else request_data['currency_profile_detail']
            company_creation_data = {
                **request_data['company_details'], **request_data['additional_details'], **request_data['currency_profile_detail']}
            company, department = CustomerManageService.create_customer_company(company_creation_data)

        elif not 'company' in request_data['customer_details'] and 'company_name' in request_data['customer_details']:
            company_creation_data = {
                'name': request_data['customer_details']['company_name'],
                'home_country': request_data['customer_details']['home_country']
            }
            company, department = CustomerManageService.create_customer_company(company_creation_data)
        elif not 'company':
            return success_response(message="Company is required", data=request_data)

        else:
            company, department = request_data['customer_details']['company'], request_data['customer_details'][
                'department']

        return company, department

    # Create customer & currency profile data
    def create(request, company_id):
        request_data = request.data
        if 'customer_details' in request_data:
            req_customer_data = request_data['customer_details']

            if (('password' in req_customer_data) and ('customer_type' not in req_customer_data or not req_customer_data['customer_type'])):
                raise CustomerException(CustomerError.CUSTOMER_TYPE_REQUIRED)

            if 'customer_type' in req_customer_data and req_customer_data['customer_type'] == 'other':
                if 'customer_type_other' not in req_customer_data or not req_customer_data['customer_type_other']:
                    raise CustomerException(CustomerError.CUSTOMER_TYPE_OTHER_REQUIRED)
            else:
                req_customer_data['customer_type_other'] = None

            # creating company for a customer based on data
            request_data['customer_details']['company'], request_data['customer_details'][
                'department'] = CustomerManageService.get_or_create_company(request_data)

            if not request_data['customer_details']['home_company'] and request_data['customer_details']['company_name']:
                request_data['customer_details']['home_company'] = request_data['customer_details']['company'][0]
                req_customer_data['is_super_admin'] = True
            else:
                jwt_token_decode = jwt.decode(request.headers['Authorization'], settings.JWT_FCT_SECRET, algorithms=['HS256'], options={'verify_exp': False})
                # Validate customer request parameters
                CustomerManageService.validate_customer_request_params(req_customer_data, jwt_token_decode['organization_id'])
                # Validate companies currency
                CurrencyValidation.validate_companies_currency(request_data, jwt_token_decode['organization_id'])


            type='customer' if 'password'  not in request_data['customer_details'] else None
            # Generate token from email
            token_hash, token = generate_token_data(req_customer_data['email'],type)
            req_customer_data['registration_token'] = token
            req_customer_data['token_date'] = datetime.now()

            req_customer_data['password'] = encode_password(req_customer_data['password']) if 'password' in req_customer_data and req_customer_data['password'] else None
            customer_serializer = CustomerSerializer(data=req_customer_data)

            # Check company department exist or not
            CustomerService.company_department_exist(req_customer_data['home_company'], req_customer_data['department'])

            if customer_serializer.is_valid(raise_exception=True):
                customer_id = (customer_serializer.save()).id
                country_id = request_data['customer_details']['home_country']
                if 'user_companies_currency' in request_data:
                    for company in request_data['user_companies_currency']:
                        # set currency profile for customer
                        CurrencyProfileService.set_currency(request_data=dict((list(company.values())[0]).items(
                        )), entity_id=customer_id, entity_type='customer', company_id=list(company.keys())[0], country_id=country_id)
                else:
                    currency_data = request_data['currency_profile_detail'] if 'currency_profile_detail' in request_data else {}
                    # set currency profile for customer
                    CurrencyProfileService.set_currency(request_data=currency_data, entity_id=customer_id, entity_type='customer',
                                                        company_id=request_data['customer_details']['home_company'], country_id=country_id)


            if 'password' in request.data['customer_details'] and request.data['customer_details']['password'] is not None:
                # token_hash -> It is a combination of customer email and uuid.
                link = settings.API_HOST + '/api/v1/company/' + str(request_data['customer_details']['home_company']) + '/customer/activate/' + token_hash
            else:
                # token_hash -> It is a combination of customer email and uuid and type for add customer to set their profile
                link = settings.FRONTEND_URL + '/set-profile/'  + token_hash

            return {'status': 'success', 'activation_link': link}

    # Resend activation link to customer by registered email
    def resend_activation_link(self, email):
        try:
            decoded_email = decode_data(email)
        except Exception as e:
            raise CustomerException(CustomerError.INVALID_TOKEN_CONTACT_ADMIN)

        customer = Customer.find_by(multi=True, email=decoded_email)
        if not customer:
            raise CustomerException(CustomerError.CUSTOMER_NOT_FOUND)

        customer_serializer = CustomerSerializer(customer, many=True)
        customer_data = customer_serializer.data[0]

        if customer_data['status'] == Customer.ACTIVE:
            raise CustomerException(CustomerError.ALREADY_ACTIVATED)

        token_hash, token = generate_token_data(decoded_email)
        customer_data['registration_token'] = token
        customer_data['token_date'] = datetime.now()

        customer_service = CustomerService(data=customer_data)
        customer_service.update(customer_id=customer_data['id'])

        # link = settings.API_HOST + '/api/v1/company/' + str(customer_data['home_company']) + '/customer/activate/' + token_hash
        link = settings.FRONTEND_URL + '/activation/customer/' + str(customer_data['home_company']) + '/' + token_hash
        response = {'status': 'success', 'activation_link': link, 'data': customer_data}

        return response

    # Activate customer by token in activation link.
    def activate_customer(self, url_token_hash):

        email, token = self.get_customer_data_from_url(url_token_hash)
        
        customer = Customer.objects.filter(email=email, status__ne=Customer.INACTIVE).first()
        if not customer:
            raise CustomerException(CustomerError.INVALID_TOKEN_CONTACT_ADMIN)

        customer_serializer = CustomerSerializer(customer)
        customer_data = customer_serializer.data

        if customer_data['status'] == Customer.PENDING:
            if (customer_data['registration_token'] != token) or (not token):
                raise CustomerException(CustomerError.INVALID_TOKEN_RESEND_LINK)

            if (customer_data['registration_token'] == token):
                return self.validate_token_and_activate_customer(customer_data,customer.token_date)

        elif customer_data['status'] == Customer.ACTIVE:
            response = {'message':'you are already activated,please login to continue.','status':'success','status_code':status.HTTP_201_CREATED}

        return response

    # Get customer email and token from url token
    def get_customer_data_from_url(self, url_token_hash):
        try:
            decoded_token = decode_data(url_token_hash)
        except Exception as e:
            raise CustomerException(CustomerError.INVALID_TOKEN_CONTACT_ADMIN)

        split_token = decoded_token.split("__")
        email = split_token[0]
        token = split_token[1]

        return email, token

    # Get customer email and token from url token
    def get_customer_data_from_url_use_in_serializer(self, url_token_hash):
        try:
            decoded_token = decode_data(url_token_hash)
            split_token = decoded_token.split("__")
            email = split_token[0]
            account_type = split_token[1]
            return {'success': True, 'data': {'email': email, 'account_type': account_type}}
        except Exception as e:
            return {'success': False, 'data': 'Invalid Token. Please contact admin for your account activation and other queries.'}


    '''Validate if customer activation link expired by token date and activate customer if token not expired.
    Show appropriate error if token expired.'''
    def validate_token_and_activate_customer(self, customer_data, token_date):
        today = timezone.now()
        hours = date_difference_in_hours(token_date, today)

        if hours > int(settings.TOKEN_EXPIRY_LIMIT):
            encoded_email = encode_data(customer_data['email'])
            response = self.resend_activation_link(encoded_email)
            if response['status'] == 'success':
                EmailNotification.verification_email(response['data'], response['activation_link'])
                response = {'data': {settings.REST_FRAMEWORK['NON_FIELD_ERROR_KEY']:['Your activation link has been expired. A new activation link has been sent to '
                                       'your registered email id.']}, 'status': 'error'}

        else:
            customer_data['registration_token'] = None
            customer_data['token_date'] = None
            customer_data['status'] = Customer.ACTIVE

            customer_service_object = CustomerService(data=customer_data)
            customer_service_object.update(customer_id=customer_data['id'])
            response = {'status': 'success','message':'Customer activated successfully','status_code':status.HTTP_200_OK}

        return response

    def get_department_id(company_id):
        department_id = Department.find_by(multi=False, company_id=company_id, name='Management').id
        return department_id

    # Update customer & currency profile data by customer ID
    def update(request, company_id, id):
        request_data = request.data
        Company.find_by(id=company_id)
        company_data = Customer.find_by(id=id, home_company=company_id, status=StatusBase.ACTIVE)
        jwt_token_decode = jwt.decode(request.headers['Authorization'], settings.JWT_FCT_SECRET, algorithms=['HS256'], options={'verify_exp': False})

        customer_serializer = CustomerSerializer(company_data)
        customer_data_list = customer_serializer.data
        customer_final_db_list = customer_data_list['company']
        customer_request_data = request_data['customer_details']['company']


        to_remove_company = Diff(customer_final_db_list, customer_request_data)

        for company in to_remove_company:
            currency_data={'entity_id':id, 'entity_type':'customer', 'company':company, 'multi':True}
            currency_profile_id = list(CurrencyProfile.find_by(**currency_data).values_list('id', flat=True))[0]
            CurrencyProfileService.delete(id=currency_profile_id)


        country_id = request_data['customer_details']['home_country']

        if 'user_companies_currency' in request_data:
            company_list = request_data['customer_details']['company']

            for company in request_data['user_companies_currency']:
                user_currency_company = list(company.keys())[0]

                if int(user_currency_company) in company_list:
                    # set currency profile for customer
                    CurrencyProfileService.set_currency(request_data=dict((list(company.values())[0]).items(
                    )), entity_id=id, entity_type='customer', company_id=user_currency_company, country_id=country_id)


        else:
            currency_data = request_data['currency_profile_detail'] if 'currency_profile_detail' in request_data else {}
            # set currency profile for customer
            CurrencyProfileService.set_currency(request_data=currency_data, entity_id=id, entity_type='customer',
                                                company_id=request_data['customer_details']['home_company'], country_id=country_id)


        # Validate customer request parameters
        CustomerManageService.validate_customer_request_params(request_data['customer_details'], jwt_token_decode['organization_id'])
        # Validate companies currency
        CurrencyValidation.validate_companies_currency(request_data, jwt_token_decode['organization_id'])


        if 'customer_details' in request_data:
            req_customer_data = request_data['customer_details']
            customer_service_object = CustomerService(data=req_customer_data)
            customer_service_object.update(customer_id=id)

        if 'user_companies_currency' in request_data:
            for company in request_data['user_companies_currency']:
                req_currency_profile_data = dict((list(company.values())[0]).items())
                CurrencyProfile.objects.filter(entity_type='customer', entity_id=id,
                                               company_id=int(list(company.keys())[0])).update(**req_currency_profile_data)

        return True

    def update_customer_supervisors_mapping(company_id, customer_id):
        Company.find_by(id=company_id)
        # customer_detail = Customer.find_by(id=customer_id, home_company=company_id, status=StatusBase.ACTIVE)

        # Update customer status to inactive
        CustomerService.delete(customer_id=customer_id)

        # Remove Customer Company & Department Mapping
        # customer_detail.company.clear()
        # customer_detail.department.clear()

        # Find parent supervisor
        # parent_supervisor_list = list(Customer.find_by(multi=True, customers=customer_id,
        #                                                status=StatusBase.ACTIVE).values_list('id', flat=True))

        # Find child supervisor
        # child_supervisors_list = list(Customer.find_by(multi=True, supervisor=customer_id,
        #                                                status=StatusBase.ACTIVE).values_list('id', flat=True))

        # Clear by customer
        # customer = Customer.find_by(id=customer_id)
        # customer.supervisor.clear()

        # Clear by supervisor
        # for clear_supervisor_id in child_supervisors_list:
        #     customer = Customer.find_by(id=clear_supervisor_id)
        #     customer.supervisor.clear()

        # Find child supervisors company
        # for child_superviosr in child_supervisors_list:
        #     child_superviosr_companies = list(Customer.find_by(multi=True, id=child_superviosr,
        #                                                        status=StatusBase.ACTIVE).values_list('company', flat=True))
        #     assign_supervisor_list = list(dict.fromkeys(Customer.find_by(multi=True, company__in=child_superviosr_companies,
        #                                                                  id__in=parent_supervisor_list, status=StatusBase.ACTIVE).values_list('id', flat=True)))

        #     # Assign suppervisor to a child supervisor
        #     for assign_supervisor in assign_supervisor_list:
        #         customer_object = Customer.find_by(id=child_superviosr)
        #         supervisor = Customer.find_by(id=assign_supervisor)
        #         customer_object.supervisor.add(supervisor)

    # Retrive Customer List By Company & Department ID
    def customer_list_by_department_id(request, company_id, department_id):
        Company.find_by(id=company_id, status=StatusBase.ACTIVE)
        filter_params = {
            'department': department_id,
            'status': StatusBase.ACTIVE
        }
        if ('name' in request.GET) and (request.GET['name'].strip()):
            filter_params.update({'name__icontains': request.GET['name']})
        customer_list = Customer.find_by(multi=True, **filter_params).order_by('name')
        result = CustomerSerializer(customer_list, many=True, fields=['id', 'name', 'is_super_admin', 'contact_no', 'landline_no_dial_code', 'landline_no', 'email', 'department']).data
        return result


    # Validate customer request parameters
    def validate_customer_request_params(request_params, organization_id):
        company_list = list(Company.find_by(multi=True, organization=organization_id, status=StatusBase.ACTIVE).values_list('id', flat=True))

        # Validate request params supervisor
        if not request_params['supervisor']:
            raise CustomerException(CustomerError.CUSTOMER_SUPERVISOR_REQUIRED)
        for supervisor in request_params['supervisor']:
            if not Customer.find_by(multi=True, id=supervisor, home_company__in=company_list, status=StatusBase.ACTIVE):
                raise CustomerException(CustomerError.CUSTOMER_SUPERVISOR_IS_INVALID)

        # Validate request params company
        for company in request_params['company']:
            if company not in company_list:
                raise CustomerException(CustomerError.CUSTOMER_COMPANY_NOT_EXISTS)

        # Validate request params home company
        if request_params['home_company'] not in company_list:
            raise CustomerException(CustomerError.CUSTOMER_COMPANY_NOT_EXISTS)

        # Validate department belongs to home company department's
        CustomerService.company_department_exist(request_params['home_company'], request_params['department'])

        return True
