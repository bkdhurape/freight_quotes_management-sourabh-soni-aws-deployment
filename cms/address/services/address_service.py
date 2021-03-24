from address.models.address import Address
from address.serializers import AddressSerializer, AddressDetailSerializer
from exceptions.address_exceptions import AddressException, AddressError
from utils.base_models import StatusBase


class AddressService:
    def __init__(self, data):
        self.data = data

    '''To create address'''

    def create(self):
        address_serializer = AddressSerializer(data=self.data)
        if address_serializer.is_valid(raise_exception=True):
            address_serializer.save()

    '''to get address data'''
    def get(entity_type, entity_id, fields=None):
        address = Address.find_by(status=StatusBase.ACTIVE,
                                  entity_type=entity_type,
                                  entity_id=entity_id,
                                  multi=True)
        address_serializer = AddressDetailSerializer(address,
                                                     many=True,
                                                     fields=fields)
        return address_serializer.data[0] if len(
            address_serializer.data) > 0 else {}

    def check_country(self, entity_id, entity_type, id):
        address = Address.find_by(
            entity_id=entity_id, entity_type=entity_type, id=id)
        address_serializer = AddressSerializer(address)
        if address_serializer.data['country'] != self.data['country']:
            raise AddressException(
                AddressError.COUNTRY_CAN_NOT_BE_UPDATED)

    '''To edit address data '''

    def update(self, entity_id, entity_type, id):
        address = Address.find_by(
            entity_id=entity_id, entity_type=entity_type, id=id)
        address_serializer = AddressSerializer(address, data=self.data)
        if address_serializer.is_valid(raise_exception=True):
            address_serializer.save()
        else:
            return address_serializer.errors

    def delete(type, entity_id, id=None):
        condition = {}

        if id is None:
            condition = {'type': type, 'entity_id': entity_id}
        else:
            condition = {'type': type, 'entity_id': entity_id, 'id': id}

        address = Address.find_by(multi=True, **condition)
        if address:
            address.delete()
