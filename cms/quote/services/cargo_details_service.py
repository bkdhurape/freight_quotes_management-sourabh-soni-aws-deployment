from address.models.address import Address
from company.services.company_service import CompanyService
from exceptions.cargo_details_exception import CargoDetailsException , CargoDetailsError
from exceptions.package_details_exception import PackageDetailsException, PackageDetailsError
from quote.models.package_details import PackageDetails
from quote.models.quote import Quote
from quote.models.quote_order_ready import QuoteOrderReady
from quote.models.quote_transport_mode import QuoteTransportMode
from quote.serializers import PackageDetailsSerializer, QuoteTransportModeSerializer, QuoteOrderReadySerializer
from quote.services.package_details_service import PackageDetailsService
from quote.services.quote_order_ready_service import QuoteOrderReadyService
from quote.services.quote_transport_mode_service import QuoteTransportModeService
from utils.base_models import StatusBase
from utils.responses import get_paginated_data
from utils.total_weight_volume import get_total_weight_volume

class CargoDetailsService:

    def __init__(self, data):
        self.data = data


    def get(self, quote_id):

        Quote.find_by(multi=False, status__ne=Quote.INACTIVE, id=quote_id)

        quote_order_ready_data = QuoteOrderReadyService.get(quote_id)
        quote_transport_mode_data = QuoteTransportModeService.get(quote_id)

        response = { 'transport_mode': quote_transport_mode_data, 'order_ready': quote_order_ready_data}


        return response


    def create(self, company_id, quote_id):

        Quote.find_by(multi=False, status__ne=Quote.INACTIVE, id=quote_id)

        package_details_service = PackageDetailsService(data=self.data)
        package_details_service.create(company_id=company_id, quote_id=quote_id)

        self.update_quote_total_weight_volume(quote_id)
        self.update_quote_order_ready(quote_id)

        return True

    def update(self, company_id, quote_id):

        if 'id' not in self.data:
            raise CargoDetailsException(CargoDetailsError.QUOTE_ORDER_READY_ID_REQUIRED)

        package_details = PackageDetails.find_by(multi=True, quote=quote_id, id=self.data['id'])
        if not package_details:
            raise CargoDetailsException(CargoDetailsError.CANNOT_UPDATE_QUOTE_ORDER_READY)

        package_details_service = PackageDetailsService(data=self.data)
        package_details_service.update(company_id=company_id, quote_id=quote_id, id=self.data['id'])

        self.update_quote_total_weight_volume(quote_id)
        self.update_quote_order_ready(quote_id)

        return True



    def update_quote_total_weight_volume(self, quote_id):
        quote_transport_modes = list(QuoteTransportMode.find_by(multi=True, quote=quote_id).values_list('id', 'transport_mode'))

        for quote_transport_mode in quote_transport_modes:

            package_transport_mode = PackageDetails.find_by(multi=True, transport_mode=quote_transport_mode[0] )

            if package_transport_mode:
                package_details_serializer = PackageDetailsSerializer(package_transport_mode, many=True)
                package_details = package_details_serializer.data
                total_weight_volume_data = get_total_weight_volume(package_details = package_details, transport_mode = quote_transport_mode[1])

                self.update_quote_transport_mode(total_weight_volume_data, quote_id, quote_transport_mode[0])



    def update_quote_order_ready(self, quote_id):

        response = {}

        quote_shipment_term = list(Quote.find_by(multi=True, status__ne=Quote.INACTIVE, id=quote_id).values_list('shipment_terms', flat=True))[0]
        shipment_term = quote_shipment_term.split("_")

        self.order_ready_validations(quote_id, shipment_term)


        package_transport_mode = PackageDetails.find_by(multi=True, quote=quote_id )

        if package_transport_mode:
            package_details_serializer = PackageDetailsSerializer(package_transport_mode, many=True)
            package_details = package_details_serializer.data

            if shipment_term[0] == 'port':
                total_weight_volume_data = get_total_weight_volume(package_details = package_details)
                order_ready_data = { **self.data, **total_weight_volume_data }
                self.create_order_ready(order_ready_data, quote_id)

            else:
                for package_detail in package_details:
                    for transport_mode in package_detail['transport_mode']:
                        response[str(transport_mode)+'_'+str(package_detail['pickup_location'])] = str(transport_mode)+'_'+str(package_detail['pickup_location'])

                self.save_order_ready(response, quote_id)



    def save_order_ready(self, response, quote_id):
        for data in response:
            package_detail_data = data.split("_")
            package_transport_mode = PackageDetails.find_by(multi=True, transport_mode=package_detail_data[0], pickup_location=package_detail_data[1] )

            if package_transport_mode:
                package_details_serializer = PackageDetailsSerializer(package_transport_mode, many=True)
                package_details = package_details_serializer.data
                total_weight_volume_data = get_total_weight_volume(package_details = package_details)

                if int(package_detail_data[0]) in self.data['transport_mode']:

                    order_ready_data = { **self.data, **total_weight_volume_data }
                    order_ready_data['quote'] = quote_id
                    order_ready_data['transport_mode'] = package_detail_data[0]
                    order_ready_data['address'] = package_detail_data[1]

                    quote_order_ready = QuoteOrderReady.find_by(multi=True, transport_mode=package_detail_data[0], address=package_detail_data[1])

                    if not quote_order_ready:
                        self.create_or_update_order_ready(data = order_ready_data)
                    else:
                        quote_order_ready_id = list(quote_order_ready.values_list('id', flat=True))
                        self.create_or_update_order_ready(data = order_ready_data, action = 'update', id = quote_order_ready_id[0])


    def create_or_update_order_ready(self, data, action = 'create', id = None):
        quote_order_ready_service = QuoteOrderReadyService(data=data)

        if action == 'create':
            quote_order_ready_service.create()
        else:
            quote_order_ready_service.update(id)


    def update_quote_transport_mode(self, data, quote_id, quote_transport_mode_id):
        data['quote'] = quote_id
        quote_transport_mode_service = QuoteTransportModeService(data=data)
        quote_transport_mode_service.update(quote_transport_mode_id)


    def order_ready_validations(self, quote_id, shipment_term):

        if shipment_term[0] == 'door':

            self.data['handover_date'] = None

            if 'is_order_ready' not in self.data:
                raise CargoDetailsException(CargoDetailsError.QUOTE_ORDER_READY_REQUIRED)

            if 'is_order_ready' in self.data and not self.data['is_order_ready'] and ('order_ready_date' not in self.data or not self.data['order_ready_date']):
                raise CargoDetailsException(CargoDetailsError.QUOTE_ORDER_READY_DATE_REQUIRED)

        if shipment_term[0] == 'port':

            self.data['order_ready_date'] = None

            if 'handover_date' not in self.data or not self.data['handover_date']:
                raise CargoDetailsException(CargoDetailsError.QUOTE_HANDOVER_DATE_REQUIRED)


        if 'invoice_value' not in self.data or not self.data['invoice_value']:
            raise CargoDetailsException(CargoDetailsError.QUOTE_INVOICE_VALUE_REQUIRED)

        if 'invoice_value_currency' not in self.data or not self.data['invoice_value_currency']:
            raise CargoDetailsException(CargoDetailsError.QUOTE_INVOICE_VALUE_CURRENCY_REQUIRED)
