# from datetime import date
from address.models.address import Address
from company.models.company import Company
from datetime import timedelta
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from utils.base_models import StatusBase
from exceptions.cargo_details_exception import CargoDetailsException, CargoDetailsError
from exceptions.package_details_exception import PackageDetailsException, PackageDetailsError
from exceptions.quote_exceptions import QuoteException, QuoteError
from exceptions.quote_transport_mode_exception import QuoteTransportModeException, QuoteTransportModeError
from freight.freight_manager import FreightManager
from port.models.port import Port
from django.db.models import Q
from utils.helpers import Diff
import datetime
import fiscalyear
import re 


class QuoteManager(FreightManager):
    """Quote Data manager used for doing db operation."""

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise QuoteException(QuoteError.QUOTE_NOT_FOUND)


class QuoteTransportModeManager(FreightManager):
    """Quote transport mode Data manager used for doing db operation."""

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise QuoteTransportModeException(QuoteTransportModeError.QUOTE_TRANSPORT_MODE_NOT_FOUND)


class PackageDetailsManager(FreightManager):
    """Package details Data manager used for doing db operation."""

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise PackageDetailsException(PackageDetailsError.PACKAGE_DETAILS_NOT_FOUND)


class CargoDetailsManager(FreightManager):
    """Cargo Details Data manager used for doing db operation."""

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise CargoDetailsException(CargoDetailsError.QUOTE_TOTAL_WEIGHT_VOLUME_NOT_FOUND)


class QuoteOrderReadyManager(FreightManager):
    """Quote Order Ready Data manager used for doing db operation."""

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise CargoDetailsException(CargoDetailsError.QUOTE_ORDER_READY_NOT_FOUND)


class QuoteServiceManager(models.Manager):

    def _create_quote_address(self, quote_id, basic_details, address_type):
        """
        Create quote address by address type
        :param quote_id:
        :type quote_id:
        :param basic_details:
        :type basic_details:
        :param address_type:
        :type address_type:
        :return:
        :rtype:
        """
        locations = basic_details['pickup_location'] if address_type == 'pickup' else basic_details['drop_location']
        for address in locations:
            address_obj = Address.objects.create(entity_type='quote',
                                                 entity_id=quote_id,
                                                 address1=address.get('address1'),
                                                 country=address['country'],
                                                 type=address_type
                                                 )
            address_obj.save()

            if 'Air' in basic_details['transport_mode'] or 'Air_courier' in basic_details['transport_mode']:
                airport_ids = address['airport_ids']
                address_obj.airport_ids.add(*airport_ids)

            if 'LCL' in basic_details['transport_mode'] or 'FCL' in basic_details['transport_mode']:
                seaport_ids = address['seaport_ids']
                address_obj.seaport_ids.add(*seaport_ids)

    def _get_quote_location(self, quote_id, location, address_type):
        address = Address.objects.filter(entity_id=quote_id, entity_type='quote', address1=location.get('address1'),
                                         country=location.get('country'), type=address_type).first()
        return address

    def _create_package_details(self, quote_id, transport_mode_ids, cargo_details):
        """
        Create quote package details
        :param quote_id:
        :type quote_id:
        :param transport_mode_ids:
        :type transport_mode_ids:
        :param cargo_details:
        :type cargo_details:
        :return:
        :rtype:
        """

        package_detail_model = apps.get_model('quote', 'PackageDetails')

        for cargo_detail in cargo_details:
            package_detail_data = {'quote_id': quote_id,
                                   'pickup_location': self._get_quote_location(quote_id=quote_id,
                                                                               location=cargo_detail[
                                                                                   'pickup_location'],
                                                                               address_type='pickup'),
                                   'drop_location': self._get_quote_location(quote_id=quote_id,
                                                                             location=cargo_detail[
                                                                                 'drop_location'],
                                                                             address_type='drop'),
                                    'is_order_ready':cargo_detail.get('is_order_ready'),
                                    'order_ready_date':cargo_detail.get('order_ready_date'),
                                    'invoice_value':cargo_detail.get('invoice_value'),
                                    'invoice_value_currency':cargo_detail.get('invoice_value_currency'),
                                    'handover_date':cargo_detail.get('handover_date')
                                   }
            
            if cargo_detail['packages']:
                for package in cargo_detail['packages']:
                    package_detail_data.update({'type': package.get('type'),
                                                'quantity': package.get('quantity'),
                                                'length': package.get('length'),
                                                'width': package.get('width'),
                                                'height': package.get('height'),
                                                'dimension_unit': package.get('dimension_unit'),
                                                'weight': package.get('weight'),
                                                'weight_unit': package.get('weight_unit'),
                                                'is_hazardous': package.get('is_hazardous'),
                                                'is_stackable': package.get('is_stackable'),
                                                'package_detail_type': package.get('package_detail_type'),
                                                'total_weight':package.get('total_weight'),
                                                'total_weight_unit':package.get('total_weight_unit'),
                                                'total_volume':package.get('total_volume'),
                                                'total_volume_unit':package.get('total_volume_unit'),
                                                'consignee_details':package.get('consignee_details'),
                                                'shipper_details':package.get('shipper_details')
                                                })

                    package_detail = package_detail_model(**package_detail_data)
                    package_detail.save()

                    # Set transport modes for package details
                    package_detail.transport_mode.add(*transport_mode_ids)

                    # Set commodities for package details
                    if 'commodity' in package:
                        cargo_commodities = package.get('commodity')
                        package_detail.commodity.add(*cargo_commodities)

    def _create_fcl_package_details(self, quote_id, transport_mode_ids, cargo_details):
        """
        Create FCL package details
        :param quote_id:
        :type quote_id:
        :param transport_mode_ids:
        :type transport_mode_ids:
        :param cargo_details:
        :type cargo_details:
        :return:
        :rtype:
        """
        package_detail_model = apps.get_model('quote', 'PackageDetails')
        container_detail_data = {}
        package_detail_data = {}

        for cargo_detail in cargo_details:
            if not cargo_detail['is_fcl_container'] or cargo_detail['is_fcl_container']:
                package_detail_data = {'quote_id': quote_id,
                                       'pickup_location': self._get_quote_location(quote_id=quote_id,
                                                                                   location=cargo_detail[
                                                                                       'pickup_location'],
                                                                                   address_type='pickup'),
                                       'drop_location': self._get_quote_location(quote_id=quote_id,
                                                                                 location=cargo_detail[
                                                                                     'drop_location'],
                                                                                 address_type='drop')
                                       }
                container_detail_data = package_detail_data.copy()
                container_package_data = package_detail_data.copy()

            if cargo_detail['packages'] and not cargo_detail['is_fcl_container']:
                for package in cargo_detail['packages']:
                    package_detail_data.update({'type': package.get('type'),
                                                'quantity': package.get('quantity'),
                                                'length': package.get('length'),
                                                'width': package.get('width'),
                                                'height': package.get('height'),
                                                'dimension_unit': package.get('dimension_unit'),
                                                'weight': package.get('weight'),
                                                'weight_unit': package.get('weight_unit'),
                                                'is_hazardous': package.get('is_hazardous'),
                                                'is_stackable': package.get('is_stackable'),
                                                'package_detail_type': package.get('package_detail_type'),
                                                'total_weight':package.get('total_weight'),
                                                'total_weight_unit':package.get('total_weight_unit'),
                                                'total_volume':package.get('total_volume'),
                                                'total_volume_unit':package.get('total_volume_unit'),
                                                'consignee_details':package.get('consignee_details'),
                                                'shipper_details':package.get('shipper_details')
                                                })

                    package_detail = package_detail_model(**package_detail_data)
                    package_detail.save()

                    # Set transport modes for package details
                    package_detail.transport_mode.add(*transport_mode_ids)

                    # Set commodities for package details
                    if 'commodity' in package:
                        cargo_commodities = package.get('commodity')
                        package_detail.commodity.add(*cargo_commodities)

            if cargo_detail['containers']:
                for container in cargo_detail['containers']:
                    container_detail_data.update({'stuffing': container['stuffing'],
                                                  'destuffing': container['destuffing'],
                                                  'is_hazardous': container['is_hazardous'],
                                                  'is_stackable': container['is_stackable'],
                                                  'weight': container['weight'],
                                                  'weight_unit': container['weight_unit'],
                                                  'container_type': container['container_type'],
                                                  'container_subtype': container['container_subtype'],
                                                'consignee_details': container.get('consignee_details'),
                                                'shipper_details': container.get('shipper_details')
                                                  })

                    if container['container_subtype'] == 'RF' and container['cargo_type'] == 'container':

                        if container['stuffing'] == 'factory':
                            container_detail_data.update({'temperature': container['temperature'],
                                                          'temperature_unit': container['temperature_unit']})

                    if container['is_fcl_container']:
                        container_detail_data.update({'is_fcl_container': True})

                    container_detail = package_detail_model(**container_detail_data)
                    container_detail.save()

                    # Set transport modes for package details
                    container_detail.transport_mode.add(*transport_mode_ids)

                    if 'commodity' in container and container['stuffing'] == 'factory':
                        container_commodities = container['commodity']
                        container_detail.commodity.add(*container_commodities)

                    container_id = container_detail.id

                    container_package_data.update({'container_id': container_id})

                    if container['packages']:
                        for container_package in container['packages']:
                            if cargo_detail['is_fcl_container']:
                                container_package_data.update({'quote_id': quote_id,
                                                               'pickup_location': self._get_quote_location(
                                                                   quote_id=quote_id,
                                                                   location=
                                                                   container_package[
                                                                       'pickup_location'],
                                                                   address_type='pickup'),
                                                               'drop_location': self._get_quote_location(
                                                                   quote_id=quote_id,
                                                                   location=
                                                                   container_package[
                                                                       'drop_location'],
                                                                   address_type='drop')
                                                               if 'drop_location' in container_package else None
                                                               })

                            container_package_data.update({'type': container_package['type'],
                                                           'quantity': container_package['quantity'],
                                                           'length': container_package['length'],
                                                           'width': container_package['width'],
                                                           'height': container_package['height'],
                                                           'dimension_unit': container_package['dimension_unit'],
                                                           'weight': container_package['weight'],
                                                           'weight_unit': container_package['weight_unit'],
                                                            'consignee_details': container_package.get('consignee_details'),
                                                            'shipper_details': container_package.get('shipper_details')
                                                           })

                            if container['stuffing'] == 'dock':
                                container_package_data.update({'is_hazardous': container_package['is_hazardous'],
                                                               'is_stackable': container_package['is_stackable'],
                                                               })

                            container_package_detail = package_detail_model(**container_package_data)
                            container_package_detail.save()

                            if container['stuffing'] == 'dock':
                                # Set transport modes for package details
                                container_package_detail.transport_mode.add(*transport_mode_ids)

                                if 'commodity' in container:
                                    container_package_commodities = container_package['commodity']
                                    container_package_detail.commodity.add(*container_package_commodities)

    def _create_additional_details(self, quote, additional_details):
        """
        Create additional details of quote
        :param quote_id:
        :type quote_id:
        :param additional_details:
        :type additional_details:
        :return:
        :rtype:
        """

        additional_details_data = {'po_number': additional_details['po_number'],
                                   'no_of_suppliers': additional_details['no_of_suppliers'],
                                   'quote_deadline': additional_details['quote_deadline'],
                                   'switch_awb': additional_details['switch_awb'],
                                   'switch_b_l': additional_details['switch_b_l'],
                                   'packaging': additional_details['packaging'],
                                   'palletization': additional_details['palletization']}

        self.model.objects.filter(id=quote.id).update(**additional_details_data)

        # If preference set, then selected airlines will be preferred for the quote
        if 'preference' in additional_details and additional_details['preference']:
            preference = additional_details['preference']
            quote.preference.add(*preference)

        # If de-preference set, then selected airlines will not be preferred for the quote
        if 'depreference' in additional_details and additional_details['depreference']:
            depreference = additional_details['depreference']
            quote.depreference.add(*depreference)

    def _update_additional_details(self, quote_id, additional_details):
        """
        Update additional details of quote
        :param quote_id:
        :type quote_id:
        :param additional_details:
        :type additional_details:
        :return:
        :rtype:
        """

        additional_details_data = {'po_number': additional_details['po_number'],
                                   'no_of_suppliers': additional_details['no_of_suppliers'],
                                   'quote_deadline': additional_details['quote_deadline'],
                                   'switch_awb': additional_details['switch_awb'],
                                   'switch_b_l': additional_details['switch_b_l'],
                                   'packaging': additional_details['packaging'],
                                   'palletization': additional_details['palletization'] 
                                   }

        quote = self.model.objects.get(id=quote_id)
        self.model.objects.filter(id=quote.id).update(**additional_details_data) 

        # While updating, if user changes to preference from depreference then preference data shouldget deleted.
        if additional_details.get('preference'):
            depreference_data = self.model.objects.filter(id=quote_id).values_list('depreference', flat=True)
            if depreference_data:
                quote.depreference.remove(*depreference_data)

        if additional_details.get('depreference'):
            preference_data = self.model.objects.filter(id=quote_id).values_list('preference', flat=True)
            if preference_data:
                quote.preference.remove(*preference_data)

        # Add new value if not in database and delete which is removed from request for preference data
        if additional_details.get('preference'):
            preference_db_data = list(self.model.objects.filter(id=quote_id).values_list('preference', flat=True))
            request_data = [i.id for i in additional_details.get('preference')]
            deleted_preference = Diff(preference_db_data, request_data)
            quote.preference.remove(*deleted_preference)
            quote.preference.add(*additional_details['preference'])   

        # Add new value if not in database and delete which is removed from request for depreference data
        if additional_details.get('depreference'):
            depreference_db_data = list(self.model.objects.filter(id=quote_id).values_list('depreference', flat=True))
            request_data = [i.id for i in additional_details.get('depreference')]
            deleted_depreference = Diff(depreference_db_data, request_data)
            quote.depreference.remove(*deleted_depreference)
            quote.depreference.add(*additional_details['depreference']) 


    def _update_quote_address(self, quote_id, basic_details, address_type):
        """
        Create quote address by address type
        :param quote_id:
        :type quote_id:
        :param basic_details:
        :type basic_details:
        :param address_type:
        :type address_type:
        :return:
        :rtype:
        """        

        locations = basic_details['pickup_location'] if address_type == 'pickup' else basic_details['drop_location']
        request_address_ids = [i.get('id') for i in locations]
        db_address_data = Address.objects.filter(entity_id=quote_id, type=address_type).values_list('id',flat=True)
        db_address_ids = [i for i in db_address_data]

        deleted_address = Diff(db_address_ids, request_address_ids)
        
        for d_data in deleted_address:            
            d_object = Address.objects.get(id=d_data, entity_id=quote_id,type=address_type)
            if address_type == 'pickup':
                # Package related to this pickup location should also get deleted
                pacakge_pickup_data = apps.get_model('quote','PackageDetails').objects.filter(quote=quote_id, pickup_location=d_data)
                pacakge_pickup_data.delete()
            if address_type == 'drop':
                # Package related to this drop location should also get deleted    
                pacakge_drop_data = apps.get_model('quote','PackageDetails').objects.filter(quote=quote_id, drop_location=d_data)
                pacakge_drop_data.delete()
            d_object.delete()

        for address in locations: 
            if 'id' in address:      
                address_update_data = Address.objects.filter(id=address['id'], entity_id=quote_id).update(
                                                    entity_type='quote',
                                                    entity_id=quote_id,
                                                    address1=address.get('address1'),
                                                    country=address['country'],
                                                    type=address_type)        
                
                # address_obj.save()
                address_obj = Address.objects.get(id=address['id'])

                if 'Air' in basic_details['transport_mode'] or 'Air_courier' in basic_details['transport_mode']:
                    airport_ids_db_data = list(Address.objects.filter(id=address['id'], entity_id=quote_id).values_list('airport_ids', flat=True))
                    request_data = [i.id for i in address['airport_ids']]
                    deleted_airport_ids = Diff(airport_ids_db_data, request_data)
                    address_obj.airport_ids.remove(*deleted_airport_ids)
                    address_obj.airport_ids.add(*address['airport_ids'])

                if 'LCL' in basic_details['transport_mode'] or 'FCL' in basic_details['transport_mode']:
                    seaport_ids_db_data = list(Address.objects.filter(id=address['id'], entity_id=quote_id).values_list('seaport_ids', flat=True))
                    request_data = [i.id for i in address['seaport_ids']]
                    deleted_seaport_ids = Diff(seaport_ids_db_data, request_data)
                    address_obj.seaport_ids.remove(*deleted_seaport_ids)
                    address_obj.seaport_ids.add(*address['seaport_ids']) 

            # locations = basic_details['pickup_location'] if address_type == 'pickup' else basic_details['drop_location']
            else:                
                address_obj = Address.objects.create(entity_type='quote',
                                                    entity_id=quote_id,
                                                    address1=address.get('address1'),
                                                    country=address['country'],
                                                    type=address_type
                                                    )
                address_obj.save()

                if 'Air' in basic_details['transport_mode'] or 'Air_courier' in basic_details['transport_mode']:
                    airport_ids = address['airport_ids']
                    address_obj.airport_ids.add(*airport_ids)

                if 'LCL' in basic_details['transport_mode'] or 'FCL' in basic_details['transport_mode']:
                    seaport_ids = address['seaport_ids']
                    address_obj.seaport_ids.add(*seaport_ids)

    def _update_package_details(self, quote_id, transport_mode_id_data, cargo_details):
        """
        Update quote package details
        :param quote_id:
        :type quote_id:
        :param transport_mode_ids:
        :type transport_mode_ids:
        :param cargo_details:
        :type cargo_details:
        :return:
        :rtype:
        """

        package_detail_model = apps.get_model('quote', 'PackageDetails')

        # Delete packages from databse which is removed from request
        request_package_id = []
        for cargo_data in cargo_details:
            for package_id in cargo_data['packages']:
                request_package_id.append(package_id.get('id'))
        
        db_package_data = package_detail_model.objects.filter(quote_id=quote_id, is_fcl_container=False, container_id=None).values_list('id', flat=True)
        db_package_ids = [i for i in db_package_data]
        
        deleted_package = Diff(db_package_ids, request_package_id)       

        for package_data in deleted_package:
            to_delete_package = package_detail_model.objects.filter(id=package_data, quote_id=quote_id)
            to_delete_package.delete()
        
        # Create and update package details
        for cargo_detail in cargo_details:
            package_detail_data = {'quote_id': quote_id,
                                   'pickup_location': self._get_quote_location(quote_id=quote_id,
                                                                               location=cargo_detail[
                                                                                   'pickup_location'],
                                                                               address_type='pickup'),
                                   'drop_location': self._get_quote_location(quote_id=quote_id,
                                                                             location=cargo_detail[
                                                                                 'drop_location'],
                                                                             address_type='drop'),
                                    'is_order_ready':cargo_detail.get('is_order_ready'),
                                    'order_ready_date':cargo_detail.get('order_ready_date'),
                                    'invoice_value':cargo_detail.get('invoice_value'),
                                    'invoice_value_currency':cargo_detail.get('invoice_value_currency'),
                                    'handover_date':cargo_detail.get('handover_date')
                                   }

            if cargo_detail['packages']:

                for package in cargo_detail['packages']:
                    package_detail_data.update({'type': package.get('type'),
                                                'quantity': package.get('quantity'),
                                                'length': package.get('length'),
                                                'width': package.get('width'),
                                                'height': package.get('height'),
                                                'dimension_unit': package.get('dimension_unit'),
                                                'weight': package.get('weight'),
                                                'weight_unit': package.get('weight_unit'),
                                                'is_hazardous': package.get('is_hazardous'),
                                                'is_stackable': package.get('is_stackable'),
                                                'package_detail_type': package.get('package_detail_type'),
                                                'total_weight':package.get('total_weight'),
                                                'total_weight_unit':package.get('total_weight_unit'),
                                                'total_volume':package.get('total_volume'),
                                                'total_volume_unit':package.get('total_volume_unit'),
                                                'consignee_details':package.get('consignee_details'),
                                                'shipper_details':package.get('shipper_details')
                                                })
                    if package.get('id'):
                        package_data = package_detail_model.objects.filter(quote_id=quote_id).values_list('id',flat=True)
                        if package_data:
                            package_object = package_detail_model.objects.get(id=package.get('id'), quote_id=quote_id)
                            package_detail_model.objects.filter(id=package.get('id')).update(**package_detail_data)
                            
                            # Set transport modes for package details
                            package_object.transport_mode.add(*transport_mode_id_data)

                            # Set commodities for package details
                            if 'commodity' in package:
                                request_commodity_ids = [i.id for i in package['commodity']]
                                db_commodity_ids = list(package_detail_model.objects.filter(id=package['id'], quote_id=quote_id).values_list('commodity', flat=True))
                                deleted_commodity_ids = Diff(db_commodity_ids, request_commodity_ids)
                                package_object.commodity.remove(*deleted_commodity_ids)
                                package_object.commodity.add(*package['commodity'])
                            
                    else:
                        package_detail = package_detail_model(**package_detail_data)
                        package_detail.save()

                        # Set transport modes for package details
                        package_detail.transport_mode.add(*transport_mode_id_data)

                        # Set commodities for package details
                        if 'commodity' in package:
                            cargo_commodities = package.get('commodity')
                            package_detail.commodity.add(*cargo_commodities)


    def _update_fcl_package_details(self, quote_id, transport_mode_id_data, cargo_details):
        """
        Create FCL package details
        :param quote_id:
        :type quote_id:
        :param transport_mode_id_data:
        :type transport_mode_id_data:
        :param cargo_details:
        :type cargo_details:
        :return:
        :rtype:
        """
        package_detail_model = apps.get_model('quote', 'PackageDetails')
        container_detail_data = {}
        package_detail_data = {}

        # Delete loose cargo for FCL while editing
        request_loose_cargo_id = []
        for cargo_data in cargo_details:
            for package_id in cargo_data['packages']:
                request_loose_cargo_id.append(package_id.get('id'))
        
        db_loose_package = package_detail_model.objects.filter(quote_id=quote_id, container_id=None, is_fcl_container=False).values_list('id', flat=True)
        db_loose_package_ids = [i for i in db_loose_package]
        
        deleted_loose_package = Diff(db_loose_package_ids, request_loose_cargo_id)       

        for loose_cargo_data in deleted_loose_package:
            to_delete_loose_cargo = package_detail_model.objects.filter(id=loose_cargo_data, quote_id=quote_id)
            to_delete_loose_cargo.delete()

        # Delete container details with its package
        container_request_id = []
        for cargo_data in cargo_details:
            for container_id in cargo_data['containers']:
                container_request_id.append(container_id.get('id'))
        
        db_package = package_detail_model.objects.filter(quote_id=quote_id, is_fcl_container=True).values_list('id', flat=True)
        db_package_ids = [i for i in db_package]
        
        deleted_package = Diff(db_package_ids, container_request_id) 

        for package_data in deleted_package:
            to_delete_container = package_detail_model.objects.filter(id=package_data, quote_id=quote_id)
            to_delete_cotainer_package = package_detail_model.objects.filter(container_id=package_data, quote_id=quote_id)
            to_delete_cotainer_package.delete()
            to_delete_container.delete()


        for cargo_detail in cargo_details:
            if not cargo_detail['is_fcl_container']:
                package_detail_data = {'quote_id': quote_id,
                                       'pickup_location': self._get_quote_location(quote_id=quote_id,
                                                                                   location=cargo_detail[
                                                                                       'pickup_location'],
                                                                                   address_type='pickup'),
                                       'drop_location': self._get_quote_location(quote_id=quote_id,
                                                                                 location=cargo_detail[
                                                                                     'drop_location'],
                                                                                 address_type='drop')
                                       }
                container_detail_data = package_detail_data.copy()
                container_package_data = package_detail_data.copy()

            if cargo_detail['packages'] and not cargo_detail['is_fcl_container']:
                for package in cargo_detail['packages']:
                    package_detail_data.update({'type': package.get('type'),
                                                'quantity': package.get('quantity'),
                                                'length': package.get('length'),
                                                'width': package.get('width'),
                                                'height': package.get('height'),
                                                'dimension_unit': package.get('dimension_unit'),
                                                'weight': package.get('weight'),
                                                'weight_unit': package.get('weight_unit'),
                                                'is_hazardous': package.get('is_hazardous'),
                                                'is_stackable': package.get('is_stackable'),
                                                'package_detail_type': package.get('package_detail_type'),
                                                'total_weight':package.get('total_weight'),
                                                'total_weight_unit':package.get('total_weight_unit'),
                                                'total_volume':package.get('total_volume'),
                                                'total_volume_unit':package.get('total_volume_unit'),
                                                'consignee_details':package.get('consignee_details'),
                                                'shipper_details':package.get('shipper_details')
                                                })

                    if package.get('id'):
                        package_data = package_detail_model.objects.filter(quote_id=quote_id).values_list('id',flat=True)
                        if package_data:
                            package_object = package_detail_model.objects.get(id=package.get('id'), quote_id=quote_id)
                            package_detail_model.objects.filter(id=package.get('id')).update(**package_detail_data)
                            
                            # Set transport modes for package details
                            package_object.transport_mode.add(*transport_mode_id_data)

                            # Set commodities for package details
                            if 'commodity' in package:
                                request_commodity_ids = [i.id for i in package['commodity']]
                                db_commodity_ids = list(package_detail_model.objects.filter(id=package['id'], quote_id=quote_id).values_list('commodity', flat=True))
                                deleted_commodity_ids = Diff(db_commodity_ids, request_commodity_ids)
                                package_object.commodity.remove(*deleted_commodity_ids)
                                package_object.commodity.add(*package['commodity'])
                            
                    else:
                        package_detail = package_detail_model(**package_detail_data)
                        package_detail.save()

                        # Set transport modes for package details
                        package_detail.transport_mode.add(*transport_mode_id_data)

                        # Set commodities for package details
                        if 'commodity' in package:
                            cargo_commodities = package.get('commodity')
                            package_detail.commodity.add(*cargo_commodities)


            if cargo_detail['containers']:
                for container in cargo_detail['containers']:
                    container_detail_data.update({'stuffing': container['stuffing'],
                                                  'destuffing': container['destuffing'],
                                                  'is_hazardous': container['is_hazardous'],
                                                  'is_stackable': container['is_stackable'],
                                                  'weight': container['weight'],
                                                  'weight_unit': container['weight_unit'],
                                                  'container_type': container['container_type'],
                                                  'container_subtype': container['container_subtype'],
                                                  'shipper_details': container.get('shipper_details'),
                                                  'consignee_details': container.get('consignee_details')
                                                  })

                    if container['container_subtype'] == 'RF' and container['cargo_type'] == 'container':

                        if container['stuffing'] == 'factory':
                            container_detail_data.update({'temperature': container['temperature'],
                                                          'temperature_unit': container['temperature_unit']})

                    if container['is_fcl_container']:
                        container_detail_data.update({'is_fcl_container': True})

                    # Update container details
                    if container.get('id'):
                        container_data = package_detail_model.objects.filter(quote_id=quote_id, is_fcl_container=True).values_list('id',flat=True)
                        if container_data:

                            # Delete container packages when removed from request body
                            requ_container_id = container.get('id')
                            pack_cont_db = package_detail_model.objects.filter(container_id=requ_container_id,quote_id=quote_id).values_list('id', flat=True)
                            pack_cont_db_ids = [i for i in pack_cont_db]                        
                            req_container_pack = [i.get('id') for i in container['packages']]
                            deleted_con_package = Diff(pack_cont_db_ids, req_container_pack)

                            for id_data in deleted_con_package:
                                to_delete_con_package = package_detail_model.objects.filter(id=id_data, quote_id=quote_id)
                                to_delete_con_package.delete()

                            container_object = package_detail_model.objects.get(id=container.get('id'), quote_id=quote_id)
                            container_detail = package_detail_model.objects.filter(id=container.get('id'), quote_id=quote_id).update(**container_detail_data)
            

                            # Set transport modes for package details
                            container_object.transport_mode.add(*transport_mode_id_data)

                            if 'commodity' in container and container['stuffing'] == 'factory':
                                container_commodities = container['commodity']
                                container_object.commodity.add(*container_commodities)

                            container_package_data.update({'container_id': container_object.id})

                            if container['packages']:
                                for container_package in container['packages']:
                                    if cargo_detail['is_fcl_container']:
                                        container_package_data.update({'quote_id': quote_id,
                                                                    'pickup_location': self._get_quote_location(
                                                                        quote_id=quote_id,
                                                                        location=
                                                                        container_package[
                                                                            'pickup_location'],
                                                                        address_type='pickup'),
                                                                    'drop_location': self._get_quote_location(
                                                                        quote_id=quote_id,
                                                                        location=
                                                                        container_package[
                                                                            'drop_location'],
                                                                        address_type='drop')
                                                                    if 'drop_location' in container_package else None
                                                                    })

                                    container_package_data.update({'type': container_package['type'],
                                                                'quantity': container_package['quantity'],
                                                                'length': container_package['length'],
                                                                'width': container_package['width'],
                                                                'height': container_package['height'],
                                                                'dimension_unit': container_package['dimension_unit'],
                                                                'weight': container_package['weight'],
                                                                'weight_unit': container_package['weight_unit'],
                                                                'consignee_details':container_package.get('consignee_details'),
                                                                'shipper_details':container_package.get('shipper_details')
                                                                })

                                    if container['stuffing'] == 'dock':
                                        container_package_data.update({'is_hazardous': container_package['is_hazardous'],
                                                                    'is_stackable': container_package['is_stackable'],
                                                                    })
                                

                                    # Update Container packages
                                    if container_package.get('id'):
                                        container_package_object = package_detail_model.objects.get(id=container_package.get('id'), quote_id=quote_id)
                                        container_package_detail = package_detail_model.objects.filter(id=container_package.get('id'), quote_id=quote_id).update(**container_package_data)
                                    

                                        if container['stuffing'] == 'dock':
                                            # Set transport modes for package details
                                            container_package_object.transport_mode.add(*transport_mode_id_data)

                        
                                            if 'commodity' in container:
                                                request_commodity_ids = [i.id for i in container_package['commodity']]
                                                db_commodity_ids = list(package_detail_model.objects.filter(id=container_package['id'], quote_id=quote_id).values_list('commodity', flat=True))
                                                deleted_commodity_ids = Diff(db_commodity_ids, request_commodity_ids)
                                                container_package_object.commodity.remove(*deleted_commodity_ids)
                                                container_package_object.commodity.add(*container_package['commodity'])
                                    
                                    # Adding new container packages while updating
                                    else:
                                        container_package_data.update({'container_id':container_object.id})
                                        container_package_detail = package_detail_model(**container_package_data)
                                        container_package_detail.save()

                                        if container['stuffing'] == 'dock':
                                            # Set transport modes for package details
                                            container_package_detail.transport_mode.add(*transport_mode_id_data)

                                            if 'commodity' in container:
                                                container_package_commodities = container_package['commodity']
                                                container_package_detail.commodity.add(*container_package_commodities)
                    
                    else:
                        container_detail = package_detail_model(**container_detail_data)
                        container_detail.save()

                        # Set transport modes for package details
                        container_detail.transport_mode.add(*transport_mode_id_data)

                        if 'commodity' in container and container['stuffing'] == 'factory':
                            container_commodities = container['commodity']
                            container_detail.commodity.add(*container_commodities)

                        container_id = container_detail.id

                        container_package_data.update({'container_id': container_id})

                        if container['packages']:
                            for container_package in container['packages']:
                                if cargo_detail['is_fcl_container']:
                                    container_package_data.update({'quote_id': quote_id,
                                                                'pickup_location': self._get_quote_location(
                                                                    quote_id=quote_id,
                                                                    location=
                                                                    container_package[
                                                                        'pickup_location'],
                                                                    address_type='pickup'),
                                                                'drop_location': self._get_quote_location(
                                                                    quote_id=quote_id,
                                                                    location=
                                                                    container_package[
                                                                        'drop_location'],
                                                                    address_type='drop')
                                                                if 'drop_location' in container_package else None
                                                                })

                                container_package_data.update({'type': container_package['type'],
                                                            'quantity': container_package['quantity'],
                                                            'length': container_package['length'],
                                                            'width': container_package['width'],
                                                            'height': container_package['height'],
                                                            'dimension_unit': container_package['dimension_unit'],
                                                            'weight': container_package['weight'],
                                                            'weight_unit': container_package['weight_unit'],
                                                            'consignee_details':container_package.get('consignee_details'),
                                                            'shipper_details':container_package.get('shipper_details')
                                                            })

                                if container['stuffing'] == 'dock':
                                    container_package_data.update({'is_hazardous': container_package['is_hazardous'],
                                                                'is_stackable': container_package['is_stackable'],
                                                                })

                                container_package_detail = package_detail_model(**container_package_data)
                                container_package_detail.save()

                                if container['stuffing'] == 'dock':
                                    # Set transport modes for package details
                                    container_package_detail.transport_mode.add(*transport_mode_id_data)

                                    if 'commodity' in container:
                                        container_package_commodities = container_package['commodity']
                                        container_package_detail.commodity.add(*container_package_commodities)
                                        
                                        
    def _generate_or_update_quote_number(self, basic_details, customer_home_company_country, quote_no=None):
        # Get Transport mode initials 
        transport_modes = basic_details['transport_mode']
        transport_mode_initial = ""
        if 'Air' in transport_modes:
            transport_mode_initial += 'A'
        if 'Air_courier' in transport_modes:
            transport_mode_initial += 'C'
        if 'FCL' in transport_modes:
            transport_mode_initial += 'F'
        if 'LCL' in transport_modes:
            transport_mode_initial += 'L'


        # Based on customer home company country ,shipment type will import or export or Third country
        customer_home_company_country_id = customer_home_company_country['country']
        drop_location_country = basic_details['drop_location'][0]['country'].id
        pickup_location_country = basic_details['pickup_location'][0]['country'].id

        if pickup_location_country == customer_home_company_country_id:
            shipment_type = 'E'
            shipment = 'export'

        if drop_location_country == customer_home_company_country_id:
            shipment_type = 'I'
            shipment = 'import'

        if pickup_location_country != customer_home_company_country_id and drop_location_country != customer_home_company_country_id:
            shipment_type = 'T'
            shipment = 'third-country'

        Generate_or_replace_quote_number = transport_mode_initial + shipment_type 

  
        if not quote_no:

            # create a financial year of last two digit (financial year start from  1 April to 31 march)
            fiscalyear.START_MONTH = 4
            financial_year = fiscalyear.FiscalYear(datetime.datetime.now().year)
            financial_year_last_two_digit = str(financial_year.fiscal_year)[-2:]
            
            # counter variable start from 0001  for generate a unique no and store in DB
            quote_obj = self.model.objects.all().order_by('id').last()
            counter_id = 0
            if quote_obj and quote_obj.quote_no_counter:
                counter_id = quote_obj.quote_no_counter
            counter = str(counter_id+1).zfill(4)
            quote_number = Generate_or_replace_quote_number + financial_year_last_two_digit + counter
            return quote_number, counter,shipment
    

        # split word and no  of quote no .
        financial_yr_and_counter_no = re.findall(r'(\w+?)(\d+)',quote_no)[0][1]
        quote_number =  Generate_or_replace_quote_number + financial_yr_and_counter_no
        return quote_number,shipment


    def create_quote(self, company_id, basic_details, customer_home_company_country, cargo_details=None, additional_details=None):
        """
        Manager method for creating quote
        :param company_id:
        :type company_id:
        :param basic_details:
        :type basic_details:
        :param cargo_details:
        :type cargo_details:
        :param additional_details:
        :type additional_details:
        :return:
        :rtype:
        """

        # Quote basic details creation
        quote_data = {}

        company = Company.objects.get(id=company_id)
        quote_data['company'] = company

        shipment_terms = basic_details['shipment_terms'].split("_")
        quote_data['shipment_terms'] = basic_details['shipment_terms']
        quote_data['expected_delivery_date'] = basic_details['expected_delivery_date'] if shipment_terms[2] == 'door' \
            else None
        quote_data['expected_arrival_date'] = basic_details['expected_arrival_date'] if shipment_terms[2] == 'port' \
            else None
        quote_data['is_origin_custom'] = basic_details['is_origin_custom']
        quote_data['is_destination_custom'] = basic_details['is_destination_custom']
        quote_data['is_personal_courier'] = basic_details['is_personal_courier']
        quote_data['is_commercial_courier'] = basic_details['is_commercial_courier']
        quote_data['quote_status'] = 'pending'
        quote_data['quote_no'],quote_data['quote_no_counter'],quote_data['shipment_type'] = self._generate_or_update_quote_number(basic_details, customer_home_company_country)

        if 'is_submit_quote' in basic_details and basic_details['is_submit_quote'] == True:
            quote_data['is_submit_quote'] = basic_details['is_submit_quote']
            quote_data['quote_status'] = 'open'
        quote_obj = self.model(**quote_data)
        quote_obj.save()

        # Quote transport mode creation
        quote_transport_mode = apps.get_model('quote', 'QuoteTransportMode')
        transport_modes = [quote_transport_mode(transport_mode=transport_mode, quote=quote_obj)
                           for transport_mode in basic_details['transport_mode']]
        result_transport_mode = quote_transport_mode.objects.bulk_create(transport_modes)
        transport_mode_ids = [transport_mode.id for transport_mode in result_transport_mode]

        # Pickup location address creation
        self._create_quote_address(quote_id=quote_obj.id, basic_details=basic_details, address_type='pickup')

        # Drop location address creation
        self._create_quote_address(quote_id=quote_obj.id, basic_details=basic_details, address_type='drop')

        # Create package details
        if 'Air' in basic_details['transport_mode'] or 'Air_courier' in basic_details['transport_mode'] or \
                'LCL' in basic_details['transport_mode']:
            self._create_package_details(quote_obj.id, transport_mode_ids, cargo_details)

        if 'FCL' in basic_details['transport_mode']:
            self._create_fcl_package_details(quote_obj.id, transport_mode_ids, cargo_details)

        # Create Additional details
        self._create_additional_details(quote_obj, additional_details)


    def update_quote(self, company_id, quote_id, basic_details,customer_home_company_country, cargo_details=None, additional_details=None):
        """
        Manager method for updating quote
        :param company_id:
        :type company_id:
        :param basic_details:
        :type basic_details:
        :param cargo_details:
        :type cargo_details:
        :param additional_details:
        :type additional_details:
        :return:
        :rtype:
        """

        # Quote basic details updation
        quote_data = {}

        quote_data['company'] = company_id
        quote_data['id'] = quote_id

        shipment_terms = basic_details['shipment_terms'].split("_")
        quote_data['shipment_terms'] = basic_details['shipment_terms']
        quote_data['expected_delivery_date'] = basic_details['expected_delivery_date'] if shipment_terms[2] == 'door' \
            else None
        quote_data['expected_arrival_date'] = basic_details['expected_arrival_date'] if shipment_terms[2] == 'port' \
            else None
        quote_data['is_origin_custom'] = basic_details['is_origin_custom']
        quote_data['is_destination_custom'] = basic_details['is_destination_custom']
        quote_data['is_personal_courier'] = basic_details['is_personal_courier']
        quote_data['is_commercial_courier'] = basic_details['is_commercial_courier']

        quote_obj = self.model.objects.filter(id=quote_id, company_id=company_id).update(**quote_data)

        # Quote transport mode updation
        quote_transport_mode = apps.get_model('quote', 'QuoteTransportMode')
        transport_modes = basic_details['transport_mode']

        quote_transport_mode_data = {}

        transport_mode_type_data = list(quote_transport_mode.objects.filter(quote_id=quote_id).values_list('transport_mode', flat=True))

        deleted_transport_modes = Diff(transport_mode_type_data, transport_modes)

        for transport_mode in deleted_transport_modes:
            transport_data = quote_transport_mode.objects.get(quote_id=quote_id, transport_mode=transport_mode)
            transport_data.delete()

        for transport_mode in transport_modes:
            quote_transport_mode_data['quote_id'] = quote_id
            quote_transport_mode_data['transport_mode'] = transport_mode

            transport_mode_data = quote_transport_mode.objects.filter(quote_id=quote_id, transport_mode=transport_mode).values()
            
            if len(transport_mode_data) > 0:
                quote_transport_mode.objects.filter(id=transport_mode_data[0]['id']).update(**quote_transport_mode_data)

            else:
                new_transport_mode = quote_transport_mode(**quote_transport_mode_data)
                new_transport_mode.save()

        transport_mode_id_data = list(quote_transport_mode.objects.filter(quote_id=quote_id).values_list('id', flat=True))

        # Pickup location address updation
        self._update_quote_address(quote_id=quote_id, basic_details=basic_details, address_type='pickup')

        # Drop location address updation
        self._update_quote_address(quote_id=quote_id, basic_details=basic_details, address_type='drop')

        # generate or update quote no 
        quote_details = self.model.objects.get(id=quote_id)
        quote_number = quote_details.quote_no
        quote_status = quote_details.quote_status
        if 'is_submit_quote' in basic_details and basic_details['is_submit_quote'] == True:
            quote_data['is_submit_quote'] = basic_details['is_submit_quote']
            current_date = datetime.date.today()
            quote_data['quote_status'] = 'open'
            quote_deadline_date =  quote_data['quote_deadline'] if 'quote_deadline' in basic_details else  quote_details.quote_deadline
            if (quote_status == 'pending' or   quote_status == 'open') and (current_date > quote_deadline_date):
                quote_data['quote_status'] = 'expired'

        if quote_number:
            quote_data['quote_no'],quote_data['shipment_type']= self._generate_or_update_quote_number(basic_details, customer_home_company_country, quote_number)
        
        self.model.objects.filter(id=quote_id, company_id=company_id).update(**quote_data)

        # Update package details
        if 'Air' in basic_details['transport_mode'] or 'Air_courier' in basic_details['transport_mode'] or \
                'LCL' in basic_details['transport_mode']:
            self._update_package_details(quote_id, transport_mode_id_data, cargo_details)

        if 'FCL' in basic_details['transport_mode']:
            self._update_fcl_package_details(quote_id, transport_mode_id_data, cargo_details)

        # Update Additional details
        self._update_additional_details(quote_id, additional_details)

        

    def duplicate_quote(self, company_id, quote_id):

        Quote = apps.get_model('quote', 'Quote')
        QuoteTransportMode = apps.get_model('quote', 'QuoteTransportMode')
        PackageDetails = apps.get_model('quote', 'PackageDetails')

        obj = Quote.objects.get(pk=quote_id, company_id=company_id)
        quote_no = obj.quote_no

        # Quote number updation
        transport_mode_char = re.findall(r'(\w+?)(\d+)',quote_no)[0][0]
        fiscalyear.START_MONTH = 4
        financial_year = fiscalyear.FiscalYear(datetime.datetime.now().year)
        financial_year_last_two_digit = str(financial_year.fiscal_year)[-2:]
        quote_obj = Quote.objects.all().order_by('id').last()
        counter_id = quote_obj.quote_no_counter
        counter = str(counter_id+1).zfill(4)
        quote_number = transport_mode_char + financial_year_last_two_digit + counter

        # Updating quote deadline
        quote_date = Quote.objects.filter(id=quote_id, company_id=company_id).values_list('created_at', 'quote_deadline')[0]
        created_at, deadline_date = quote_date
        # created_at.strftime('%Y-%m-%d') will give same output as created_at.date() but will have type as string.
        delta = deadline_date - created_at.date()
        diff_days = (delta.days)
        new_deadline = deadline_date + timedelta(days=diff_days)

        obj.quote_no_counter = counter
        obj.quote_no = quote_number
        obj.quote_deadline = new_deadline
        obj.pk = None
        obj.save()

        # Adding transport mode
        transport_mode_data = QuoteTransportMode.objects.filter(quote_id=quote_id)
        transport_object = {}
        for transport_mode in transport_mode_data:
            transport_object['quote_id'] = obj.id
            transport_object['transport_mode'] = transport_mode
            new_transport_mode = QuoteTransportMode(**transport_object)
            new_transport_mode.save()


        # Adding preference and depreference in duplicated quote
        preference_deprefernce_data = Quote.objects.filter(id=quote_id, company_id=company_id).values('preference','depreference')
        for data in preference_deprefernce_data:
            if data['preference']:
                obj.preference.add(data['preference'])
            if data['depreference']:
                obj.depreference.add(data['depreference'])    

        # Creating address
        address_object = Address.objects.filter(entity_type='quote', entity_id=quote_id)
        new_address_ids = []

        for data in address_object:
            data.pk = None
            data.entity_id = obj.id
            data.save()
            new_address_ids.append(data.id)
    
        # Adding airport_ids and seaport_ids
        old_address_data = Address.objects.filter(entity_type='quote', entity_id=quote_id).values('type','airport_ids','seaport_ids')
        for data in old_address_data:
            if data['type'] == 'pickup':
                for ids in new_address_ids:
                    address_object = Address.objects.filter(id=ids).values_list('type', flat=True)[0]
                    if address_object == 'pickup':
                        new_address_object = Address.objects.get(id=ids)
                        if data['airport_ids']:
                            new_address_object.airport_ids.add(data['airport_ids'])
                        if data['seaport_ids']:
                            new_address_object.seaport_ids.add(data['seaport_ids'])
            if data['type'] == 'drop':
                for ids in new_address_ids:
                    address_object = Address.objects.filter(id=ids).values_list('type', flat=True)[0]
                    if address_object == 'drop':
                        new_address_object = Address.objects.get(id=ids)
                        if data['airport_ids']:
                            new_address_object.airport_ids.add(data['airport_ids'])
                        if data['seaport_ids']:
                            new_address_object.seaport_ids.add(data['seaport_ids'])

        # Adding packages
        package_data = PackageDetails.objects.filter(quote_id=quote_id)
        address_new_data = Address.objects.filter(entity_id=obj.id, entity_type='quote')
        for package in package_data:
            for address_object in address_new_data:
                package_address_pickup = Address.objects.filter(id = package.pickup_location_id , entity_id=quote_id)
                package_address_drop = Address.objects.filter(id = package.drop_location_id, entity_id=quote_id)
                if package_address_pickup:
                    if package_address_pickup[0].address1 == address_object.address1 or package_address_pickup[0].country == address_object.country and package_address_pickup[0].type == 'pickup':
                        package.pickup_location_id = address_object.id
                if package_address_drop:
                    if package_address_drop[0].address1 == address_object.address1 or package_address_drop[0].country == address_object.country and package_address_drop[0].type == 'drop':
                        package.drop_location_id = address_object.id

            package.quote_id = obj.id
            package.pk = None
            package.save()
    
        # Updating container id in its package
        old_package_ids = PackageDetails.objects.filter(quote_id=quote_id)
        old_ids = [ids.id for ids in old_package_ids]
        new_package_ids = PackageDetails.objects.filter(quote_id=obj.id)
        new_ids = [ids.id for ids in new_package_ids]

        for container_data in old_package_ids:
            if container_data.is_fcl_container == True:
                container_id = container_data.id
                index_of_container = old_ids.index(container_id)
                new_container_id = new_ids[index_of_container]
                old_container_packages_ids =  [ids.id for ids in PackageDetails.objects.filter(container_id=container_id,quote_id=quote_id)]
                indexs_of_packages = []
                for ids in old_container_packages_ids:
                    old_package_index = old_ids.index(ids)
                    PackageDetails.objects.filter(id=new_ids[old_package_index]).update(container_id=new_container_id)
        
    
        # Adding commodity and transport mode to packages
        for data in package_data.values('commodity','transport_mode'):   
            for ids in new_ids:
                package_obj = PackageDetails.objects.get(id=ids)
                if data['commodity']:
                    package_obj.commodity.add(data['commodity'])
                package_obj.transport_mode.add(data['transport_mode'])

                
    def update_manage_quote(self, company_id, quote_id, data):
        quote_data = {}
        quote ={}
        package_detail_model = apps.get_model('quote', 'PackageDetails')
        if 'po_number' in data:
            quote['po_number'] = data['po_number']
        if 'quote_deadline' in data:
            quote['quote_deadline'] = data['quote_deadline']
        self.model.objects.filter(~Q(status=StatusBase.INACTIVE),id=quote_id).update(**quote)
        if 'packages' in data:
            package_data={}
            for packages in data['packages']:
                if 'shipper_details' in packages:
                    package_data.update({'shipper_details':packages['shipper_details']})
                if 'consignee_details' in packages:
                    package_data.update({'consignee_details':packages['consignee_details']})
                package_object = package_detail_model.objects.filter(id=packages['id'],quote_id=quote_id,is_fcl_container=False)
                if package_object:
                    package_object.update(**package_data)
                                
        if 'container_details' in data:
            container_data={}
            for fcl_container in data['container_details']:
                if 'shipper_details' in fcl_container:
                    container_data.update({'shipper_details':fcl_container['shipper_details']})
                if 'consignee_details' in fcl_container:
                    container_data.update({'consignee_details':fcl_container['consignee_details']})

                container_id = fcl_container['id']
                container_object = package_detail_model.objects.filter(id=container_id,quote_id=quote_id,is_fcl_container=True)
                if container_object:
                    container_object.update(**container_data)
                if 'container_packages' in fcl_container:
                    fcl_container_packages={}
                   
                    for fcl_package in fcl_container['container_packages']:
                        if 'shipper_details' in fcl_container:
                            fcl_container_packages.update({'shipper_details':fcl_package['shipper_details']})
                        if 'consignee_details' in fcl_container:
                            fcl_container_packages.update({'consignee_details':fcl_package['consignee_details']})
                        fcl_package_object = package_detail_model.objects.filter(id=fcl_package['id'],quote_id=quote_id,container_id=container_id)
                        if fcl_package_object:
                            fcl_package_object.update(**fcl_container_packages)
                                
