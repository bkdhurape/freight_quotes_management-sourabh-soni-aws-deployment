from django_restql.mixins import DynamicFieldsMixin
from enquiry_management.models.company_expertise import CompanyExpertise
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from commodity.models.commodity import Commodity
from country.models.country import Country
from vendor.models.vendor import Vendor



class CompanyExpertiseSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model=CompanyExpertise
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']

class CompanyExpertiseBaseSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    vendor_type = serializers.ChoiceField(write_only=True, choices=Vendor.VENDOR_TYPE_CHOICES)
    commodity = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Commodity.objects,
                                                                               write_only=True, error_messages=
                                                                            {"does_not_exist": "Invalid commodity ID"}))
    
    from_trade_lanes = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Country.objects,
                                                                               write_only=True, error_messages=
                                                                            {"does_not_exist": "Invalid Country ID"}), required=False)

    to_trade_lanes = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Country.objects,
                                                                               write_only=True, error_messages=
                                                                            {"does_not_exist": "Invalid  Country ID"}), required=False)

    trade_lanes = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Country.objects,
                                                                               write_only=True, error_messages=
                                                                            {"does_not_exist": "Invalid Country ID"}), required=False)
    validators = [UniqueTogetherValidator(queryset=CompanyExpertise.objects.all(), fields=[
                                              'company', 'transport_mode'], message='This transport_mode already exists for this company')]


    class Meta:
        model = CompanyExpertise
        fields = ['transport_mode','container_type', 'hazardous', 'instant_quotes', 'trade_lanes', 'from_trade_lanes',
                  'to_trade_lanes', 'commodity', 'company','max_weight','weight_unit','temperature_controlled','vendor_type']
        read_only_fields = ['id']

    
    def validate(self, data):

        errors = {}
        if 'courier' not in data['vendor_type'] :
            data['max_weight'],data['weight_unit'] = None,None
        
        # For FCL container type should not be blank
        if data['transport_mode'] in ['FCLI', 'FCLE', 'FCLTC']: 
            data['temperature_controlled'] = None
            if ('container_type' not in data or not data['container_type']):
                errors.update({'container_type':'Container type is required for FCL'})
        else:
            data['container_type'] = []

        # For Third country from_trade_lanes and to_trade_lanes are required
        if data['transport_mode'] in ['ATC', 'ACTC', 'FCLTC', 'LCLTC']:
            data['trade_lanes'] = []
            if 'from_trade_lanes' not in data or not data['from_trade_lanes']:
                errors.update({'from_trade_lanes':'This field is required for Third Country'})
            if 'to_trade_lanes' not in data or not data['to_trade_lanes']:
                errors.update({'to_trade_lanes':'This field is required for Third Country'})
             
        # For Air, FCL and LCL trade_lanes is required
        if data['transport_mode'] in ['AI', 'AE','ACI', 'ACE', 'FCLI', 'FCLE', 'LCLI', 'LCLE']:
            if ('trade_lanes' not in data or not data['trade_lanes']):
                errors.update({'trade_lanes':'This field is required for all modes of Import and Export'})
            else:
                data['from_trade_lanes'] = []
                data['to_trade_lanes'] = []

        #  set default value true for air,air Courier,lcl import/export/third_country ,if some one set null from backend for hacking purpose
        if data['transport_mode'] in ['AI', 'AE', 'ATC', 'ACE', 'ACI', 'ACTC', 'LCLI', 'LCLE', 'LCLTC'] and ('temperature_controlled' in data and (data.get('temperature_controlled')=="" or data.get('temperature_controlled') is None)):
            errors.update({'temperature_controlled':'This fields is required'})

        data.pop('vendor_type', None)
        if errors:
            raise serializers.ValidationError(errors)
        return data

