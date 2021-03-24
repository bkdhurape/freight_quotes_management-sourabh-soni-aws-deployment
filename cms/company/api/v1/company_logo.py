from company.decorator import validate_company
from company.models.company import Company
from company.serializers import CompanyBaseSerializer
from django.db import transaction
from rest_framework import generics
from utils.responses import success_response, error_response


class CompanyLogo(generics.GenericAPIView):

    @validate_company
    @transaction.atomic
    def put(self, request, company_id):
        company = Company.objects.get(id=company_id)
        serializer = CompanyBaseSerializer(company, data=request.data,fields=['company_logo'])
        if serializer.is_valid():
            serializer.save()
            return success_response(message='Company Logo Updated successfully.')
        return error_response(data=serializer.errors)

    @validate_company
    @transaction.atomic
    def delete(self, request, company_id):
        company_detail = Company.objects.get(id=company_id)
        company_detail.company_logo.delete(save=True)
        return success_response(message="Company Logo removed successfully")