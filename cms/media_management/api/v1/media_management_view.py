from django.db import transaction
from media_management.serializers import CustomerProfileSerializer,VendorProfileSerializer
from rest_framework import generics
from customer.models.customer import Customer
from vendor.models.vendor import Vendor
from django.conf import settings
from utils.base_models import StatusBase
import json, jwt
from utils.responses import success_response, error_response

class MediaManagementView(generics.GenericAPIView):

    @transaction.atomic
    def post(self, request, user_id):
        jwt_token_decode = jwt.decode(request.headers['Authorization'], settings.JWT_FCT_SECRET, algorithms=['HS256']) 
        if jwt_token_decode['account_type'] == 'customer':
            customer_detail = Customer.objects.filter(id=user_id, status=StatusBase.ACTIVE).first()
            if not customer_detail:
                return error_response(data="customer not found")
            serializer = CustomerProfileSerializer(data=request.data, instance=customer_detail)

        elif 'vendor' == jwt_token_decode['account_type']:
            vendor_detail = Vendor.objects.filter(id=user_id, status=StatusBase.ACTIVE).first()
            if not  vendor_detail:
                return error_response(data="vendor not found")
            serializer = VendorProfileSerializer(data=request.data, instance=vendor_detail)

        if serializer.is_valid():
            serializer.save()
            return success_response(message='Profile Picture Uploaded successfully')
        else:
               return error_response(data=serializer.errors)


    @transaction.atomic
    def delete(self, request, user_id):
        jwt_token_decode = jwt.decode(request.headers['Authorization'], settings.JWT_FCT_SECRET, algorithms=['HS256']) 
        if jwt_token_decode['account_type'] == 'customer' :
            customer_detail = Customer.objects.filter(id=user_id, status=StatusBase.ACTIVE).first()
            if not customer_detail:
                return error_response(data="customer not found")
            customer_detail.profile_picture.delete(save=True)

        elif 'vendor' == jwt_token_decode['account_type']:
            vendor_detail = Vendor.objects.filter(id=user_id, status=StatusBase.ACTIVE).first()
            if not  vendor_detail:
                return error_response(data="vendor not found")
            vendor_detail.profile_picture.delete(save=True)

        return success_response(message="Profie picture removed successfully")