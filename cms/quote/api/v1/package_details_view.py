from django.db import transaction
from quote.serializers import PackageDetailsSerializer
from quote.services.package_details_service import PackageDetailsService
from rest_framework import generics
from utils.responses import success_response

class PackageDetailsView(generics.GenericAPIView):
    serializer_class = PackageDetailsSerializer

    @transaction.atomic
    def post(self, request, company_id, quote_id):

        package_details_service = PackageDetailsService(data=request.data)
        result = package_details_service.create(company_id=company_id, quote_id=quote_id)
        if result:
            return success_response(message='Package details added successfully')
        else:
            return success_response(message="Failed to add package details")



    def get(self, request, company_id, quote_id):

        package_details_service = PackageDetailsService(data=request)
        result = package_details_service.get(company_id=company_id, quote_id=quote_id)
        if result:
            return success_response(message="Package details are retrieved successfully", data=result)
        else:
            return success_response(message="No more records")

class PackageDetailsIdView(generics.GenericAPIView):

    def get(self, request, company_id, quote_id, package_details_id):

        package_details_service = PackageDetailsService({})
        result = package_details_service.get_by_id(company_id=company_id, quote_id=quote_id, package_details_id=package_details_id)
        if result:
            return success_response(message="Package details retrieved successfully", data=result)
        else:
            return success_response(message="No data found")
