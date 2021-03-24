from company.managers.company_manager import CompanyManager, CompanyServiceManager
from company.decorator import validate_company
from company.models.company import Company
from company.serializers import CompanySerializer
from company.serializers import CompanyUpdateSerializer,CompanyAddSerializer,CompanyBaseSerializer
from company.services import CompanyService, CompanyManageService
from django.db import transaction
from rest_framework import generics
from utils.responses import success_response,error_response
import logging

logger = logging.getLogger(__name__)


class CompanyView(generics.GenericAPIView):

    serializer_class = CompanySerializer
    '''get  all company details'''

    def get(self, request):
        company_service = CompanyService(data=request)
        company_result = company_service.get(address_details=True)
        if company_result:

            return success_response(message="Company Data retrived successfully",
                                    data=company_result)
        else:
            return success_response(message="No more records")

    '''create or add  new company'''
    @transaction.atomic
    def post(self, request):
        serializer = CompanyAddSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            Company.services.add_company(company_details=data.get(
                'company_info'), address_details=data.get('address_details'))

            return success_response(message='Company Details added successfully.', data=None)
        return error_response(data=serializer.errors)


class CompanyDetailView(generics.GenericAPIView):

    serializer_class = CompanySerializer
    '''get  all company details based on id'''

    def get(self, request, company_id):
        company_service = CompanyService({})
        company_result = company_service.get(id=company_id, address_details=True)
        return success_response(message="Company Data retrived successfully",
                                data=company_result)
    '''delete company details based on id'''
    @transaction.atomic
    def delete(self, request, company_id):
        company_details = CompanyService.delete(company_id=company_id)
        return success_response(message="Company removed successfully")

    '''edit company details based on id'''
    @transaction.atomic
    def put(self, request, company_id):
        company = Company.objects.get(id=company_id)
        serializer = CompanyUpdateSerializer(company, data=request.data, context={'id':company_id})
        if serializer.is_valid():
            data = serializer.validated_data

            Company.services.update_company(company_details=data.get(
                'company_info'), address_details=data.get('address_details'), id=company_id)

            return success_response(message='Company Details Updated successfully.', data=None)
        return error_response(data=serializer.errors)
