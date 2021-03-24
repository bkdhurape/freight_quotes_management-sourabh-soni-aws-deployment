from address.models.address import Address
from django.conf import settings
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from quote.decorators import validate_quote_info
from quote.models.quote import Quote
from quote.serializers import QuoteSerializer, QuoteCreationSerializer,QuoteUpdateSerializer,QuoteListingSerializers,QuoteListingUpdateSerializer
from quote.services.quote_service import QuoteService
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from utils.base_models import StatusBase
from django.conf import settings
from address.models.address import Address
import json, jwt
from rest_framework import filters
from utils.responses import success_response, error_response
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from quote.decorators import validate_quote_info
import datetime


class QuoteView(generics.GenericAPIView):
    serializer_class = QuoteSerializer

    @transaction.atomic
    def post(self, request, company_id):
        jwt_token_decode = jwt.decode(request.headers['Authorization'], settings.JWT_FCT_SECRET, algorithms=['HS256'])
        customer_home_company_country = \
        Address.objects.filter(entity_type='company', entity_id=jwt_token_decode['home_company']).values('country')[0]
        data = request.data
        serializer = QuoteCreationSerializer(data=request.data, context=request.data.get('basic_details', {})
                                             .get('transport_mode', []))
        if serializer.is_valid():
            data = serializer.validated_data
            Quote.services.create_quote(company_id=company_id, basic_details=data['basic_details'],
                                        cargo_details=data['cargo_details'],
                                        additional_details=data['additional_details'],
                                        customer_home_company_country=customer_home_company_country)
            return success_response(message='Quote created successfully.')
        return error_response(data=serializer.errors)


class QuoteDetailView(generics.GenericAPIView):

    def get(self, request, company_id, quote_id):

        quote_service = QuoteService({})
        result = quote_service.get_by_id(
            company_id=company_id, quote_id=quote_id)
        if result:

            return success_response(message='Quote data retrived successfully', data=result)
        else:
            return success_response(message='No data found')

    @validate_quote_info
    def put(self, request, company_id, quote_id):

        jwt_token_decode = jwt.decode(request.headers['Authorization'], settings.JWT_FCT_SECRET, algorithms=['HS256'])
        customer_home_company_country = \
        Address.objects.filter(entity_type='company', entity_id=jwt_token_decode['home_company']).values('country')[0]
        data = request.data
        quote_object = Quote.objects.get(company=company_id, id=quote_id)
        serializer = QuoteUpdateSerializer(quote_object, data=data, context=request.data.get('basic_details', {})
                                           .get('transport_mode', []))
        if serializer.is_valid():
            data = serializer.validated_data
            Quote.services.update_quote(company_id=company_id, quote_id=quote_id, basic_details=data['basic_details'],
                                        cargo_details=data['cargo_details'],
                                        additional_details=data['additional_details'],
                                        customer_home_company_country=customer_home_company_country)
            return success_response(message='Quote updated successfully.')
        return error_response(data=serializer.errors)

    @validate_quote_info
    def delete(self, request, company_id, quote_id):

        quote_data = Quote.objects.get(company_id=company_id, id=quote_id)
        quote_data.status = StatusBase.INACTIVE
        quote_data.save()
        return success_response(message='Quote deleted successfully')


class CustomResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data,
            'message': "Quote Data Retreive Successfully",
            'status_code': status.HTTP_200_OK
        })


class QuoteListView(generics.ListAPIView):
    model = Quote
    pagination_class = CustomResultsSetPagination
    serializer_class = QuoteListingSerializers
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['^shipment_term','pickup_location']
    filterset_fields = ['quote_status','id']

    def get_queryset(self):
        queryset = Quote.objects.filter(~Q(status=StatusBase.INACTIVE), company_id=self.kwargs['company_id']).order_by(
            'id')
        quote_status = self.request.query_params.get('status', None)
        quote_deadline = self.request.query_params.get('quote_deadline_order', None)
        quote_no = self.request.query_params.get('quote_no_order', None)
        transport_modes = self.request.query_params.get('transport_modes_order', None)
        if quote_status is not None:
            if quote_status == 'close':
                queryset = queryset.filter(quote_status__in=["expired", "booked", 'cancelled'])
            else:
                queryset = queryset.filter(quote_status=quote_status)

        elif quote_deadline is not None:
            if quote_deadline == 'dec':
                queryset = queryset.order_by("-quote_deadline")
            else:
                queryset = queryset.order_by("quote_deadline")

        elif quote_no is not None:
            if quote_no == 'dec':
                queryset = queryset.order_by("-created_at")
            else:
                queryset = queryset.order_by("created_at")

        # elif transport_modes is not None:
        #     if transport_modes == 'dec':
        #         queryset = queryset.order_by("-transport_modes")
        #     else:
        #         queryset = queryset.order_by("transport_modes")

        return queryset


# Creating duplicate quote
@api_view(['POST'])
@transaction.atomic
def create_duplicate_quote(request, company_id, quote_id):

    Quote.services.duplicate_quote(company_id=company_id, quote_id=quote_id)
    return success_response(message='Duplicate quote created successfully')

class QuoteListingUpdate(generics.GenericAPIView):
    @validate_quote_info
    @transaction.atomic
    def put(self, request, company_id, quote_id):
        data = request.data
        quote_object = Quote.objects.get(company=company_id, id=quote_id)
        serializer = QuoteListingUpdateSerializer(quote_object, data=data)
        if serializer.is_valid():
            data = serializer.validated_data
            Quote.services.update_manage_quote(company_id=company_id, quote_id=quote_id,data=data)
            return success_response(message="Quote updated successfully")
        return error_response(data=serializer.errors)

