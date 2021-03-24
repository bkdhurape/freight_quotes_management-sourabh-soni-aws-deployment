from branch.models import Branch , BranchTransportMode
from commodity.models.commodity import Commodity
from country.models.country import Country
from state.models.state import State
from city.models.city import City
from region.models.region import Region
from django.apps import apps
from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from utils.base_models import StatusBase
from vendor.models.vendor import Vendor
import pint
ureg = pint.UnitRegistry()


class BranchSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Branch
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']
    
class BranchTransportModeSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = BranchTransportMode
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']

    
class BranchBaseSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    
    class Meta:
        model = Branch
        fields = ['name','country','state','city','region', 'minimum_weight','parent',
                  'maximum_weight', 'weight_unit', 'minimum_radius', 'maximum_radius', 'radius_unit', 'company']
        read_only_fields = ['id']

        extra_kwargs = {
            'country': {'error_messages': {'does_not_exist': 'Invalid country.'}},
            'state': {'error_messages': {'does_not_exist': 'Invalid state.'}},
            'city': {'error_messages': {'does_not_exist': 'Invalid city.'}},
            'region': {'error_messages': {'does_not_exist': 'Invalid region.'}}
        }

        validators = [UniqueTogetherValidator(queryset=Branch.objects.all(), fields=[
                                              'company', 'name'], message='The branch name already exists for this company')]

    def validate(self, data): 

        if data['name'] != 'HQ':

            vendor_type = list(Vendor.find_by(
                multi=True, home_company_id=data['company'], status=Vendor.ACTIVE).values_list('vendor_type', flat=True))[0]

            if vendor_type == 'transport_only':
                
                # Required field weight and radius validation function
                self.weight_and_radius_validations(data)

                # Unit conversion function of weight and radius
                self.weight_and_radius_unit_conversion(data)
            
            else:
                data['minimum_weight']=None
                data['maximum_weight']=None
                data['minimum_weight_kg']=None
                data['maximum_weight_kg']=None
                data['weight_unit']=None
                data['minimum_radius']=None
                data['maximum_radius']=None
                data['minimum_radius_km']=None
                data['maximum_radius_km']=None
                data['radius_unit']=None
            
        return data

    def weight_and_radius_validations(self, data):

        errors = {}

        if('minimum_weight' not in data or not data['minimum_weight']):
            errors.update({'minimum_weight':'minimum_weight is required'})

        if('maximum_weight' not in data or not data['maximum_weight']):
            errors.update({'maximum_weight':'maximum_weight is required'})

        if (('minimum_weight' in data and data['minimum_weight']) and ('weight_unit' not in data or not data['weight_unit'])):
            errors.update({'weight_unit':'weight_unit is required'})
        
        if (('maximum_weight' in data and data['maximum_weight']) and ('weight_unit' not in data or not data['weight_unit'])):
            errors.update({'weight_unit':'weight_unit is required'})

        if (('minimum_weight' in data and data['minimum_weight']) >= ('maximum_weight' in data and data['maximum_weight'])):
            errors.update({'maximum_weight':'maximum_weight should be more than minimum weight'})

        if('minimum_radius' not in data or not data['minimum_radius']):
            errors.update({'minimum_radius':'minimum_radius is required'})

        if('maximum_radius' not in data or not data['maximum_radius']):
            errors.update({'maximum_radius':'maximum_radius is required'})

        if (('minimum_radius' in data and data['minimum_radius']) and ('radius_unit' not in data or not data['radius_unit'])):
            errors.update({'radius_unit':'radius_unit is required'})       

        if (('maximum_radius' in data and data['maximum_radius']) and ('radius_unit' not in data or not data['radius_unit'])):
            errors.update({'radius_unit':'radius_unit is required'})

        if (('minimum_radius' in data and data['minimum_radius']) >= ('maximum_radius' in data and data['maximum_radius'])):
            errors.update({'maximum_radius':'maximum_radius should be greater than minimum_radius is'})

        if errors:
            raise serializers.ValidationError(errors)
        return data


    def weight_and_radius_unit_conversion(self, data):

        # Converting minimum weight to kg
        minimum_weight = ureg(str(data['minimum_weight'])+data['weight_unit'])
        minimum_weight_to_kg = minimum_weight.to('kg')
        new_minimum_weight_kg = round((minimum_weight_to_kg.magnitude),3)                
        data['minimum_weight_kg'] = new_minimum_weight_kg

        # Converting maximum weight to kg
        maximum_weight = ureg(str(data['maximum_weight'])+data['weight_unit'])
        maximum_weight_to_kg = maximum_weight.to('kg')
        new_maximum_weight_kg = round((maximum_weight_to_kg.magnitude),3)
        data['maximum_weight_kg'] = new_maximum_weight_kg 

        # Converting minimum radius to km
        minimum_radius = ureg(str(data['minimum_radius'])+data['radius_unit'])
        minimum_radius_to_km = minimum_radius.to('km')
        new_minimum_radius_km = round((minimum_radius_to_km.magnitude),3)
        data['minimum_radius_km'] = new_minimum_radius_km

        # Converting maximum radius to km
        maximum_radius = ureg(str(data['maximum_radius'])+data['radius_unit'])
        maximum_radius_to_km = maximum_radius.to('km')
        new_maximum_radius_km = round((maximum_radius_to_km.magnitude),3)              
        data['maximum_radius_km'] = new_maximum_radius_km


class BranchDeleteSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    branch_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Branch
        fields = ['branch_id','company']
    

    def validate(self, data):     
       
        branch_data = list(Branch.objects.filter(status=StatusBase.ACTIVE, company=data['company'], id=data['branch_id']).values_list('is_head_branch', 'parent'))[0]
        is_head_branch , parent_id = branch_data

        list_error = []

        if is_head_branch == True:
            list_error.append("You can not delete head branch")

        vendor_data = Vendor.objects.filter(branch=data['branch_id'], status=StatusBase.ACTIVE)

        if vendor_data.count() and is_head_branch == False:
            list_error.append("You cant not delete branch as it has users")
        
        data['parent_id'] = parent_id

        if list_error:
            raise serializers.ValidationError(list_error)
        return data


class BranchTransportModeBaseSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    commodity = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Commodity.objects,
                                                                               write_only=True, error_messages=
                                                                            {"does_not_exist": "Invalid commodity ID"}))
    
    from_trade_lanes = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Country.objects,
                                                                               write_only=True, error_messages=
                                                                            {"does_not_exist": "Invalid ID"}), required=False)

    to_trade_lanes = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Country.objects,
                                                                               write_only=True, error_messages=
                                                                            {"does_not_exist": "Invalid ID"}), required=False)

    trade_lanes = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Country.objects,
                                                                               write_only=True, error_messages=
                                                                            {"does_not_exist": "Invalid ID"}), required=False)

    class Meta:
        model = BranchTransportMode
        fields = ['transport_mode','container_type', 'hazardous', 'instant_quotes', 'trade_lanes', 'from_trade_lanes',
                  'to_trade_lanes', 'commodity', 'branch']
        read_only_fields = ['id']

        validators = [UniqueTogetherValidator(queryset=BranchTransportMode.objects.all(), fields=[
                                              'branch', 'transport_mode'], message='This transport_mode already exists for this branch')]


    def validate(self, data):

        errors = {}
        
        # For FCL container type should not be blank
        if data['transport_mode'] in ['FCLI', 'FCLE', 'FCLTC']: 
            if ('container_type' not in data or not data['container_type']):
                errors.update({'container_type':'Container type is required for FCL'})
        else:
            data['container_type'] = []

        # For Third country from_trade_lanes and to_trade_lanes are required
        if data['transport_mode'] in ['ATC', 'FCLTC', 'LCLTC']:
            if 'from_trade_lanes' not in data or not data['from_trade_lanes']:
                errors.update({'from_trade_lanes':'This field is required for Third Country'})
            if 'to_trade_lanes' not in data or not data['to_trade_lanes']:
                errors.update({'to_trade_lanes':'This field is required for Third Country'})
            else:
                data['trade_lanes'] = []
           

        # For Air, FCL and LCL trade_lanes is required
        if data['transport_mode'] in ['AI', 'AE', 'FCLI', 'FCLE', 'LCLI', 'LCLE']:
            if ('trade_lanes' not in data or not data['trade_lanes']):
                errors.update({'trade_lanes':'This field is required for all modes of Import and Export'})
            else:
                data['from_trade_lanes'] = []
                data['to_trade_lanes'] = []

        if errors:
            raise serializers.ValidationError(errors)
        return data


class BranchUpdateSerializer(BranchBaseSerializer):

    class Meta(BranchBaseSerializer.Meta):
        model = Branch

    def validate(self, data):

        vendor_type = list(Vendor.find_by(
                multi=True, home_company_id=data['company'], status=Vendor.ACTIVE).values_list('vendor_type', flat=True))[0]

        if vendor_type == 'transport_only':
            
            # Required field weight and radius validation function
            self.weight_and_radius_validations(data)

            # Unit conversion function of weight and radius
            self.weight_and_radius_unit_conversion(data)
        
        else:
            data['minimum_weight']=None
            data['maximum_weight']=None
            data['minimum_weight_kg']=None
            data['maximum_weight_kg']=None
            data['weight_unit']=None
            data['minimum_radius']=None
            data['maximum_radius']=None
            data['minimum_radius_km']=None
            data['maximum_radius_km']=None
            data['radius_unit']=None

        return data