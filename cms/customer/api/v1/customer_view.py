from company.models.company import Company
from customer.models.customer import Customer
from customer.serializers import CustomerSerializer, CustomerRegistrationSerializer, AddCustomerSerializer, \
    CustomerUpdateSerializer
from customer.services.customer_manage_service import CustomerManageService
from customer.services.customer_service import CustomerService
from django.db import transaction
from django.utils.decorators import method_decorator
from customer.decorators import validate_customer_company
from rest_framework import generics, status
from rest_framework.decorators import api_view
from utils.responses import success_response, error_response


class CustomerView(generics.GenericAPIView):
    serializer_class = CustomerSerializer

    @transaction.atomic
    def get(self, request, company_id):
        customer_service = CustomerService(data=request)
        customer_result = customer_service.get_customer_details(
            request, company_id)
        if customer_result:
            return success_response(message="Customer Data retrieved successfully.", data=customer_result)
        else:
            return success_response(message='No more records')

    @transaction.atomic
    def post(self, request, company_id):
        request.data['home_company'] = company_id
        request.data['is_super_admin'] = False
        _organization_id = Company.objects.get(id=company_id).organization.id
        serializer = CustomerUpdateSerializer(data=request.data, context={'organization_id': _organization_id})
        if serializer.is_valid():
            serializer.save()
            return success_response(message='Customer added successfully.')
        return error_response(data=serializer.errors)


class CustomerDetailView(generics.GenericAPIView):
    serializer_class = CustomerSerializer

    @transaction.atomic
    def get(self, request, company_id, id):
        result = CustomerService.get_customer_detail_by_id(company_id, id)
        if result:
            return success_response(message="Customer Data retrieved successfully.", data=result)
        else:
            return success_response(message="Customer data not found.")

    @method_decorator(validate_customer_company)
    @transaction.atomic
    def put(self, request, company_id, id):
        request.data['home_company'] = company_id
        _organization_id = Company.objects.get(id=company_id).organization.id
        _customer = Customer.objects.get(id=id)
        serializer = CustomerUpdateSerializer(_customer, data=request.data, context={'organization_id': _organization_id, 'id':id},exclude=["email"])
        if serializer.is_valid():
            serializer.save()
            return success_response(message='Customer updated successfully.')
        return error_response(data=serializer.errors)

    # Update status to inactive of customer
    @transaction.atomic
    def delete(self, request, company_id, id):
        # Delete customer supervisor
        CustomerManageService.update_customer_supervisors_mapping(
            company_id, id)
        return success_response(message="Customer removed successfully.")


@api_view(['POST'])
@transaction.atomic
def create_customer(request):
    serializer = CustomerRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        Customer.services.registration(customer_details=data['customer_details'],
                                                         company_details=data.get('company_details'),
                                                         additional_details=data.get('additional_details'))
        return success_response(message='We have sent an email to your registered email-id, open it up to activate your account')
    return error_response(data=serializer.errors)