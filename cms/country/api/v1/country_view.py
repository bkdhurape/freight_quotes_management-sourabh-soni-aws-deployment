from country.models.country import Country
from country.serializers import CountrySerializer
from django.db import transaction
from rest_framework import generics
from utils.responses import success_response


class CountryView(generics.GenericAPIView):
    serializer_class = CountrySerializer

    @transaction.atomic
    def get(self, request):
        country_list = Country.find_by(multi=True).order_by('name')
        country_result =  CountrySerializer(country_list, many=True, fields=['id', 'name', 'code', 'currency_code']).data
        if country_result:
            return success_response(message="Country Data retrieved successfully.", data=country_result)
        else:
            return success_response(message='No record found.')


class CountryDetailView(generics.GenericAPIView):
    serializer_class = CountrySerializer

    @transaction.atomic
    def get(self, request, id):
        Country.find_by(id=id)
        country_list = Country.find_by(multi=True, id=id)
        country_result =  CountrySerializer(country_list, many=True, fields=['id', 'name', 'code', 'currency_code']).data
        if country_result:
            return success_response(message="Country Data retrieved successfully.", data=country_result)
        else:
            return success_response(message='No record found.')
