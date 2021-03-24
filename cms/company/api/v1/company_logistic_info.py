from company.decorator import validate_company_logistics_info
from company.models.company_logistic_info import CompanyLogisticInfo
from company.serializers import CompanyLogisticInfoSerializer, AdditionalDetailsCompanySerializer
from company.services import CompanyLogisticInfoService
from django.db import transaction
from rest_framework import generics
from utils.responses import success_response, error_response
import logging
logger = logging.getLogger(__name__)


class CompanyLogisticInfoView(generics.GenericAPIView):

    serializer_class = CompanyLogisticInfoSerializer
    '''To get logistic info for a company'''

    def get(self, request, company_id):
        company_logistic_info = CompanyLogisticInfoService.get(
            company_id=company_id)
        return success_response(
            message="Company logistic info retrived successfully",
            data=company_logistic_info)


class CompanyLogisticInfoDetailView(generics.GenericAPIView):

    serializer_class = CompanyLogisticInfoSerializer

    ''''get company logistic info details based on additional details id'''

    def get(self, request, company_id, company_logistic_id):
        company_logistic_info = CompanyLogisticInfoService.get_details(
            company_id=company_id, id=company_logistic_id)
        return success_response(
            message="Company logistic info retrived successfully",
            data=company_logistic_info)

    '''update company logistic info details based on additional details id'''

    @validate_company_logistics_info
    @transaction.atomic
    def put(self, request, company_id, company_logistic_id):
        request.data['company_logistics'].update({'company':company_id})
        serializer = AdditionalDetailsCompanySerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            CompanyLogisticInfo.services.update_additional_detail(company_id=company_id, id=company_logistic_id, company_logistics=data.get(
                'company_logistics'), currency_profile_details=data.get('currency_profile_details'))
            return success_response(
                message="Company additional details updated successfully")
        return error_response(data=serializer.errors)
