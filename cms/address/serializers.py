from address.models.address import Address
from city.serializers import CitySerializer
from country.serializers import CountrySerializer
from django_restql.mixins import DynamicFieldsMixin
from port.models.port import Port
from rest_framework import serializers
from state.serializers import StateSerializer
from utils.base_models import QuoteChoice
from country.models.country import Country


class AddressSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Address
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']

class PortDetailsSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Port
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']

class AddressDetailSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    country = CountrySerializer()
    state = StateSerializer(required=False)
    city = CitySerializer(required=False)

    class Meta:
        model = Address
        fields = ['id', 'address1', 'address2', 'state', 'city', 'country', 'pincode', 'type', 'entity_type',
                  'entity_id']
        read_only_fields = ['id']

class QuoteAddressDetailSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    country = CountrySerializer()
    state = StateSerializer(required=False)
    city = CitySerializer(required=False)
    airport_ids = PortDetailsSerializer(many = True,required = False)
    seaport_ids = PortDetailsSerializer(many = True,required = False)

    class Meta:
        model = Address
        fields = ['id', 'address1', 'address2', 'state', 'city', 'pincode', 'country','type', 'entity_type',
                  'entity_id','airport_ids','seaport_ids']
        read_only_fields = ['id']


class AddressBaseSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """
        Serializer for address info in registration step.
    """
    street = serializers.CharField(max_length=255, source='address1')

    class Meta:
        model = Address
        fields = ['country', 'state', 'city', 'pincode', 'street']

        extra_kwargs = {
            'country': {'error_messages': {'does_not_exist': 'Invalid country.'}},
            'state': {'error_messages': {'does_not_exist': 'Invalid state.'}},
            'city': {'error_messages': {'does_not_exist': 'Invalid city.'}}
        }


class LocationSerializer(serializers.ModelSerializer):
    """
        Serializer for address info in registration step.
    """
    id = serializers.IntegerField(required=False)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects,error_messages={"does_not_exist": "Invalid "
                                                                                                       "seaport id"},required=False, allow_null=True)
    street = serializers.CharField(max_length=255, source='address1', required=False)
    shipment_terms = serializers.CharField(max_length=255,required=False)
    transport_mode = serializers.MultipleChoiceField(choices=QuoteChoice.QUOTE_TRANSPORT_MODE_CHOICES,
                                                     allow_empty=False,required=False)
    airport_ids = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Port.objects,
                                                                                 write_only=True,
                                                                                 error_messages=
                                                                                 {
                                                                                     "does_not_exist": "Invalid "
                                                                                                       "airport id"}),
                                        required=False)
    seaport_ids = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Port.objects,
                                                                                 write_only=True,
                                                                                 error_messages=
                                                                                 {
                                                                                     "does_not_exist": "Invalid "
                                                                                                       "seaport id"}),
                                        required=False)

    class Meta:
        model = Address
        fields = ['shipment_terms', 'transport_mode', 'airport_ids', 'seaport_ids', 'country', 'state', 'city',
                  'pincode', 'street','id']

        extra_kwargs = {
            'id': {'read_only': False, 'write_only':False},
            'country': {'error_messages': {'does_not_exist': 'Invalid country.'}},
            'state': {'error_messages': {'does_not_exist': 'Invalid state.'}},
            'city': {'error_messages': {'does_not_exist': 'Invalid city.'}}
        }

    def validate(self, data):
        transport_mode = data.get('transport_mode')
        shipment_terms = data.get('shipment_terms').split("_")
        airport_ids = data.get('airport_ids')
        seaport_ids = data.get('seaport_ids')

        errors = {}
        if shipment_terms[0] == 'port' or shipment_terms[2] == 'port':

            if 'Air' in transport_mode or 'Air_courier' in transport_mode:
                if not airport_ids:
                    errors.update({'airport_ids': 'Airport is required.'})

            if 'LCL' in transport_mode or 'FCL' in transport_mode:
                if not seaport_ids:
                    errors.update({'seaport_ids': 'Seaport is required.'})

        if errors:
            raise serializers.ValidationError(errors)

        return data
