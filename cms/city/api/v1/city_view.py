from city.models.city import City
from city.serializers import CitySerializer
from country.models.country import Country
from django.db import transaction
from rest_framework import generics
from state.models.state import State
from utils.responses import success_response


class CityView(generics.GenericAPIView):
    serializer_class = CitySerializer

    @transaction.atomic
    def get(self, request, country_id, state_id):
        Country.find_by(id=country_id)
        State.find_by(country=country_id, id=state_id)
        city_list = City.find_by(multi=True, state=state_id).order_by('name')
        city_result =  CitySerializer(city_list, many=True, fields=['id', 'state', 'name']).data
        if city_result:
            return success_response(message="City Data retrieved successfully.", data=city_result)
        else:
            return success_response(message='No record found.')


class CityDetailView(generics.GenericAPIView):
    serializer_class = CitySerializer

    @transaction.atomic
    def get(self, request, country_id, state_id, id):
        Country.find_by(id=country_id)
        State.find_by(country=country_id, id=state_id)
        City.find_by(state=state_id, id=id)
        city_list = City.find_by(multi=True, state=state_id, id=id)
        city_result =  CitySerializer(city_list, many=True, fields=['id', 'state', 'name']).data
        if city_result:
            return success_response(message="City Data retrieved successfully.", data=city_result)
        else:
            return success_response(message='No record found.')
