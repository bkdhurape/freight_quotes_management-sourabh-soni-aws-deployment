from company.models.company import Company
from customer.models.invited_vendor import InvitedVendor
from customer.serializers import InvitedVendorSerializer, InvitedVendorUpdateSerializer
from customer.services.invited_vendor_service import InvitedVendorService
from django.db import transaction
from rest_framework import generics, status
from utils.base_models import StatusBase
from utils.responses import success_response, error_response


class VendorClientView(generics.GenericAPIView):
    serializer_class = InvitedVendorSerializer

    # Get all vendor types
    def get(self, request, company_id, vendor_id):
        invited_vendor_service = InvitedVendorService(data=request)
        invited_vendor_data = invited_vendor_service.get_all(company_id, vendor_id, user_type = 'vendor')

        if invited_vendor_data:
            return success_response(message="Vendor clients data retrieved successfully.", data=invited_vendor_data)
        else:
            return success_response(message="No more data")


class VendorClientDetailView(generics.GenericAPIView):
    serializer_class = InvitedVendorSerializer

    # Update vendor type details
    @transaction.atomic
    def put(self, request, company_id, vendor_id, id, action):
        _invited_vendor = InvitedVendor.objects.get(id=id)
        data = {'vendor_company': company_id, 'vendor': vendor_id, 'id': id, 'action': action}
        serializer = InvitedVendorUpdateSerializer(_invited_vendor, data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message='Vendor client updated successfully.')
        return error_response(data=serializer.errors)

