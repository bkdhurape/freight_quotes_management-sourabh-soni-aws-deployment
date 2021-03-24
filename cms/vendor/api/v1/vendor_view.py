from company.models.company import Company
from django.db import transaction
from rest_framework import generics, status
from rest_framework.decorators import api_view
from utils.responses import success_response, error_response
from vendor.models.vendor import Vendor
from vendor.serializers import VendorSerializer, VendorRegistrationSerializer, VendorUpdateSerializer
from vendor.services.vendor_manage_service import VendorManageService
from vendor.services.vendor_service import VendorService


class VendorView(generics.GenericAPIView):
    serializer_class = VendorSerializer

    # Get all vendors
    def get(self, request, company_id):
        vendor_service = VendorService(data=request)
        result = vendor_service.get_vendor_details(request, company_id)
        if result:
            return success_response(message="Vendor Data retrieved successfully.", data=result)
        else:
            return success_response(message='No more records')

    # Create vendor
    @transaction.atomic
    def post(self, request, company_id=None, token=None):
        request.data['home_company'] = company_id
        request.data['is_super_admin'] = False
        _organization_id = Company.objects.get(id=company_id).organization.id
        serializer = VendorUpdateSerializer(data=request.data, context={'organization_id': _organization_id})
        if serializer.is_valid():
            serializer.save()
            return success_response(message='Vendor added successfully.')
        return error_response(data=serializer.errors)


class VendorDetailView(generics.GenericAPIView):
    serializer_class = VendorSerializer

    # Get vendor details by id
    def get(self, request, company_id, id):
        result = VendorService.get_vendor_detail_by_id(
            company_id, id)
        if result:
            return success_response(message="Vendor Data retrieved successfully.", data=result)
        else:
            return success_response(message="Vendor data not found.")

    # Update vendor details
    @transaction.atomic
    def put(self, request, company_id, id):
        request.data['home_company'] = company_id
        _organization_id = Company.objects.get(id=company_id).organization.id
        _vendor = Vendor.objects.get(id=id)
        serializer = VendorUpdateSerializer(_vendor, data=request.data,
                                            context={'organization_id': _organization_id})
        if serializer.is_valid():
            serializer.save()
            return success_response(message='Vendor updated successfully.')
        return error_response(data=serializer.errors)

    # Update status to inactive of vendor
    @transaction.atomic
    def delete(self, request, company_id, id):

        # Delete vendor supervisor
        VendorManageService.update_vendor_supervisors_mapping(company_id, id)

        return success_response(message="Vendor removed successfully")


@api_view(['POST'])
@transaction.atomic
def create_vendor(request):
    serializer = VendorRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        Vendor.services.registration(vendor_details=data.get('vendor_details'),
                                     address_details=data.get('address_details'))
        return success_response(message='Vendor registered successfully')
    return error_response(data=serializer.errors)
