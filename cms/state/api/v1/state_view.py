from country.models.country import Country
from django.db import transaction
from rest_framework import generics
from state.models.state import State
from state.serializers import StateSerializer
from utils.responses import success_response


class StateView(generics.GenericAPIView):
    serializer_class = StateSerializer

    @transaction.atomic
    def get(self, request, country_id):
        Country.find_by(id=country_id)
        state_list = State.find_by(multi=True, country=country_id).order_by('name')
        state_result =  StateSerializer(state_list, many=True, fields=['id', 'country', 'name']).data
        if state_result:
            return success_response(message="State Data retrieved successfully.", data=state_result)
        else:
            return success_response(message='No record found.')


class StateDetailView(generics.GenericAPIView):
    serializer_class = StateSerializer

    @transaction.atomic
    def get(self, request, country_id, id):
        Country.find_by(id=country_id)
        State.find_by(country=country_id, id=id)
        state_list = State.find_by(multi=True, country=country_id, id=id)
        state_result =  StateSerializer(state_list, many=True, fields=['id', 'country', 'name']).data
        if state_result:
            return success_response(message="State Data retrieved successfully.", data=state_result)
        else:
            return success_response(message='No record found.')
