from company.models.company import Company
from customer.models.invited_vendor import InvitedVendor
from customer.serializers import InvitedVendorSerializer, DeleteInvitedVendorSerializer
from customer.services.invited_vendor_service import InvitedVendorService
from django.db import transaction
from rest_framework import generics, status
from utils.base_models import StatusBase
from utils.responses import success_response, error_response


class InvitedVendorView(generics.GenericAPIView):
    serializer_class = InvitedVendorSerializer

    @transaction.atomic
    def get(self, request, company_id, customer_id):
        invited_vendor_service = InvitedVendorService(data=request)
        invited_vendor_data = invited_vendor_service.get_all(company_id, customer_id, user_type='customer')

        if invited_vendor_data:
            return success_response(message="Invited Vendor Data retrieved successfully.", data=invited_vendor_data)
        else:
            return success_response(message='No more records')

    @transaction.atomic
    def post(self, request, company_id, customer_id):
        request.data['customer'] = customer_id
        request.data['customer_company'] = company_id
        request.data['vendor_company'] = None
        request.data['vendor'] = None

        serializer = InvitedVendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message='Vendor invited successfully.')
        return error_response(data=serializer.errors)
        # invited_vendor_service = InvitedVendorService(data=request.data)
        # data = invited_vendor_service.create(customer_company_id=company_id, customer_id = customer_id)
        # if 'success' == data['status']:
        #     return success_response(message='Vendor invited successfully.', data=data['data'])
        # else:
        #     return success_response(status_code=status.HTTP_400_BAD_REQUEST, status='failure',
        #                             message='Invited Vendor creation failure.')


class InvitedVendorDetailView(generics.GenericAPIView):
    serializer_class = InvitedVendorSerializer

    @transaction.atomic
    def get(self, request, company_id, customer_id, id):
        invited_vendor_service = InvitedVendorService({})
        result = invited_vendor_service.get(id)
        if result:
            return success_response(message="Invited vendor data retrieved successfully.", data=result)
        else:
            return success_response(message="Invited vendor data not found.")

    @transaction.atomic
    def delete(self, request, company_id, customer_id, id):
        data = {'company': company_id, 'customer': customer_id, 'id': id}
        serializer = DeleteInvitedVendorSerializer(data=data)
        if serializer.is_valid():
            InvitedVendor.services.delete(company_id=company_id, customer_id=customer_id, id=id)
            return success_response(message="Invite vendor removed successfully")
        return error_response(data=serializer.errors)

        # # Delete invited
        # InvitedVendorService.delete(company_id, customer_id, id)
        # return success_response(message="Vendor invite delete successfully")
