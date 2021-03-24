from django.db import transaction
from quote.serializers import QuoteSerializer
from quote.services.additional_details_service import AdditionalDetailsService
from rest_framework import generics
from utils.responses import success_response

class AdditionalDetailsView(generics.GenericAPIView):
    serializer_class = QuoteSerializer

    @transaction.atomic
    def post(self, request, company_id, quote_id):

        additional_details_service = AdditionalDetailsService(data=request.data)
        result = additional_details_service.update(company_id=company_id, quote_id=quote_id)
        if result:
            return success_response(message="Additional details added successfully")
        else:
            return success_response(message="Failed to add additional details")

    @transaction.atomic
    def put(self, request, company_id, quote_id):

        additional_details_service = AdditionalDetailsService(data=request.data)
        result = additional_details_service.update(company_id=company_id, quote_id=quote_id)
        if result:
            return success_response(message="Additional details updated successfully")
        else:
            return success_response(message="Failed to add additional details")



