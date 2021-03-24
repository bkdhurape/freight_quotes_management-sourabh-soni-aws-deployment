from django.db import transaction
from rest_framework import generics
from transport.models.transport import Transport
from transport.serializers import TransportSerializer
from utils.responses import success_response


class TransportView(generics.GenericAPIView):
    serializer_class = TransportSerializer

    @transaction.atomic
    def get(self, request):
        transport_list = Transport.find_by(multi=True).order_by('type')
        if transport_list:
            transport_result =  TransportSerializer(transport_list, many=True, fields=['id', 'name', 'code', 'type']).data
            if transport_result:
                return success_response(message="Transport Data retrieved successfully.", data=transport_result)
        return success_response(message='No record found.')


class TransportDetailView(generics.GenericAPIView):
    serializer_class = TransportSerializer

    @transaction.atomic
    def get(self, request, id):
        transport_list = Transport.find_by(multi=True, id=id)
        if transport_list:
            transport_result =  TransportSerializer(transport_list, many=True, fields=['id', 'name', 'code', 'type']).data
            if transport_result:
                return success_response(message="Transport Data retrieved successfully.", data=transport_result)
        
        return success_response(message='No record found.')
