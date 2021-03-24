from django.db import transaction
from quote.serializers import QuoteTransportModeSerializer
from quote.services.cargo_details_service import CargoDetailsService
from rest_framework import generics
from utils.responses import success_response

class CargoDetailsView(generics.GenericAPIView):
    serializer_class = QuoteTransportModeSerializer


    def get(self, request, company_id, quote_id):

        cargo_details_service = CargoDetailsService(data=request)
        result = cargo_details_service.get(quote_id=quote_id)
        if result:
            return success_response(message='Cargo Details retrived successfully', data=result)
        else:
            return success_response(message='No more records')


    @transaction.atomic
    def post(self, request, company_id, quote_id):
        cargo_details_service = CargoDetailsService(data=request.data)
        result = cargo_details_service.create(company_id = company_id, quote_id=quote_id)
        if result:
            return success_response(message="Cargo details added successfully")
        else:
            return success_response(message="Failed to add cargo details")


    @transaction.atomic
    def put(self, request, company_id, quote_id):
        cargo_details_service = CargoDetailsService(data=request.data)
        result = cargo_details_service.update(company_id = company_id, quote_id=quote_id)
        if result:
            return success_response(message="Cargo Details updated successfully")
        else:
            return success_response(message="Failed to update cargo details")
