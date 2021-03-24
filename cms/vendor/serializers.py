from address.models.address import Address
from branch.models.branch import Branch
from branch.serializers import BranchSerializer
from country.models.country import Country
from country.serializers import CountrySerializer
from django.core.serializers import serialize
from state.serializers import StateSerializer
from city.serializers import CitySerializer
from branch.serializers import BranchSerializer
from company.models.company import Company
from company.serializers import CompanySerializer
from currency.models.currency_profile import CurrencyProfile
from datetime import datetime
from django.conf import settings
from django_restql.mixins import DynamicFieldsMixin
from notification.managers.email_manager import EmailNotification
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from vendor.models.vendor import Vendor, VendorType
from vendor.models.vendor_companies_mode import VendorCompaniesMode
from address.serializers import AddressBaseSerializer
from utils.helpers import Diff, generate_token_data
import json


class VendorSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Vendor
        extra_kwargs = {'password': {'write_only': True}}
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']


class VendorDetailSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    branch = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    home_company = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        extra_kwargs = {'password': {'write_only': True}}
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']


    def get_branch(self, obj):

        result_list = []

        vendor_branch_data = BranchSerializer(obj.branch.all().order_by('id'), many=True, read_only=True,
                                 fields=('id', 'name')).data

        vendor_branch_ids = [i['id'] for i in vendor_branch_data]
        
        def get_children_data(branch_id):
            branch_dict = {}
            branch_obj = BranchSerializer(Branch.objects.get(id=branch_id, status=Branch.ACTIVE), fields=('id', 'name')).data
            branch_dict.update(branch_obj)

            has_children = list(Branch.objects.filter(parent=branch_obj['id'], status=Branch.ACTIVE).values('id', 'name'))
            if has_children:
                child_list = []
                for child in has_children:
                    child_id = child['id']
                    child_result = get_children_data(child_id)
                    child_list.append(child_result)
                branch_dict.update({'children': child_list})

            return branch_dict


        for branch_data in vendor_branch_ids:
            result = get_children_data(branch_data)
            result_list.append(result)

        return result_list

    def get_company(self, obj):
        return CompanySerializer(obj.company.all().order_by('id'), many=True, read_only=True,
                                 fields=('id', 'name')).data

    def get_home_company(self, obj):
        return {'id': obj.home_company.id, 'name': obj.home_company.name}


class VendorTypeSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = VendorType
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']


class VendorCompaniesModeSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = VendorCompaniesMode
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']


class VendorDetailsSerializer(serializers.ModelSerializer):
    """
        Serializer for Vendor registration details.
    """
    REQUIRED_TOGETHER_FIELDS = [('contact_no_dial_code', 'contact_no'),
                                ('landline_no_dial_code', 'landline_no')]

    company_name = serializers.CharField(max_length=255)

    class Meta:
        model = Vendor
        fields = ['name', 'email', 'secondary_email', 'contact_no_dial_code', 'contact_no', 'landline_no_dial_code',
                  'landline_no', 'vendor_type', 'company_name', 'designation', 'password', 'home_company']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, 'allow_blank': False, 'allow_null': False},
            'home_company': {'required': False, 'allow_null': True}
        }

    def validate_company_name(self, data):
        if Company.objects.filter(user_type='vendor', name__iexact=data).exists():
            raise serializers.ValidationError('Company already exists. Please contact admin.')
        return data

    def validate(self, data):
        errors = {}
        for field1, field2 in self.REQUIRED_TOGETHER_FIELDS:
            msg = 'This field is required.'
            if data.get(field1) and not data.get(field2):
                errors.update({field2: msg})
            elif not data.get(field1) and data.get(field2):
                errors.update({field1: msg})

        if not data.get('contact_no') and not data.get('landline_no'):
            msg = 'Please fill either Mobile Number or Landline Number.'
            errors.update({'contact_no': msg, 'landline_no': msg})
        if errors:
            raise serializers.ValidationError(errors)
        return data


class VendorRegistrationSerializer(serializers.Serializer):
    """
        Serializer for Vendor registration.
    """
    vendor_details = VendorDetailsSerializer()
    address_details = AddressBaseSerializer()


class VendorCompaniesUpdateSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), error_messages={"does_not_exist":
                                                                                                     "Invalid company "
                                                                                                     "id"})

    class Meta:
        model = CurrencyProfile
        fields = ['id', 'entity_type', 'entity_id', 'air_currency', 'lcl_currency', 'fcl_currency',
                  'company']
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
            'entity_type': {'required': False},
            'entity_id': {'required': False},
            'air_currency': {'required': True, 'allow_null': False, 'allow_blank': False},
            'lcl_currency': {'required': True, 'allow_null': False, 'allow_blank': False},
            'fcl_currency': {'required': True, 'allow_null': False, 'allow_blank': False}
        }


class VendorCompanyModeUpdateSerializer(serializers.ModelSerializer):
    vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all(), required=False)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), error_messages={"does_not_exist":
                                                                                                     "Invalid company "
                                                                                                     "id"})

    class Meta:
        model = VendorCompaniesMode
        fields = ['id', 'vendor', 'company', 'mode']
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
            'vendor': {'required': False}
        }


class VendorUpdateSerializer(serializers.ModelSerializer):
    REQUIRED_TOGETHER_FIELDS = [('contact_no_dial_code', 'contact_no'),
                                ('landline_no_dial_code', 'landline_no')]

    companies = VendorCompaniesUpdateSerializer(many=True)
    company_modes = VendorCompanyModeUpdateSerializer(many=True)
    branch = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Branch.objects,
                                                                            write_only=True,
                                                                            error_messages=
                                                                            {"does_not_exist": "Invalid branch id"}))
    supervisor = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Vendor.objects,
                                                                                write_only=True,
                                                                                error_messages=
                                                                                {
                                                                                    "does_not_exist": "Invalid "
                                                                                                      "supervisor "
                                                                                                      "id"}))

    class Meta:
        model = Vendor
        fields = ['id', 'name', 'email', 'secondary_email', 'contact_no_dial_code', 'contact_no',
                  'landline_no_dial_code', 'landline_no', 'company', 'designation', 'password',
                  'branch', 'supervisor', 'home_company', 'companies', 'company_modes']
        extra_kwargs = {
            'password': {'write_only': True},
            'company': {'required': False},
        }

    def validate(self, attrs):
        error_dict = {}

        for field1, field2 in self.REQUIRED_TOGETHER_FIELDS:
            msg = 'This field is required.'
            if attrs.get(field1) and not attrs.get(field2):
                error_dict.update({field2: msg})
            elif not attrs.get(field1) and attrs.get(field2):
                error_dict.update({field1: msg})

        if not attrs.get('contact_no') and not attrs.get('landline_no'):
            msg = 'Please fill either Mobile Number or Landline Number.'
            error_dict.update({'contact_no': msg, 'landline_no': msg})

        attrs['company'] = [i['company'] for i in attrs.get('companies', None)]

        company = attrs.get('company')
        if not company:
            error_dict.update({'company': 'This field is required'})

        # Validate Company List
        company_list_by_organization_id = Company.objects.filter(organization=self.context['organization_id'])
        for company in attrs['companies']:
            if company['company'] not in company_list_by_organization_id:
                error_dict.update({'company': 'Invalid company ID.'})

        # Validate Branch List
        branch_list_by_company_id = Branch.objects.filter(company=attrs['home_company'])
        for branch in attrs['branch']:
            if branch not in branch_list_by_company_id:
                error_dict.update({'branch': 'Invalid branch ID.'})

        # Validate Supervisor List
        if 'is_super_admin' not in attrs or not attrs['is_super_admin']:
            if 'supervisor' in attrs and attrs['supervisor']:

                supervisor_list_by_organization_id = Vendor.objects.filter(
                    company__organization=self.context['organization_id']).values_list('id', flat=True)

                for supervisor in attrs['supervisor']:
                    if supervisor.id not in supervisor_list_by_organization_id:
                        error_dict.update({'supervisor': 'Invalid supervisor ID.'})
            else:
                error_dict.update({'supervisor': 'Supervisor is required.'})

        # Validate Home Company
        if attrs['home_company'] not in company_list_by_organization_id:
            error_dict.update({'home_company': 'Invalid supervisor ID.'})

        if error_dict:
            raise serializers.ValidationError(error_dict)

        return attrs

    def create(self, validated_data):
        vendor_companies_data = validated_data.get('companies')
        vendor_company_modes_data = validated_data.get('company_modes')
        branch = validated_data.get('branch')
        supervisor = validated_data.get('supervisor')
        company = validated_data.get('company')

        validated_data.pop('companies', None)
        validated_data.pop('company_modes', None)
        validated_data.pop('branch', None)
        validated_data.pop('supervisor', None)
        validated_data.pop('company', None)

        token_hash, token = generate_token_data(validated_data.get('email'), 'vendor')
        validated_data['registration_token'] = token
        validated_data['token_date'] = datetime.now()

        vendor_obj = Vendor.objects.create(**validated_data)
        vendor_obj.branch.set(branch)
        vendor_obj.supervisor.set(supervisor)
        vendor_obj.company.set(company)

        for vendor_company in vendor_companies_data:
            vendor_company['entity_type'] = "vendor"
            vendor_company['entity_id'] = vendor_obj.id
            CurrencyProfile.objects.create(**vendor_company)

        for vendor_company_mode in vendor_company_modes_data:
            vendor_company_mode.update({'vendor': vendor_obj})
            VendorCompaniesMode.objects.create(**vendor_company_mode)

        link = settings.FRONTEND_URL + '/set-profile/' + token_hash
        email_data = {
            'customer_name': validated_data.get('name'),
            'customer_email': validated_data.get('email'),
            'link': link,
        }
        EmailNotification.set_profile_email(email_data)

        return vendor_obj

    def update(self, instance, validated_data):
        vendor_companies_data = validated_data.get('companies')
        vendor_company_modes_data = validated_data.get('company_modes')
        company = [i.id for i in validated_data.get('company')]

        currency_company_ids = CurrencyProfile.objects.filter(
            entity_type='customer', entity_id=instance.id).values_list('company', flat=True)
        company_mode_ids = VendorCompaniesMode.objects.filter(vendor=instance.id).values_list('company', flat=True)

        deleted_currency_profile_ids = Diff(currency_company_ids, company)
        deleted_currency_mode_ids = Diff(company_mode_ids, company)

        for vendor_company in deleted_currency_profile_ids:
            CurrencyProfile.objects.filter(entity_type='vendor', entity_id=instance.id, company=vendor_company) \
                .delete()

        for vendor_company_mode in deleted_currency_mode_ids:
            VendorCompaniesMode.objects.filter(vendor=instance.id, company=vendor_company_mode).delete()

        for vendor_company in vendor_companies_data:
            vendor_company.update({'entity_type': 'vendor', 'entity_id': instance.id})
            if 'id' in vendor_company:
                CurrencyProfile.objects.filter(id=vendor_company['id']).update(**vendor_company)
            else:
                CurrencyProfile.objects.create(**vendor_company)

        for vendor_company_mode in vendor_company_modes_data:
            vendor_company_mode.update({'vendor': instance})
            if 'id' in vendor_company_mode:
                VendorCompaniesMode.objects.filter(id=vendor_company_mode['id']).update(**vendor_company_mode)
            else:
                VendorCompaniesMode.objects.create(**vendor_company_mode)

        validated_data.pop('companies', None)
        validated_data.pop('company_modes', None)

        return super(VendorUpdateSerializer, self).update(instance, validated_data)
