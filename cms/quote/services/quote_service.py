from address.models.address import Address
from address.serializers import AddressSerializer
from address.services.address_service import AddressService
from exceptions.quote_exceptions import QuoteError, QuoteException
from quote.models.package_details import PackageDetails
from quote.models.quote import Quote
from quote.models.quote_transport_mode import QuoteTransportMode
from quote.serializers import PackageDetailsSerializer, QuoteSerializer, QuoteGetSerializer, PackageLooseSerializer,QuoteAddressDetailSerializer,QuotePackageDetailsSerializers
from quote.services.quote_transport_mode_service import QuoteTransportModeService
from utils.base_models import StatusBase
from utils.helpers import Diff
from utils.responses import get_paginated_data


class QuoteService:

    def __init__(self, data):
        self.data = data

    
    def get(self, company_id):

        quote_data = Quote.find_by(
            multi=True, join=False, status__ne=Quote.INACTIVE, company_id=company_id)

        quote_paginated_data = get_paginated_data(
            QuoteSerializer, quote_data, self.data)

        if quote_paginated_data:

            for quote in quote_paginated_data:
                shipment_terms = quote['shipment_terms'].split("_")

                quote['pickup_location'] = self.get_address(
                    quote, 'pickup', shipment_terms[0])

                quote['drop_location'] = self.get_address(
                    quote, 'drop', shipment_terms[2])

                quote['transport_mode'] = QuoteTransportModeService.get_transport_mode_by_quote_id(
                    quote_id=quote['id'])

            return quote_paginated_data

    def get_by_id(self, company_id, quote_id):

        quote_data_object={}
        quote_data = Quote.find_by(
            status__ne=Quote.INACTIVE, company_id=company_id, id=quote_id)

        quote_serializer = QuoteSerializer(quote_data, fields=['id','transport_modes','shipment_terms','expected_delivery_date','expected_arrival_date','is_origin_custom','is_submit_quote','is_destination_custom','is_personal_courier','is_commercial_courier','quote_no_counter','quote_no','quote_status'])

        quote_dict = quote_serializer.data

        shipment_terms = quote_dict['shipment_terms'].split("_")

        quote_dict['pickup_location'] = self.get_address(
            quote_dict, 'pickup', shipment_terms[0])

        quote_dict['drop_location'] = self.get_address(
            quote_dict, 'drop', shipment_terms[2])

        additional_details_serializer = QuoteSerializer(quote_data, fields=['po_number','no_of_suppliers','quote_deadline','switch_awb','switch_b_l','packaging','palletization','preference','depreference'])

        # package with adddress
        pickup_location_data = Address.objects.filter(entity_type ='quote', entity_id = quote_id, type = 'pickup').values_list('id', flat=True)
        pickup_location_ids = [i for i in pickup_location_data]

        cargo_data = []
        for ids in pickup_location_ids:
            cargo_package_data = {}
            
            # For loose cargo
            address_object = Address.find_by(id=ids, entity_id=quote_id, entity_type='quote', type='pickup')
            address_serializer = AddressSerializer(address_object)
            cargo_package_data.update({'pickup_location':address_serializer.data})
            package_d = PackageDetails.find_by(pickup_location_id=ids, quote_id=quote_id, container_id=None,is_fcl_container=False, multi=True)
            package_d_serializer = PackageLooseSerializer(package_d, many=True)
            cargo_package_data.update({'packages':package_d_serializer.data})

            # For container and container's package
            container_data = PackageDetails.find_by(pickup_location_id=ids, quote_id=quote_id, container_id=None, is_fcl_container=True, multi=True)
            container_data_serializer = PackageLooseSerializer(container_data, many=True)

            for fcl_package in container_data_serializer.data:
                fcl_package_data = PackageDetails.find_by(container_id=fcl_package['id'], quote_id=quote_id, multi=True)
                fcl_package_data_serializer = PackageLooseSerializer(fcl_package_data, many=True)
                fcl_package['packages'] = fcl_package_data_serializer.data
                for location in fcl_package_data_serializer.data:
                    pickup_id = location['pickup_location']
                    drop_id = location['drop_location']
                    location['pickup_location'] = self.get_address_by_id(pickup_id,'quote', quote_id, 'pickup')
                    location['drop_location'] = self.get_address_by_id(drop_id,'quote', quote_id, 'drop')

                cargo_package_data.update({'containers':container_data_serializer.data})
                
            cargo_data.append(cargo_package_data)
       
        quote_data_object.update({'basic_details':quote_dict,'cargo_details':cargo_data,'additional_details':additional_details_serializer.data})

        return quote_data_object

    def get_address_by_type(self, entity_type, entity_id, type):
        address = Address.find_by(status=StatusBase.ACTIVE,
                                  entity_type=entity_type,
                                  entity_id=entity_id,
                                  type=type,
                                  multi=True)
        address_serializer = AddressSerializer(address,
                                               many=True)
        return address_serializer.data

    def get_address(self, quote, type, shipment_term):

        # if shipment_term == 'door':
        return self.get_address_by_type('quote', quote['id'], type)

    def get_address_by_id(self, id, entity_type, entity_id, type):
        address_data = Address.objects.filter(id=id,
                                  status=StatusBase.ACTIVE,
                                  entity_type=entity_type,
                                  entity_id=entity_id,
                                  type=type).values('id','entity_type','entity_id','address1','address2','country_id','state_id','city_id','pincode','type')
        
        return address_data[0] if len(address_data) > 0 else {}





    