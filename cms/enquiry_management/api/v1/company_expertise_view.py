from django.db import transaction
from enquiry_management.models.company_expertise import CompanyExpertise
from enquiry_management.serializers import CompanyExpertiseBaseSerializer
from enquiry_management.services.company_expertise_service import CompanyExpertiseService
from enquiry_management.services.company_expertise_manage_service import CompanyExpertiseManageService
from rest_framework import generics
from enquiry_management.decorator import validate_company_expertise_id
from utils.responses import success_response, error_response
from utils.base_models import StatusBase


class CompanyExpertiseView(generics.GenericAPIView):
    serializer_class = CompanyExpertiseBaseSerializer

    @transaction.atomic
    def post(self, request, company_id):
        data = request.data    
        data['company'] =  company_id
        serializer = CompanyExpertiseBaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message='company expertise added successfully')
        return error_response(data=serializer.errors)

    def get(self, request, company_id):

        company_expertise_service = CompanyExpertiseService(
            data=request)
        response = company_expertise_service.get(company_id=company_id)
        if response:
            return success_response(message="Company Expertise data retrieved successfully.", data=response)
        else:
            return success_response(message="No more records")


class CompanyExpertiseDetailView(generics.GenericAPIView):
    serializer_class = CompanyExpertiseBaseSerializer

    def get(self, request, company_id,expertise_id):

        company_expertise_service = CompanyExpertiseService({})
        response = company_expertise_service.get(company_id=company_id,id=expertise_id)

        return success_response(message="Company Expertise data retrieved successfully.", data=response)

    @validate_company_expertise_id
    @transaction.atomic
    def put(self, request, company_id, expertise_id):
        data = request.data    
        company_expertise_object = CompanyExpertise.objects.get(company=company_id,id=expertise_id)
        serializer = CompanyExpertiseBaseSerializer(company_expertise_object,data=data,exclude=['company'])
        if serializer.is_valid():
            serializer.save()
            return success_response(message='Company Expertise data updated successfully')
        return error_response(data=serializer.errors)

    @validate_company_expertise_id
    @transaction.atomic
    def delete(self, request, company_id, expertise_id):
        company_expertise_data = CompanyExpertise.objects.get(company_id = company_id, id = expertise_id, status=StatusBase.ACTIVE)
        company_expertise_data.delete()
        return success_response(message="Company Expertise deleted successfully")
