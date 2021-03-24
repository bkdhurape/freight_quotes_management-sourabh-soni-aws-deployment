from company.models.company import Company
from currency.models.currency_profile import CurrencyProfile
from currency.services.currency_profile_service import CurrencyProfileService
from customer.models.customer import Customer
from customer.serializers import CustomerDetailSerializer, CustomerSerializer
from datetime import datetime
from department.models.department import Department
from django.conf import settings
from exceptions import CustomerException, CustomerError
from notification.managers.email_manager import EmailNotification
from utils.base_models import StatusBase
from utils.responses import get_paginated_data
from utils.helpers import generate_token_data


class CustomerService:

    def __init__(self, data):
        self.data = data

    def update(self, customer_id):

        # Check company department exist or not
        CustomerService.company_department_exist(
            self.data['home_company'], self.data['department'])

        customer = Customer.find_by_ids(id=customer_id)
        self.data['id'] = customer_id
        customer_serializer = CustomerSerializer(customer, data=self.data)

        if customer_serializer.is_valid(raise_exception=True):
            customer_serializer.save()

    # Update customer status to inactive
    def delete(customer_id):
        customer = Customer.find_by(id=customer_id, status=StatusBase.ACTIVE)
        customer.status = StatusBase.INACTIVE
        customer.save()

    # Get all customer details with customer & currency details
    def get_customer_details(self, request, company_id):
        result = []
        Company.find_by(id=company_id)
        filter_params = {
            'home_company': company_id,
            'status__in': [Customer.ACTIVE, Customer.PENDING]
        }
        if ('name' in request.GET) and (request.GET['name'].strip()):
            filter_params.update({'name__icontains': request.GET['name']})

        customer_data = Customer.find_by(
            multi=True, **filter_params).order_by('-id')

        customer_paginated_data = get_paginated_data(
            CustomerDetailSerializer, customer_data, self.data)
        if customer_paginated_data:

            for customer in customer_paginated_data:
                id = int(customer['id'])
                currency_profile_dicts = CurrencyProfileService.get_currency_profile(entity_type='customer',
                                                                                     entity_id=id)
                result.append({
                    'customer_data': customer,
                    'currency_profile_data': currency_profile_dicts
                })

            return result
        else:
            return False

    # Get customer & currency profile data by customer ID
    def get_customer_detail_by_id(company_id, id):
        Company.find_by(id=company_id)
        customer_data = Customer.find_by(
            multi=True, join=False, id=id, home_company=company_id, status__ne=Customer.INACTIVE)
        if not customer_data:
            return False

        customer_serializer = CustomerDetailSerializer(
            customer_data, many=True)
        customer = customer_serializer.data[0]

        currency_profile_dicts = CurrencyProfileService.get_currency_profile(
            entity_type='customer', entity_id=id)

        result = {
            'customer_data': customer,
            'currency_profile_data': currency_profile_dicts
        }

        return result

    # Check company department exist or not
    def company_department_exist(company_id, department_id_list):
        Company.find_by(id=company_id, status=StatusBase.ACTIVE)

        for department_id in department_id_list:
            department_exist = Department.find_by(
                multi=True, company=company_id, id=department_id)
            if not department_exist:
                raise CustomerException(
                    CustomerError.CUSTOMER_COMPANY_DEPARTMENT_NOT_EXISTS)


    def add_customer(params):
        # Create Customer
        customer_details = params['customer_details']
        customer_company = customer_details['company']
        customer_details.pop('company')
        customer_department = customer_details['department']
        customer_details.pop('department')
        customer_supervisor = customer_details['supervisor']
        customer_details.pop('supervisor')
        customer_object = Customer.objects.create(**customer_details)
        customer_object.company.set(customer_company)
        customer_object.department.set(customer_department)
        customer_object.supervisor.set(customer_supervisor)
        token_hash, token = generate_token_data(customer_details['email'], 'customer')
        customer_object.registration_token = token
        customer_object.token_date = datetime.now()
        customer_object.save()

        # Bulk Create Customer Companies Currency Details
        companies = params['companies']
        bulk_currency_obj = []
        for company in companies:
            currency_profile_params = {
                "entity_type": "customer",
                "entity_id": customer_object.id,
                "company": company['company'],
                "air_currency": company['currency_details']['air_currency'],
                "lcl_currency": company['currency_details']['lcl_currency'],
                "fcl_currency": company['currency_details']['fcl_currency']
            }
            bulk_currency_obj.append(CurrencyProfile(**currency_profile_params))
        CurrencyProfile.objects.bulk_create(objs=bulk_currency_obj)

        link = settings.FRONTEND_URL + '/set-profile/' + token_hash
        email_data = {
            'customer_name': customer_details['name'],
            'customer_email': customer_details['email'],
            'link': link,
        }
        EmailNotification.set_profile_email(email_data)

        return link