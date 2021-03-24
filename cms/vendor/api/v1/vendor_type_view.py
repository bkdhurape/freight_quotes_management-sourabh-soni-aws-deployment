from django.db import transaction
from rest_framework import generics, status
from utils.responses import success_response
from vendor.serializers import VendorTypeSerializer
from vendor.services.vendor_type_service import VendorTypeService

class VendorTypeView(generics.GenericAPIView):
    serializer_class = VendorTypeSerializer

    # Get all vendor types
    def get(self, request):
        vendor_type_service = VendorTypeService(data=request)
        result = vendor_type_service.get_all()
        if result:
            return success_response(message="Vendor type data retrieved successfully.", data=result)
        else:
            return success_response(message="No more data")

    # Create vendor type
    @transaction.atomic
    def post(self, request):
        vendor_type_service = VendorTypeService(data=request.data)
        response = vendor_type_service.create()
        if response:
            return success_response(message='Vendor type added successfully.')
        else:
            return success_response(status_code=status.HTTP_400_BAD_REQUEST, status='failure',
                                   message='Vendor type creation failure.')


class VendorTypeDetailView(generics.GenericAPIView):
    serializer_class = VendorTypeSerializer

    # Get vendor type details by id
    def get(self, request, id):
        result = VendorTypeService.get(id)
        if result:
            return success_response(message="Vendor type data retrieved successfully.", data=result)
        else:
            return success_response(message="Vendor type data not found.")

    # Update vendor type details
    @transaction.atomic
    def put(self, request, id):
        vendor_type_service = VendorTypeService(data=request.data)
        if vendor_type_service.update(id):
            return success_response(message='Vendor type updated successfully.')
        else:
            return success_response(status_code=status.HTTP_400_BAD_REQUEST, status='failure',
                                   message='Cannot update vendor.')

    # Update status to inactive of vendor type
    @transaction.atomic
    def delete(self, request, id):
        # Update vendor type status to inactive
        if VendorTypeService.delete(id=id):
            return success_response(message="Vendor type removed successfully")
        else:
            return success_response(message="Cannot remove vendor type")
