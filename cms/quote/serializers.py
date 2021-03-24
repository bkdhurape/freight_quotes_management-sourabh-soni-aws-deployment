from address.serializers import LocationSerializer,QuoteAddressDetailSerializer
from address.models.address import Address
from commodity.models.commodity import Commodity
from django_restql.mixins import DynamicFieldsMixin
from quote.models.package_details import PackageDetails
from quote.models.quote import Quote
from quote.models.quote_order_ready import QuoteOrderReady
from quote.models.quote_transport_mode import QuoteTransportMode
from rest_framework import serializers
from utils.base_models import QuoteChoice
from utils.helpers import unique
from decimal import Decimal
from django.core.validators import MinValueValidator, RegexValidator
import datetime


class QuoteSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    transport_modes = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Quote
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']
    

class QuoteTransportModeSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = QuoteTransportMode
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']

class PackageDetailsSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = PackageDetails
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']

class PackageLooseSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    transport_mode = serializers.StringRelatedField(many=True)

    class Meta:
        model = PackageDetails
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']


class QuotePackageDetailsSerializers(DynamicFieldsMixin, serializers.ModelSerializer):
    transport_mode = serializers.StringRelatedField(many=True)
    commodity = serializers.StringRelatedField(many=True)
    pickup_location = QuoteAddressDetailSerializer()
    drop_location = QuoteAddressDetailSerializer()



    class Meta:
        model = PackageDetails
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']


class QuoteOrderReadySerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = QuoteOrderReady
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']


class BasicDetailsSerializer(serializers.ModelSerializer):
    """
        Serializer for Quote basic details
    """
    transport_mode = serializers.MultipleChoiceField(choices=QuoteChoice.QUOTE_TRANSPORT_MODE_CHOICES,
                                                     allow_empty=False)
    pickup_location = LocationSerializer(many=True)
    drop_location = LocationSerializer(many=True)

    class Meta:
        model = Quote
        fields = ['transport_mode', 'pickup_location', 'drop_location', 'shipment_terms', 'expected_delivery_date',
                  'is_origin_custom', 'is_destination_custom', 'expected_arrival_date', 'is_personal_courier',
                  'is_commercial_courier','is_submit_quote']

    def validate(self, data):
        transport_mode = data.get('transport_mode')
        shipment_terms = data.get('shipment_terms').split("_")
        expected_delivery_date = data.get('expected_delivery_date')
        expected_arrival_date = data.get('expected_arrival_date')
        is_personal_courier = data.get('is_personal_courier')
        is_commercial_courier = data.get('is_commercial_courier')

        errors = {}
        if shipment_terms[2] == 'door':
            if not expected_delivery_date:
                errors.update({'expected_delivery_date': 'Expected delivery date is required.'})
        if shipment_terms[2] == 'port':
            if not expected_arrival_date:
                errors.update({'expected_arrival_date': 'Expected arrival date is required.'})

        if 'Air_courier' in transport_mode:
            if (is_personal_courier is False or not is_personal_courier) and \
                    (is_commercial_courier is False or not is_commercial_courier):
                raise serializers.ValidationError('For Air_courier, personal_courier or '
                                                  'commercial_courier is required.')

        if errors:
            raise serializers.ValidationError(errors)

        return data


class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']


class PackageDetailsSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    container_id = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(allow_null=True, required=False)
    width = serializers.FloatField(allow_null=True, required=False)
    height = serializers.FloatField(allow_null=True, required=False)
    dimension_unit = serializers.ChoiceField(choices=QuoteChoice.DIMENSION_UNIT_CHOICES, required=False, allow_null=True)
    weight = serializers.FloatField(allow_null=True, required=False)
    weight_unit = serializers.ChoiceField(choices=QuoteChoice.WEIGHT_UNIT_CHOICES, required=False, allow_null=True)
    commodity = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Commodity.objects,
                                                                               write_only=True), required=False)
    total_weight = serializers.FloatField(allow_null=True, required=False)
    total_weight_unit = serializers.ChoiceField(choices=QuoteChoice.WEIGHT_UNIT_CHOICES, required=False)
    total_volume = serializers.FloatField(allow_null=True, required=False)
    total_volume_unit = serializers.ChoiceField(choices=QuoteChoice.VOLUME_UNIT_CHOICES, required=False)
    is_stackable = serializers.BooleanField(required=False)
    is_hazardous = serializers.BooleanField(required=False)
    package_detail_type = serializers.CharField(max_length=255, required=False)

    container_stuffing = serializers.CharField(max_length=255, required=False)
    container_subtype = serializers.CharField(max_length=255, required=False)

    pickup_location = LocationSerializer(required=False)
    drop_location = LocationSerializer(required=False)

    stuffing = serializers.CharField(required=False)
    destuffing = serializers.CharField(required=False)

    temperature = serializers.FloatField(allow_null=True, required=False)
    temperature_unit = serializers.ChoiceField(choices=QuoteChoice.TEMPERATURE_UNIT_CHOICES, required=False)


    class Meta:
        model = PackageDetails
        fields = ['id','container_id','type', 'quantity', 'length', 'width', 'height', 'dimension_unit', 'weight', 'weight_unit',
                  'is_hazardous', 'is_stackable', 'commodity', 'total_weight', 'total_weight_unit', 'total_volume',
                  'total_volume_unit', 'package_detail_type', 'pickup_location', 'drop_location', 'stuffing',
                  'destuffing', 'temperature', 'temperature_unit', 'container_stuffing', 'container_subtype','shipper_details','consignee_details']

    def validate(self, data):
        p_type = data.get('type')
        container_stuffing = data.get('container_stuffing')
        container_subtype = data.get('container_subtype')
        commodity = data.get('commodity')

        errors = {}
        if container_stuffing == 'dock':
            if 'commodity' not in data or not commodity:
                errors.update({'commodity': 'Commodity is required.'})
            if 'is_stackable' not in data:
                errors.update({'is_stackable': 'Stackable is required.'})
            if 'is_hazardous' not in data:
                errors.update({'is_hazardous': 'Hazardous is required.'})

        if p_type:
            package_detail_type = data.get('package_detail_type')

            if container_subtype == 'FR' and package_detail_type == 'total':
                raise serializers.ValidationError('For Flatrack container type, only dimensions are required')

            if package_detail_type == 'total':
                total_weight = data.get('total_weight')
                total_weight_unit = data.get('total_weight_unit')

                if not total_weight:
                    errors.update({'total_weight': 'Total weight is required.'})
                if not total_weight_unit:
                    errors.update({'total_weight_unit': 'Total weight unit is required.'})

            if package_detail_type == 'package':
                quantity = data.get('quantity')
                length = data.get('length')
                width = data.get('width')
                height = data.get('height')
                dimension_unit = data.get('dimension_unit')
                weight = data.get('weight')
                weight_unit = data.get('weight_unit')

                if not quantity:
                    errors.update({'quantity': 'Quantity is required.'})
                if not length:
                    errors.update({'length': 'Length is required.'})
                if not width:
                    errors.update({'width': 'Width is required.'})
                if not height:
                    errors.update({'height': 'Height is required.'})
                if not dimension_unit:
                    errors.update({'dimension_unit': 'Dimension unit is required.'})
                if not weight:
                    errors.update({'weight': 'Weight is required.'})
                if not weight_unit:
                    errors.update({'weight_unit': 'Weight unit is required.'})

        if errors:
            raise serializers.ValidationError(errors)

        return data


class ContainerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    packages = PackageDetailsSerializer(many=True, required=False)
    multi_drop = serializers.BooleanField(default=False)
    is_fcl_container = serializers.BooleanField(default=False)
    cargo_type = serializers.CharField(required=False)

    class Meta:
        model = PackageDetails
        fields = ['id','weight', 'weight_unit', 'container_type', 'container_subtype', 'no_of_containers', 'stuffing',
                  'destuffing', 'is_hazardous', 'is_stackable', 'commodity', 'packages', 'temperature',
                  'temperature_unit', 'multi_drop', 'shipper_details', 'consignee_details', 'is_fcl_container',
                  'cargo_type','shipper_details','consignee_details']

    def validate(self, data):
        container_type = data.get('container_type')
        stuffing = data.get('stuffing')
        destuffing = data.get('destuffing')
        commodity = data.get('commodity')
        packages = data.get('packages')
        multi_drop = data.get('multi_drop')
        shipper_details = data.get('shipper_details')
        consignee_details = data.get('consignee_details')
        is_fcl_container = data.get('is_fcl_container')

        errors = {}
        if container_type:
            container_subtype = data.get('container_subtype')
            no_of_containers = data.get('no_of_containers')
            weight = data.get('weight')
            weight_unit = data.get('weight_unit')
            temperature = data.get('temperature')
            temperature_unit = data.get('temperature_unit')

            if not container_subtype:
                errors.update({'container_subtype': 'Container sub-type is required.'})
            if not no_of_containers:
                errors.update({'no_of_containers': 'No. of containers is required.'})
            if not weight:
                errors.update({'weight': 'Weight is required.'})
            if not weight_unit:
                errors.update({'weight_unit': 'Weight unit is required.'})

            if container_subtype == 'FR' or container_subtype == 'OT':
                if 'packages' not in data or not packages:
                    errors.update({'packages': 'Package(s) is required.'})
            if container_subtype == 'RF':
                if not shipper_details:
                    errors.update({'shipper_details': 'Shipper details is required.'})
                if not temperature:
                    errors.update({'temperature': 'Temperature is required.'})
                if not temperature_unit:
                    errors.update({'temperature_unit': 'Temperature unit is required.'})

            if container_subtype == 'Tank':
                if not consignee_details:
                    errors.update({'consignee_details': 'Consignee details is required.'})

        if stuffing == 'factory':
            if 'commodity' not in data or not commodity:
                errors.update({'commodity': 'Commodity is required.'})
            if 'is_stackable' not in data:
                errors.update({'is_stackable': 'Stackable is required.'})
            if 'is_hazardous' not in data:
                errors.update({'is_hazardous': 'Hazardous is required.'})

        if stuffing == 'dock' or destuffing == 'dock':
            if 'packages' not in data or not packages:
                errors.update({'packages': 'Package(s) is required.'})

        if multi_drop:
            if destuffing == 'factory':
                errors.update({'destuffing': 'For multiple drop location, only dock destuffing is required'})

        package_same_location = []
        package_stuffing = []
        temperature_package = []
        non_temperature_package = []

        if is_fcl_container:
            package_same_location_count = {}
            package_stuffing_count = 0
            temperature_package_count = 0

            for package in packages:
                if package['stuffing'] == 'factory':
                    package_same_location.append(package['pickup_location']['address1'])
                package_stuffing.append(package['stuffing'])

                if package['temperature'] is not None:
                    temperature_package.append(package['temperature'])

                if package['temperature'] is None:
                    non_temperature_package.append(package['temperature'])

            package_same_location_count = unique(package_same_location)
            package_stuffing_count = unique(package_stuffing)
            temperature_package_count = unique(temperature_package)

            if len(package_same_location_count) > 1:
                raise serializers.ValidationError('For factory stuffing, package needs to be from same location.')

            if len(package_stuffing_count) > 1:
                raise serializers.ValidationError('For multiple packages with factory and dock stuffing, same '
                                                  'container cannot be used for different stuffing.')

            if len(temperature_package) > 0 and container_subtype != 'RF':
                raise serializers.ValidationError('Cannot add temperature controlled packages in this type of '
                                                  'container')

            if len(non_temperature_package) > 0 and container_subtype == 'RF':
                raise serializers.ValidationError('Cannot add non temperature controlled packages in this type of '
                                                  'container')

            if len(temperature_package_count) > 1:
                raise serializers.ValidationError('Same container cannot be used for different temperature packages.')

        if errors:
            raise serializers.ValidationError(errors)

        return data


class CargoDetailsSerializer(serializers.Serializer):

    transport_mode = serializers.ListField(child=serializers.CharField(),
                                           allow_empty=False,
                                           error_messages={"empty": "Transport mode is required.",
                                                           'required': "Transport mode is required."})

    packages = PackageDetailsSerializer(many=True, required=False)
    containers = ContainerSerializer(many=True, required=False)
    id =serializers.IntegerField(required=False)
    pickup_location = LocationSerializer(required=False)
    drop_location = LocationSerializer(required=False)

    multi_drop = serializers.BooleanField(default=False)
    is_fcl_container = serializers.BooleanField(default=False)

    is_order_ready = serializers.BooleanField(default=False)
    order_ready_date = serializers.DateField(validators=[MinValueValidator(datetime.date.today)] , allow_null=True, required=False)
    invoice_value = serializers.DecimalField(max_digits=10, decimal_places=4,  allow_null=True,required=False, validators=[MinValueValidator(Decimal('0.00'))])
    invoice_value_currency = serializers.CharField(default='INR', max_length=5, required=False)
    handover_date = serializers.DateField(validators=[MinValueValidator(datetime.date.today)] , allow_null=True, required=False)

    class Meta:
        model = PackageDetails
        fields = ['transport_mode', 'pickup_location', 'drop_location', 'packages', 'containers', 'multi_drop',
                  'is_fcl_container','is_order_ready','order_ready_date','invoice_value','invoice_value_currency','handover_date']

    def validate(self, data):
        transport_mode = data.get('transport_mode')
        multi_drop = data.get('multi_drop')
        packages = data.get('packages')

        errors = {}
        if ('Air' in transport_mode or 'LCL' in transport_mode) and 'packages' not in data:
            errors.update({'packages': 'Package details is required.'})

        if 'multi_drop' in data and multi_drop and 'packages' not in data and not packages:
            errors.update({'packages': 'Package details is required.'})

        if errors:
            raise serializers.ValidationError(errors)

        return data


class AdditionalDetailsSerializer(serializers.ModelSerializer):
    no_of_suppliers = serializers.IntegerField()
    
    class Meta:
        model = Quote
        fields = ['po_number', 'no_of_suppliers', 'quote_deadline', 'switch_awb', 'switch_b_l', 'packaging',
                  'palletization', 'preference', 'depreference']

    def validate(self, data):
        preference = data.get('preference')
        depreference = data.get('depreference')

        errors = {}

        if 'Air' in self.context:

            if not preference and not depreference:
                raise serializers.ValidationError('One should be selected either preference or depreference.')

            if preference and depreference:
                raise serializers.ValidationError('You can select either preference or depreference not both at the same '
                                                'time.')

            if preference and len(preference) > 5:
                errors.update({'preference': 'You can select only five airlines in preference'})

            if depreference and len(depreference) > 5:
                errors.update({'depreference': 'You can select only five airlines in de-preference'})
        else:
            preference = []
            depreference = []

        if errors:
            raise serializers.ValidationError(errors)

        return data


class QuoteCreationSerializer(serializers.Serializer):
    """
        Serializer for Quote creation
    """
    basic_details = BasicDetailsSerializer()
    cargo_details = CargoDetailsSerializer(many=True)
    additional_details = AdditionalDetailsSerializer()


class QuoteUpdateSerializer(serializers.Serializer):

    """
        Serializer for Quote updation
    """
    basic_details = BasicDetailsSerializer()
    cargo_details = CargoDetailsSerializer(many=True)
    additional_details = AdditionalDetailsSerializer()

class QuoteListingSerializers(serializers.ModelSerializer): 


    """
        Serializer for Quote Listing
    """
    transport_modes=serializers.StringRelatedField(many=True)
    quote_deadline = serializers.SerializerMethodField('get_quote_deadline')
    pickup_location = serializers.SerializerMethodField('get_pickup_location')
    drop_location = serializers.SerializerMethodField('get_drop_location')
    fcl_container_details = serializers.SerializerMethodField('get_fcl_container_details')

    def get_quote_deadline(self, obj):
        quote_obj = Quote.objects.get(id = obj.id)
        quote_type =  quote_obj.quote_status
        quote_deadline_date = quote_obj.quote_deadline
        current_date = datetime.date.today()
        if (quote_type == 'pending' or quote_type == 'open') and (current_date > quote_deadline_date):
            quote_type = 'expired'
            quote_data = {'quote_status':quote_type}
            Quote.objects.filter(id = obj.id).update(**quote_data)
        return  quote_deadline_date


    def get_pickup_location(self, obj):
        pickup_location = Address.objects.filter(entity_type ='quote', entity_id = obj.id, type = 'pickup' )
        serializer = QuoteAddressDetailSerializer(instance= pickup_location, many=True)
        pickups = serializer.data
        for pickup in  pickups:
            pickup_id = int(pickup['id'])
            package_details = PackageDetails.objects.filter(pickup_location = pickup_id,quote_id = obj.id,is_fcl_container=False,container__isnull=True)
            if package_details is not None:
                package = QuotePackageDetailsSerializers(instance=package_details, many=True,required = False,exclude = ['pickup_location'])
                pickup['packages_details'] = package.data 
                
            
        return  pickups

    def get_drop_location(self, obj):
        drop_location = Address.objects.filter(entity_type ='quote', entity_id = obj.id, type = 'drop')
        serializer = QuoteAddressDetailSerializer(instance=drop_location, many=True)
        drop_data = serializer.data

        return drop_data

    def get_fcl_container_details(self, obj):
        package_details = PackageDetails.objects.filter(quote_id = obj.id,is_fcl_container=True,container__isnull=True)
        serializer = QuotePackageDetailsSerializers(instance= package_details, many=True)
        containers = serializer.data
        for container in  containers:
            container_id = int(container['id'])
            fcl_package_details = PackageDetails.objects.filter(container = container_id,quote_id = obj.id,container__isnull=False)
            if fcl_package_details is not None:
                fcl_package = QuotePackageDetailsSerializers(instance=fcl_package_details, many=True,required = False)
                container['fcl_packages'] = fcl_package.data 

        return  containers

    class Meta:
        model = Quote
        fields =['id','transport_modes','po_number','quote_no','shipment_terms','quote_status','created_at','pickup_location','is_submit_quote','fcl_container_details','quote_deadline','drop_location']


class QuoteGetSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Quote
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        

class QuoteUpdatePackageDetailsSerializers(DynamicFieldsMixin, serializers.ModelSerializer):

    """
        Serializer for Quote Listing updation
    """
    id =serializers.IntegerField(required=True)
    class Meta:
        model = PackageDetails
        fields = ['id','shipper_details','consignee_details']
        read_only_fields = ['id']

class ContainerSerializer(serializers.ModelSerializer):
    id =serializers.IntegerField(required=True)
    container_packages = QuoteUpdatePackageDetailsSerializers(many=True,required=False)

    class Meta:
        model = PackageDetails
        fields = ['id','shipper_details','consignee_details','container_packages']  
        read_only_fields = ['id']

    def validate(self,data):
        errors={}
        container_object= PackageDetails.objects.filter(id=data['id'],is_fcl_container=True,container__isnull=True)
        if container_object:
            container_subtype=container_object.values('container_subtype')[0]['container_subtype']
            if container_subtype == 'RF':
                    if not data.get('shipper_details'):
                        errors.update({'shipper_details': 'Shipper details is required.'})

            if container_subtype == 'Tank':
                    if not data.get('consignee_details'):
                        errors.update({'consignee_details': 'Consignee details is required.'})
        if errors:
            raise serializers.ValidationError(errors)
        return data

class QuoteListingUpdateSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    packages = QuoteUpdatePackageDetailsSerializers(many=True,required=False)
    container_details = ContainerSerializer(many=True,required=False)

    class Meta:
        model = Quote
        fields=['id','po_number','quote_deadline','container_details','packages']
        read_only_fields = ['id']


    
