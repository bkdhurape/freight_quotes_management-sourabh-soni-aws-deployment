from address.models.address import Address
from company.services.company_service import CompanyService
from exceptions.cargo_details_exception import CargoDetailsException , CargoDetailsError
from exceptions.package_details_exception import PackageDetailsException, PackageDetailsError
from quote.models.package_details import PackageDetails
from quote.models.quote import Quote
from quote.models.quote_transport_mode import QuoteTransportMode
from quote.serializers import PackageDetailsSerializer
from utils.helpers import unique
from utils.total_weight_volume import get_package_total_weight_volume, get_total_weight_volume


class PackageDetailsService:

    def __init__(self, data):
        self.data = data

    def create(self, company_id, quote_id):

        Quote.find_by(multi=False, status__ne=Quote.INACTIVE, id=quote_id)
        self.data['quote'] = quote_id

        quote_data = Quote.find_by(
            multi=False, status__ne=Quote.INACTIVE, id=quote_id)

        transport_mode_type_data = list(QuoteTransportMode.find_by(
            multi=True, quote_id=quote_id, status=Quote.ACTIVE, id__in=self.data['transport_mode']).values_list('transport_mode', flat=True))

        drop_locations = list(Address.find_by(multi=True, status=Quote.ACTIVE, entity_id=self.data['quote'], type='drop').values_list('id', flat=True))

        # Get shipment terms
        quote_shipment_term = quote_data.shipment_terms

        shipment_term = quote_shipment_term.split("_")

        if ('Air' in transport_mode_type_data or 'LCL' in transport_mode_type_data or 'Air_courier' in transport_mode_type_data) or ('FCL' in transport_mode_type_data and self.data['is_fcl_container'] == False):
            # Calling address and port validation function
            self.address_and_port_exist_validation_for_quote(
                quote_id, shipment_term, transport_mode_type_data, drop_locations)

        # Temperature validation for Air
        self.temperature_validation_for_air(transport_mode_type_data)

        # Calling transport validation function
        self.transport_mode_exist_validation_for_quote(
            quote_id, self.data['transport_mode'])

        # calling required field validation function
        self.required_field_validations(quote_id, transport_mode_type_data)

        if 'package_detail_type' in self.data and self.data['package_detail_type'] == 'total':
            self.total_weight_volume_validations(self.data)
            data = get_package_total_weight_volume(self.data)
        else:
            data = self.data

        self.container_validation(data, shipment_term, drop_locations)

        if 'FCL' in transport_mode_type_data and self.data['is_fcl_container'] == True:
            data['commodity'] = []

        package_details_serializer = PackageDetailsSerializer(data=data)

        id = None
        if package_details_serializer.is_valid(raise_exception=True) and (( 'cargo_type' in data and data['cargo_type'] == 'container' and 'FCL' in transport_mode_type_data) or ('cargo_type' not in data and 'FCL' not in transport_mode_type_data)):
            id = (package_details_serializer.save()).id

            if 'FCL' in transport_mode_type_data and 'packages' in data:
                if data['is_fcl_container'] == True:
                    self.assign_packages_to_container(id, data['packages'])
                if data['is_fcl_container'] == False and data['cargo_type'] == 'container':
                    self.create_packages_and_loose_cargo_of_container(id, data['packages'], transport_mode_type_data, drop_locations)

        if 'loose_cargo' in data and data['loose_cargo'] and 'packages' in data['loose_cargo'] and data['loose_cargo']['packages']:
            self.create_packages_and_loose_cargo_of_container(id, data['loose_cargo']['packages'], transport_mode_type_data, drop_locations, 'loose_cargo')

        return True

    def container_validation(self, data, shipment_term, drop_locations):

        if 'container_subtype' in data and data['container_subtype']:
            if ((data['container_subtype'] == 'FR' or data['container_subtype'] == 'OT') and ('packages' not in data or not data['packages'])) or (len(drop_locations) > 1 and ('packages' not in data or not data['packages'])):
                raise PackageDetailsException(PackageDetailsError.PACKAGE_REQUIRED)

            if data['container_subtype'] == 'FR' and ('packages' in data and data['packages']):
                for package in data['packages']:
                    if package['package_detail_type'] == 'total':
                        raise PackageDetailsException(PackageDetailsError.PACKAGE_REQUIRED)

            if data['container_subtype'] == 'RF' and data['is_fcl_container'] == False:
                if 'temperature' not in data or not data['temperature']:
                    raise PackageDetailsException(PackageDetailsError.TEMPERATURE_REQUIRED)
                if 'temperature_unit' not in data or not data['temperature_unit']:
                    raise PackageDetailsException(PackageDetailsError.TEMPERATURE_UNIT_REQUIRED)
                if 'shipper_details' not in data or not data['shipper_details']:
                    raise PackageDetailsException(PackageDetailsError.SHIPPER_DETAILS_REQUIRED)

            if data['container_subtype'] == 'Tank':
                if 'consignee_details' not in data or not data['consignee_details']:
                    raise PackageDetailsException(PackageDetailsError.CONSIGNEE_DETAILS_REQUIRED)

            if data['container_subtype'] != 'RF':
                data['temperature'] = None
                data['temperature_unit'] = None

        # self.package_type_validations();
        if 'stuffing' in data and data['stuffing'] == 'factory' and data['is_fcl_container'] == False:
            if 'is_stackable' not in data:
                    raise PackageDetailsException(PackageDetailsError.STACKABLE_REQUIRED)
            if 'is_hazardous' not in data:
                    raise PackageDetailsException(PackageDetailsError.HAZARDOUS_REQUIRED)
            if 'commodity' not in data or not data['commodity']:
                    raise PackageDetailsException(PackageDetailsError.COMMODITY_REQUIRED)

        if (('stuffing' in data and data['stuffing'] == 'dock' and shipment_term[0] == 'door') or ('destuffing' in data and data['destuffing'] == 'dock' and shipment_term[2] == 'door')) and data['is_fcl_container'] == True:
            if ('packages' not in data or not data['packages']):
                raise PackageDetailsException(PackageDetailsError.PACKAGE_REQUIRED)

            for transport_mode in data['transport_mode']:
                package_details = PackageDetails.find_by(multi=True, id__in=data['packages'], quote_id = data['quote'], transport_mode=transport_mode)
                if not package_details:
                    raise PackageDetailsException(PackageDetailsError.INVALID_PACKAGE)


    def assign_packages_to_container(self, id, packages):

        for transport_mode in self.data['transport_mode']:
            package_details = PackageDetails.find_by(multi=True, id__in=packages, quote_id = self.data['quote'], transport_mode=transport_mode)
            if not package_details:
                raise PackageDetailsException(PackageDetailsError.INVALID_PACKAGE)

        package_details = PackageDetails.find_by(multi=True, id__in=self.data['packages'],temperature__isnull=False)
        package_details_temperatures = list(package_details.values_list('temperature', flat=True))
        if len(package_details_temperatures) > 0 and self.data['container_subtype'] != 'RF':
            raise PackageDetailsException(PackageDetailsError.INVALID_CONTAINER_TYPE)

        package_details = PackageDetails.find_by(multi=True, id__in=self.data['packages'],temperature__isnull=True)
        package_details_temperatures = list(package_details.values_list('temperature', flat=True))
        if len(package_details_temperatures) > 0 and self.data['container_subtype'] == 'RF':
            raise PackageDetailsException(PackageDetailsError.INVALID_PACKAGE_TYPE)


        package_details_pickup_location_ids = list(PackageDetails.find_by(multi=True, id__in=self.data['packages'], stuffing = 'factory').values_list('pickup_location', flat=True))
        unique_pickup_location_ids = unique(package_details_pickup_location_ids)

        if len(unique_pickup_location_ids) > 1:
            raise PackageDetailsException(PackageDetailsError.FACTORY_SAME_PICUKUP_PACKAGE_REQUIRED)

        package_details_pickup_location_ids = list(PackageDetails.find_by(multi=True, id__in=self.data['packages']).values_list('stuffing', flat=True))
        unique_pickup_location_ids = unique(package_details_pickup_location_ids)

        if len(unique_pickup_location_ids) > 1:
            raise PackageDetailsException(PackageDetailsError.DIFFERENT_CONTAINER_REQUIRED)

        unique_package_details_temperatures = unique(package_details_temperatures)
        if len(unique_package_details_temperatures) > 1:
            raise PackageDetailsException(PackageDetailsError.FOR_TEMPERATURE_DIFFERENT_CONTAINER_REQUIRED)


        for package in packages:
            package_details = PackageDetails.find_by(id=package)
            package_details_serializer = PackageDetailsSerializer(package_details)
            package_details_data = package_details_serializer.data

            package_details_data['container'] = id
            package_details_serializer = PackageDetailsSerializer(package_details, data=package_details_data)
            if package_details_serializer.is_valid(raise_exception=True):
                package_details_serializer.save()

    def create_packages_and_loose_cargo_of_container(self, id, packages, transport_mode_type_data, drop_locations, cargo_type = None):

        if (self.data['stuffing'] == 'dock' or self.data['destuffing'] == 'dock') and not packages and cargo_type is None:
            raise PackageDetailsException(PackageDetailsError.PACKAGE_REQUIRED)

        for package in packages:

            package['quote'] = self.data['quote']
            package['transport_mode'] = self.data['transport_mode']
            package['pickup_location'] = self.data['pickup_location']

            if len(drop_locations) == 1:
                if 'drop_location' not in self.data or self.data['drop_location'] is None:
                    raise PackageDetailsException(
                        PackageDetailsError.DROP_LOCATION_REQUIRED)

                package['drop_location'] = self.data['drop_location']

            if len(drop_locations) > 1 and self.data['cargo_type'] == 'loose_cargo':
                if 'drop_location' not in package or not package['drop_location']:
                    raise PackageDetailsException(
                        PackageDetailsError.DROP_LOCATION_REQUIRED)

                if 'drop_location' in package and package['drop_location']:
                    drop_data = Address.find_by(multi=True, status=Quote.ACTIVE,
                                                entity_id=self.data['quote'], type='drop', id=package['drop_location'])

                    if not drop_data:
                        raise PackageDetailsException(
                            PackageDetailsError.DROP_LOCATION_NOT_FOUND_FOR_QUOTE)

            self.package_type_validations(package, transport_mode_type_data)


            if self.data['stuffing'] == 'dock' and cargo_type is None:
                if 'is_stackable' not in package:
                        raise PackageDetailsException(PackageDetailsError.STACKABLE_REQUIRED)
                if 'is_hazardous' not in package:
                        raise PackageDetailsException(PackageDetailsError.HAZARDOUS_REQUIRED)
                if 'commodity' not in package or not package['commodity']:
                        raise PackageDetailsException(PackageDetailsError.COMMODITY_REQUIRED)
            else:
                if cargo_type is None:
                    package['is_stackable'] = self.data['is_stackable']
                    package['is_hazardous'] = self.data['is_hazardous']
                    package['commodity'] = self.data['commodity']

            if  cargo_type is None:
                package['stuffing'] = self.data['stuffing']
                package['destuffing'] = self.data['destuffing']
                package['container'] = id

            if package['package_detail_type'] == 'total':
                self.total_weight_volume_validations(package)
                data = get_package_total_weight_volume(package)
            else:
                data = package

            package_details_serializer = PackageDetailsSerializer(data=data)

            if package_details_serializer.is_valid(raise_exception=True):
                package_details_serializer.save()


    def update(self, company_id, quote_id, id):

        Quote.find_by(multi=False, status__ne=Quote.INACTIVE, id=quote_id)
        self.data['quote'] = quote_id

        quote_data = Quote.find_by(
            multi=False, status__ne=Quote.INACTIVE, id=quote_id)

        transport_mode_type_data = list(QuoteTransportMode.find_by(
            multi=True, quote_id=quote_id, status=Quote.ACTIVE, id__in=self.data['transport_mode']).values_list('transport_mode', flat=True))

        # Get shipment terms
        quote_shipment_term = quote_data.shipment_terms

        shipment_term = quote_shipment_term.split("_")

        # Calling address and port validation function
        self.address_and_port_exist_validation_for_quote(
            quote_id, shipment_term, transport_mode_type_data)


        # Calling transport validation function
        self.transport_mode_exist_validation_for_quote(
            quote_id, self.data['transport_mode'])

        # calling required field validation function
        self.required_field_validations(quote_id, transport_mode_type_data)


        if self.data['package_detail_type'] == 'total':
            self.total_weight_volume_validations(self.data)
            data = get_package_total_weight_volume(self.data)
        else:
            data = self.data

        self.container_validation(data)

        package_details = PackageDetails.find_by(id=id)
        package_details_serializer = PackageDetailsSerializer(package_details, data=self.data)
        if package_details_serializer.is_valid(raise_exception=True):
            package_details_serializer.save()

            if data['stuffing'] == 'dock' and 'FCL' in transport_mode_type_data:
                self.assign_packages_to_container(id, data['packages'])

        return True


    def total_weight_volume_validations(self, data):

        if 'total_weight' not in data or not data['total_weight']:
            raise CargoDetailsException(CargoDetailsError.TOTAL_WEIGHT_REQUIRED)

        if 'total_weight_unit' not in data or not data['total_weight_unit']:
            raise CargoDetailsException(CargoDetailsError.TOTAL_WEIGHT_UNIT_REQUIRED)

        if 'total_volume' not in data or not data['total_volume']:
            raise CargoDetailsException(CargoDetailsError.TOTAL_VOLUME_REQUIRED)

        if 'total_volume_unit' not in data or not data['total_volume_unit']:
            raise CargoDetailsException(CargoDetailsError.TOTAL_VOLUME_UNIT_REQUIRED)



    def required_field_validations(self, quote_id, transport_mode_type_data):

        # Calling fcl validations function
        self.fcl_validations(transport_mode_type_data)

        if 'Air' in transport_mode_type_data or 'LCL' in transport_mode_type_data or 'Air_courier' in transport_mode_type_data:
            # Calling package type validations function
            self.package_type_validations(self.data, transport_mode_type_data)

        # Calling air, lcl and air courier validations function
        self.air_lcl_and_air_courier_validations(transport_mode_type_data)


    def fcl_validations(self, transport_mode_type_data):

        pick_locations = list(Address.find_by(multi=True, status=Quote.ACTIVE, entity_id=self.data['quote'], type='pickup').values_list('id', flat=True))

        if 'container' in self.data:
            package_details = PackageDetails.find_by(multi=True, id=self.data['container'], quote=self.data['quote'])
            if not package_details:
                raise PackageDetailsException(
                    PackageDetailsError.INVALID_CONTAINER)

        if 'FCL' in transport_mode_type_data and 'container' not in self.data and ('cargo_type' in self.data and self.data['cargo_type'] == 'container'):
            if ('container_type' not in self.data or not self.data['container_type']) and ('type' not in self.data or not self.data['type']):
                raise PackageDetailsException(
                    PackageDetailsError.FOR_FCL_TYPE_OR_CONTAINER_TYPE_REQUIRED)

            if 'container_type' in self.data and self.data['container_type']:

                if 'container_subtype' not in self.data or not self.data['container_subtype']:
                    raise PackageDetailsException(
                        PackageDetailsError.CONTAINER_SUBTYPE_REQUIRED)

                if 'no_of_containers' not in self.data or not self.data['no_of_containers']:
                    raise PackageDetailsException(
                        PackageDetailsError.NO_OF_CONTAINERS_REQUIRED_FOR_FCL)
                if ('stuffing' not in self.data or not self.data['stuffing']) and (len(pick_locations) == 1 and self.data['is_fcl_container'] == False):
                    raise PackageDetailsException(
                        PackageDetailsError.STUFFING_REQUIRED_FOR_FCL)
                if 'destuffing' not in self.data or not self.data['destuffing']:
                    raise PackageDetailsException(
                        PackageDetailsError.DESTUFFING_REQUIRED_FOR_FCL)
                if ('weight' not in  self.data or not  self.data['weight']) and self.data['is_fcl_container'] == False:
                    raise PackageDetailsException(
                        PackageDetailsError.WEIGHT_REQUIRED)
                if ('weight_unit' not in  self.data or not  self.data['weight_unit']) and self.data['is_fcl_container'] == False:
                    raise PackageDetailsException(
                        PackageDetailsError.WEIGHT_UNIT_REQUIRED)

        drop_locations = list(Address.find_by(multi=True, status=Quote.ACTIVE, entity_id=self.data['quote'], type='drop').values_list('id', flat=True))
        if len(drop_locations) > 1 and self.data['cargo_type'] == 'container' and self.data['destuffing'] == 'factory' and self.data['is_fcl_container'] == True:
            raise PackageDetailsException(
                PackageDetailsError.ONLY_DOCK_DESTUFFING_REQUIRED)

        # if (('no_of_containers' in self.data and self.data['no_of_containers']) or ('stuffing'in self.data and self.data['stuffing']) or ('destuffing' in self.data and self.data['destuffing'])) and ('container_type' not in self.data or not self.data['container_type']):
        #     raise PackageDetailsException(
        #         PackageDetailsError.CONTAINERT_TYPE_REQUIRED_FOR_FCL)

    def package_type_validations(self, data, transport_mode_type_data):

        # pick_locations = list(Address.find_by(multi=True, status=Quote.ACTIVE, entity_id= data['quote'], type='pickup').values_list('id', flat=True))
        drop_locations = list(Address.find_by(multi=True, status=Quote.ACTIVE, entity_id=data['quote'], type='drop').values_list('id', flat=True))

        if 'type' in  data and  data['type'] or ('FCL' in transport_mode_type_data and 'container_subtype' in  data and ( data['container_subtype'] == 'FR' or  data['container_subtype'] == 'OT')):
            if 'quantity' not in  data or not  data['quantity']:
                raise PackageDetailsException(
                    PackageDetailsError.QUANTITY_REQUIRED)
            if 'length' not in  data or not  data['length']:
                raise PackageDetailsException(
                    PackageDetailsError.LENGTH_REQUIRED)
            if 'width' not in  data or not  data['width']:
                raise PackageDetailsException(
                    PackageDetailsError.WIDTH_REQUIRED)
            if 'height' not in  data or not  data['height']:
                raise PackageDetailsException(
                    PackageDetailsError.HEIGHT_REQUIRED)
            if 'dimension_unit' not in  data or not  data['dimension_unit']:
                raise PackageDetailsException(
                    PackageDetailsError.DIMENSION_UNIT_REQUIRED)
            if 'weight' not in  data or not  data['weight']:
                raise PackageDetailsException(
                    PackageDetailsError.WEIGHT_REQUIRED)
            if 'weight_unit' not in  data or not  data['weight_unit']:
                raise PackageDetailsException(
                    PackageDetailsError.WEIGHT_UNIT_REQUIRED)
            if ('stuffing' not in  data or not  data['stuffing']) and ('FCL' in transport_mode_type_data and data['cargo_type'] == 'loose_cargo' and data['is_fcl_container'] == False):
                raise PackageDetailsException(
                    PackageDetailsError.STUFFING_REQUIRED_FOR_FCL)
            if ('destuffing' not in  data or not  data['destuffing']) and ('FCL' in transport_mode_type_data and data['cargo_type'] == 'loose_cargo' and len(drop_locations) == 1):
                raise PackageDetailsException(
                    PackageDetailsError.DESTUFFING_REQUIRED_FOR_FCL)

        # if ('package_detail_type' in self.data and self.data['package_detail_type'] and self.data['package_detail_type'] == 'package') and  (('quantity' in self.data and self.data['quantity']) or ('length'in self.data and self.data['length']) or ('width' in self.data and self.data['width']) or ('height' in self.data and self.data['height']) or ('dimension_unit' in self.data and self.data['dimension_unit']) or ('weight' in self.data and self.data['weight']) or ('weight_unit' in self.data and self.data['weight_unit'])) and ('type' not in self.data or not self.data['type']):
        #     raise PackageDetailsException(PackageDetailsError.TYPE_REQUIRED)

    def air_lcl_and_air_courier_validations(self, transport_mode_type_data):

        if 'Air' in transport_mode_type_data or 'LCL' in transport_mode_type_data or 'Air_courier' in transport_mode_type_data:

            if ('package_detail_type' in self.data and self.data['package_detail_type'] and self.data['package_detail_type'] == 'package') and ('type' not in self.data or not self.data['type']):
                raise PackageDetailsException(PackageDetailsError.TYPE_REQUIRED)

            if 'FCL' not in transport_mode_type_data:
                self.data['container_type'] = None
                self.data['no_of_containers'] = None
                self.data['stuffing'] = None
                self.data['destuffing'] = None

    def temperature_validation_for_air(self,transport_mode_type_data):

        if 'Air' in transport_mode_type_data:
            if ('temperature' not in self.data or not self.data['temperature']):
                raise PackageDetailsException(PackageDetailsError.TEMPERATURE_REQUIRED)
            if (self.data['temperature'] and 'temperature_unit' not in self.data or not self.data['temperature_unit']):
                raise PackageDetailsException(PackageDetailsError.TEMPERATURE_UNIT_REQUIRED)
        else:
            if 'FCL' not in transport_mode_type_data:
                self.data['temperature'] = None
                self.data['temperature_unit'] = None

    def address_and_port_exist_validation_for_quote(self, quote_id, shipment_term, transport_mode_type_data, drop_locations):

        # if shipment_term[0] == 'door':
            if 'pickup_location' not in self.data or not self.data['pickup_location']:
                raise PackageDetailsException(
                    PackageDetailsError.PICKUP_LOCATION_REQUIRED)

            pickup_data = Address.find_by(multi=True, status=Quote.ACTIVE,
                                          entity_id=quote_id, type='pickup', id=self.data['pickup_location'])

            if not pickup_data:
                raise PackageDetailsException(
                    PackageDetailsError.PICKUP_LOCATION_NOT_FOUND_FOR_QUOTE)

            # self.source_airport_and_seaport_validation(
            #     transport_mode_type_data)

        # else:
        #     self.data['pickup_location'] = None

        # if (('Air' in transport_mode_type_data or 'LCL' in transport_mode_type_data or 'Air_courier' in transport_mode_type_data) and shipment_term[2] == 'door') or (shipment_term[2] == 'door' and 'FCL' in transport_mode_type_data and (self.data['cargo_type'] == 'container' or (self.data['cargo_type'] == 'loose_cargo' and len(drop_locations) == 1)) and self.data['is_fcl_container'] == False):
            if 'drop_location' not in self.data or not self.data['drop_location']:
                raise PackageDetailsException(
                    PackageDetailsError.DROP_LOCATION_REQUIRED)

            drop_data = Address.find_by(multi=True, status=Quote.ACTIVE,
                                        entity_id=quote_id, type='drop', id=self.data['drop_location'])

            if not drop_data:
                raise PackageDetailsException(
                    PackageDetailsError.DROP_LOCATION_NOT_FOUND_FOR_QUOTE)

            # self.destination_airport_and_seaport_validation(
            #     transport_mode_type_data)
        # else:
        #     self.data['drop_location'] = None

        # Calling shipment term port validation function
        # if ('package_detail_type' in self.data and self.data['package_detail_type'] and self.data['package_detail_type'] == 'package'):
        #     self.shipment_term_port_validation(
        #         shipment_term, transport_mode_type_data)


    # def shipment_term_port_validation(self, shipment_term, transport_mode_type_data):
    #
    #     if shipment_term[0] == 'port':
    #         if ('pickup_air_port' not in self.data or not self.data['pickup_air_port']) and 'Air' in transport_mode_type_data:
    #             raise PackageDetailsException(
    #                 PackageDetailsError.PICKUP_AIR_PORT_REQUIRED)
    #
    #         if ('pickup_sea_port' not in self.data or not self.data['pickup_sea_port']) and 'FCL' in transport_mode_type_data:
    #             raise PackageDetailsException(
    #                 PackageDetailsError.PICKUP_SEA_PORT_REQUIRED)
    #
    #         self.source_airport_and_seaport_validation(
    #             transport_mode_type_data)
    #
    #     if shipment_term[2] == 'port':
    #         if ('drop_air_port' not in self.data or not self.data['drop_air_port']) and 'Air' in transport_mode_type_data:
    #             raise PackageDetailsException(
    #                 PackageDetailsError.DROP_AIR_PORT_REQUIRED)
    #
    #         if ('drop_sea_port' not in self.data or not self.data['drop_sea_port']) and 'FCL' in transport_mode_type_data:
    #             raise PackageDetailsException(
    #                 PackageDetailsError.DROP_SEA_PORT_REQUIRED)
    #
    #         self.destination_airport_and_seaport_validation(
    #             transport_mode_type_data)
    #


    # def source_airport_and_seaport_validation(self, transport_mode_type_data):
    #
    #     if ('pickup_air_port' in self.data and self.data['pickup_air_port']) and ('Air' in transport_mode_type_data or 'Air_courier' in transport_mode_type_data):
    #         self.check_port_exist(
    #             'pickup_air_port', PackageDetailsError.PICKUP_AIR_PORT_INVALID)
    #
    #     if ('pickup_sea_port' in self.data and self.data['pickup_sea_port']) and ('FCL' in transport_mode_type_data or 'LCL' in transport_mode_type_data):
    #         self.check_port_exist(
    #             'pickup_sea_port', PackageDetailsError.PICKUP_SEA_PORT_INVALID)
    #
    #     if ('Air' in transport_mode_type_data or 'Air_courier' in transport_mode_type_data) and ('FCL' not in transport_mode_type_data and 'LCL' not in transport_mode_type_data):
    #         self.data['pickup_sea_port'] = []
    #
    #     if ('FCL' in transport_mode_type_data or 'LCL' in transport_mode_type_data) and ('Air' not in transport_mode_type_data and 'Air_courier' not in transport_mode_type_data):
    #         self.data['pickup_air_port'] = []
    #


    # def destination_airport_and_seaport_validation(self, transport_mode_type_data):
    #
    #     if ('drop_air_port' in self.data and self.data['drop_air_port']) and ('Air' in transport_mode_type_data or 'Air_courier' in transport_mode_type_data):
    #         self.check_port_exist(
    #             'drop_air_port', PackageDetailsError.DROP_AIR_PORT_INVALID)
    #
    #     if ('drop_sea_port' in self.data and self.data['drop_sea_port']) and ('FCL' in transport_mode_type_data or 'LCL' in transport_mode_type_data):
    #         self.check_port_exist(
    #             'drop_sea_port', PackageDetailsError.DROP_SEA_PORT_INVALID)
    #
    #     if ('Air' in transport_mode_type_data or 'Air_courier' in transport_mode_type_data) and ('FCL' not in transport_mode_type_data and 'LCL' not in transport_mode_type_data):
    #         self.data['drop_sea_port'] = []
    #
    #     if ('FCL' in transport_mode_type_data or 'LCL' in transport_mode_type_data) and ('Air' not in transport_mode_type_data and 'Air_courier' not in transport_mode_type_data):
    #         self.data['drop_air_port'] = []
    #


    # def check_port_exist(self, key, error):
    #     condition = {}
    #     for data in self.data[key]:
    #         condition = {key: data}
    #         port_data = Quote.find_by(
    #             multi=True, id=self.data['quote'], status__ne=Quote.INACTIVE, **condition)
    #
    #         if not port_data:
    #             raise PackageDetailsException(error)
    #


    def transport_mode_exist_validation_for_quote(self, quote_id, transport_mode_id):

        for transport_id in transport_mode_id:
            transport_mode_data = QuoteTransportMode.find_by(
                multi=True, status=Quote.ACTIVE, quote_id=quote_id, id=transport_id)
            if not transport_mode_data:
                raise PackageDetailsException(
                    PackageDetailsError.TRANSPORT_MODE_NOT_FOUND_FOR_QUOTE)



    def get(self, company_id, quote_id):

        Quote.find_by(status__ne=Quote.INACTIVE, id=quote_id)

        package_data = {}

        package_dict = {}
        package_container = []

        transport_mode_type_data = list(QuoteTransportMode.find_by(
            multi=True, quote_id=quote_id, status=Quote.ACTIVE).values_list('transport_mode', flat=True))

        if 'Air' in transport_mode_type_data or 'Air_courier' in transport_mode_type_data or 'LCL' in transport_mode_type_data:
            package_details_data = PackageDetails.find_by(
                multi=True, status=Quote.ACTIVE, quote_id=quote_id)

            package_details_serializer = PackageDetailsSerializer(
                package_details_data, many=True)

            package_data = package_details_serializer.data

        else:

            condition = {}
            pickup_locations = list(Address.find_by(multi=True, status=Quote.ACTIVE, entity_id=quote_id, type='pickup').values_list('id', flat=True))

            for pickup_location in pickup_locations:

                condition = { 'pickup_location': pickup_location, 'quote_id': quote_id, 'cargo_type': 'container', 'container__isnull': True }
                package_data[str(pickup_location)+'_containers'] = self.get_package_data(condition)

                condition.update({'cargo_type': 'loose_cargo'})
                package_data[str(pickup_location)+'_loose_cargo'] = self.get_package_data(condition)

            for pickup_location in pickup_locations:

                containers = package_data[str(pickup_location)+'_containers']

                for container in containers:
                    condition = { 'pickup_location': pickup_location, 'quote_id': quote_id, 'cargo_type': 'container', 'container': container['id'] }
                    packages = self.get_package_data(condition)
                    container['packages'] = packages
                    container['total_weight_volume'] = get_total_weight_volume(packages)

                package_dict = {
                    "is_fcl_container": False,
                    "pickup_location": pickup_location,
                    "containers": containers,
                    "loose_cargo": package_data[str(pickup_location)+'_loose_cargo'],
                }
                package_container.append(package_dict)


            condition = { 'quote_id': quote_id, 'cargo_type': 'container', 'container__isnull': True, 'is_fcl_container': True }
            container_tab_data = self.get_package_data(condition)

            if len(container_tab_data) > 0:

                for container_tab in container_tab_data:
                    condition = { 'quote_id': quote_id, 'cargo_type': 'loose_cargo', 'container': container_tab['id'] }
                    packages = self.get_package_data(condition)
                    container_tab['packages'] = packages
                    container_tab['total_weight_volume'] = get_total_weight_volume(packages)

                package_dict = {"is_fcl_container": True, "containers": container_tab_data}
                package_container.append(package_dict)


            package_data = package_container

        return package_data


    def get_package_data(self, condition):
        package_details = PackageDetails.find_by(multi=True, **condition)
        package_details_serializer = PackageDetailsSerializer(package_details, many=True)

        return package_details_serializer.data


    def get_by_id(self, company_id, quote_id, package_details_id):

        Quote.find_by(status__ne=Quote.INACTIVE,
                      company_id=company_id, id=quote_id)

        package_details_data = PackageDetails.find_by(
            status=Quote.ACTIVE, quote_id=quote_id, id=package_details_id)

        package_details_serializer = PackageDetailsSerializer(
            package_details_data)

        return package_details_serializer.data
