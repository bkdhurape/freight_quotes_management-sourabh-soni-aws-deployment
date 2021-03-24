from company.serializers import CompanySerializer
from company.models.company_logistic_info import CompanyLogisticInfo
from company.models.company import Company
from country.models.country import Country
from currency.models.currency_profile import CurrencyProfile
from currency.serializers import CustomerCompaniesCurrencySerializer
from datetime import datetime
from department.models.department import Department
from address.models.address import Address
from customer.models.customer import Customer
from customer.models.invited_vendor import InvitedVendor
from department.serializers import DepartmentSerializer
from django.conf import settings
from django_restql.mixins import DynamicFieldsMixin
from notification.managers.email_manager import EmailNotification
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from company.serializers import PDFBase64File, CompanyValidationSerializer
from utils.helpers import Diff, generate_token_data, encode_data
from vendor.models.vendor import Vendor
from utils.base_models import StatusBase
from django.core.validators import RegexValidator


class CustomerSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    REQUIRED_TOGETHER_FIELDS = [('contact_no_dial_code', 'contact_no'),
                                ('landline_no_dial_code', 'landline_no')]

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'secondary_email', 'contact_no_dial_code', 'contact_no',
                  'landline_no_dial_code', 'landline_no',
                  'customer_type', 'customer_type_other', 'company', 'password', 'designation', 'registration_token',
                  'token_date',
                  'department', 'supervisor', 'home_country', 'home_company', 'client', 'is_super_admin', 'status','profile_picture']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CustomerCreateUpdateSerializer(CustomerSerializer):
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

        # Validate Company List
        company_list_by_organization_id = Company.objects.filter(organization=self.context['organization_id'])
        for company in attrs['company']:
            if company not in company_list_by_organization_id:
                error_dict.update({'company': 'Invalid company ID.'})

        # Validate Department List
        department_list_by_company_id = Department.objects.filter(company=attrs['home_company'])
        for department in attrs['department']:
            if department not in department_list_by_company_id:
                error_dict.update({'department': 'Invalid department ID.'})

        # Validate Supervisor List
        if 'is_super_admin' not in attrs or not attrs['is_super_admin']:
            if attrs['supervisor']:

                supervisor_list_by_organization_id = Customer.objects.filter(
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


class CustomerInfoSerializer(serializers.ModelSerializer):
    """
        Serializer for Customer registration details.
    """
    REQUIRED_TOGETHER_FIELDS = [('contact_no_dial_code', 'contact_no'),
                                ('landline_no_dial_code', 'landline_no')]

    email = serializers.EmailField(max_length=254,
                                   validators=[UniqueValidator(queryset=Customer.objects.all(),
                                                               lookup='iexact',
                                                               message='Customer with this email already exists.')],
                                   error_messages={'required': 'Customer email required.'})
    company_name = serializers.CharField(min_length=4,max_length=255, validators=[RegexValidator(regex='^[A-Za-z]+[A-Za-z\d\._\s]+$')])


    class Meta:
        model = Customer
        fields = ['name', 'email', 'secondary_email', 'contact_no_dial_code', 'contact_no', 'landline_no_dial_code',
                  'landline_no', 'customer_type', 'customer_type_other', 'company_name', 'designation', 'password',
                  'home_country']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, 'allow_blank': False, 'allow_null': False},
            'customer_type': {'required': True, 'allow_null': False, 'allow_blank': False}
        }

    def validate_company_name(self, data):
        if Company.objects.filter(user_type='customer', name__iexact=data).exists():
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


class AddressInputSerializer(serializers.ModelSerializer):
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


class CompanyInfoSerializer(serializers.ModelSerializer):
    """
        Serializer for company info.
    """
    customer_type = serializers.ChoiceField(write_only=True, choices=Customer.CUSTOMER_TYPE_CHOICES)
    home_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects,
                                                      write_only=True)
    pan_document = PDFBase64File(required = False, allow_null=True)
    gst_document = PDFBase64File(required = False, allow_null=True)
    cin_document = PDFBase64File(required = False, allow_null=True)
    iec_document = PDFBase64File(required = False, allow_null=True)
    business_activity = serializers.ListField(child=serializers.CharField(),
                                              allow_empty=False,
                                              error_messages={"empty": "Business activity value is required.",
                                                              'required': "Business activity value is required."})
    industry = serializers.ListField(child=serializers.CharField(),
                                     allow_empty=False,
                                     error_messages={"empty": "Industry value is required.",
                                                     'required': "Industry value is required."})

    class Meta:
        model = Company
        fields = ('company_type', 'industry', 'industry_other', 'business_activity', 'business_activity_other',
                  'iec', 'gst', 'pan', 'cin', 'home_country', 'customer_type','iec_document', 'gst_document', 'pan_document', 'cin_document')

    def validate(self, data):
        country = data.get('home_country')
        errors = {}
        CompanyValidationSerializer.validate_company_details(country, data, errors)
        if 'other' in data.get('industry', []) and not data.get('industry_other'):
            errors.update({'industry_other': 'This is required.'})
        if 'other' in data.get('business_activity', []) and not data.get('business_activity_other'):
            errors.update({'business_activity_other': 'This is required.'})
        if errors:
            raise serializers.ValidationError(errors)
        data.pop('customer_type', None)
        data.pop('home_country', None)
        return data


class CompanyDetailsSerializer(serializers.Serializer):
    """
        Company section serializer with address details.
    """
    company_info = CompanyInfoSerializer()
    address_details = AddressInputSerializer()


class CurrencyProfileSerializer(serializers.ModelSerializer):
    """
        Serializer for currency profile.
    """

    class Meta:
        model = CurrencyProfile
        fields = ['air_currency', 'lcl_currency', 'fcl_currency']


class CompanyLogisticInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyLogisticInfo
        fields = ['annaul_logistic_spend_currency',
                  'annual_logistic_spend',
                  'annual_air_shipments',
                  'annual_lcl_shipments',
                  'annual_fcl_shipments',
                  'total_shipments',
                  'annual_air_volume',
                  'annual_lcl_volume',
                  'annual_fcl_volume'
                  ]

    def validate(self, data):
        if 'annaul_logistic_spend_currency' in data and not data.get('annaul_logistic_spend_currency'):
            raise serializers.ValidationError({'annaul_logistic_spend_currency': "This field is required"})
        return data


class AdditionalDetailsSerializer(serializers.Serializer):
    """
        Additional details section serializer.
    """
    company_logistics = CompanyLogisticInfoSerializer()
    currency_profile_details = CurrencyProfileSerializer()


class CustomerRegistrationSerializer(serializers.Serializer):
    """
        Serializer for Customer registration.
    """
    customer_details = CustomerInfoSerializer()
    company_details = CompanyDetailsSerializer(required=False)
    additional_details = AdditionalDetailsSerializer(required=False)

    def validate(self, data):
        if (data.get('company_details') and not data.get('additional_details')) or \
                (data.get('additional_details') and not data.get('company_details')):
            raise serializers.ValidationError('Both company_details and additional_details section data is required if '
                                              'you pass one of the section along with customer_details.')
        return data


class CustomerDetailSerializer(CustomerSerializer):
    company = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    supervisor = serializers.SerializerMethodField()
    home_country = serializers.SerializerMethodField()
    home_company = serializers.SerializerMethodField()

    def get_company(self, obj):
        return CompanySerializer(obj.company.all().order_by('id'), many=True, read_only=True,
                                 fields=('id', 'name')).data

    def get_department(self, obj):
        return DepartmentSerializer(obj.department.all().order_by('id'), many=True, read_only=True,
                                    fields=('id', 'name')).data

    def get_supervisor(self, obj):
        return CustomerSerializer(obj.supervisor.all().order_by('id'), many=True, read_only=True,
                                  fields=('id', 'name')).data

    def get_home_country(self, obj):
        return {'id': obj.home_country.id, 'name': obj.home_country.name}

    def get_home_company(self, obj):
        return {'id': obj.home_company.id, 'name': obj.home_company.name}


class InvitedVendorSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    REQUIRED_TOGETHER_FIELDS = [('contact_no_dial_code', 'contact_no'),
                                ('landline_no_dial_code', 'landline_no')]

    class Meta:
        model = InvitedVendor
        fields = ['id', 'name', 'email', 'contact_no_dial_code', 'contact_no', 'landline_no_dial_code', 'landline_no',
                  'company_name', 'customer_company', 'customer', 'vendor_company', 'vendor', 'status']
        read_only_fields = ['id']

    def validate(self, attrs):
        error_dict = {}

        name = attrs.get('name', None)
        email = attrs.get('email', None)
        if not name:
            error_dict.update({'name': 'Name is required'})

        if not email:
            error_dict.update({'email': 'Email is required'})

        for field1, field2 in self.REQUIRED_TOGETHER_FIELDS:
            msg = 'This field is required.'
            if attrs.get(field1) and not attrs.get(field2):
                error_dict.update({field2: msg})
            elif not attrs.get(field1) and attrs.get(field2):
                error_dict.update({field1: msg})

        if not attrs.get('contact_no') and not attrs.get('landline_no'):
            msg = 'Please fill either Mobile Number or Landline Number.'
            error_dict.update({'contact_no': msg, 'landline_no': msg})

        if error_dict:
            raise serializers.ValidationError(error_dict)

        return attrs

    def create(self, validated_data):

        company_name = validated_data.get('company_name', None)
        company = Company.objects.filter(name=company_name, user_type='vendor').first()

        customer_company = validated_data.get('customer_company')
        customer_company_name = Company.objects.get(id=customer_company.id).name

        if company:
            validated_data['vendor_company'] = company

            vendor = Vendor.objects.filter(email=validated_data['email'], home_company=company.id).first()
            if vendor:
                validated_data['vendor'] = vendor
                invited_vendor_obj = InvitedVendor.objects.create(**validated_data)
            else:
                vendor = Vendor.objects.filter(is_super_admin=True, home_company=company.id).first()
                validated_data['vendor'] = vendor if vendor else None
                invited_vendor_obj = InvitedVendor.objects.create(**validated_data)

                validated_data.pop('customer')
                validated_data.pop('customer_company')
                validated_data.pop('vendor_company')
                validated_data.pop('vendor')

                email_data = {
                    'vendor_super_admin_name': vendor.name,
                    'vendor_super_admin_email': vendor.email,
                    'name': validated_data.get('name'),
                    'email': validated_data.get('email'),
                    'company_name': validated_data.get('company_name'),
                    'customer_company_name': customer_company_name
                }

                if validated_data.get('contact_no') and validated_data.get('contact_no_dial_code'):
                    email_data.update({'dial_code': validated_data.get('contact_no_dial_code'),
                                       'contact_no': validated_data.get('contact_no')})

                if validated_data.get('landline_no') and validated_data.get('landline_no_dial_code'):
                    email_data.update({'dial_code': validated_data.get('landline_no_dial_code'),
                                       'contact_no': validated_data.get('landline_no')})

                EmailNotification.invite_vendor(email_data)

        else:
            invited_vendor_obj = InvitedVendor.objects.create(**validated_data)
            data = str(invited_vendor_obj.id) + '__' + \
                validated_data['company_name'] + '__' + validated_data['email']
            encoded_data = encode_data(data)
            invitation_link = settings.API_HOST + '/api/v1/vendor/' + encoded_data

            email_data = {
                'name': validated_data.get('name'),
                'email': validated_data.get('email'),
                'customer_company_name': customer_company_name,
                'invitation_link': invitation_link
            }

            EmailNotification.invite_vendor_with_link(email_data)

        return invited_vendor_obj


class InvitedVendorUpdateSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    action = serializers.CharField(max_length=50)
    vendor_company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=True,
                                                  error_messages={"does_not_exist": "Invalid company id"})
    vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all(), required=True,
                                            error_messages={"does_not_exist": "Invalid vendor id"})

    class Meta:
        model = InvitedVendor
        fields = ['id', 'status', 'vendor_company', 'vendor', 'action']
        read_only_fields = ['id']

    def validate(self, attrs):
        error_dict = {}

        vendor = attrs.get('vendor')
        vendor_company = attrs.get('vendor_company')

        action = attrs.get('action')
        if action not in ['accept', 'reject']:
            error_dict.update({'action': 'You can either ACCEPT or REJECT client'})

        else:
            vendor = Vendor.objects.filter(id=vendor.id, home_company_id=vendor_company.id, is_super_admin=True)

            invited_vendor = InvitedVendor.objects.get(id=attrs.get('id'))
            if invited_vendor and not vendor and invited_vendor['vendor_id'] != vendor.id:
                error_dict.update({'action': 'You cannot ACCEPT or REJECT this client.'})

        if error_dict:
            raise serializers.ValidationError(error_dict)

        return attrs

    def update(self, instance, validated_data):
        validated_data['status'] = InvitedVendor.ACTIVE if validated_data.get('action') == 'accept' \
            else InvitedVendor.REJECT
        return super(InvitedVendorUpdateSerializer, self).update(instance, validated_data)


class DeleteInvitedVendorSerializer(DynamicFieldsMixin, serializers.Serializer):
    company = serializers.IntegerField(write_only=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=True,
                                                  error_messages={"does_not_exist": "Invalid customer id"})
    id = serializers.PrimaryKeyRelatedField(queryset=InvitedVendor.objects.all(), required=True,
                                            error_messages={"does_not_exist": "Vendor customer id"})

    class Meta:
        model = InvitedVendor
        fields = ['id', 'customer', 'company']

    def validate(self, attrs):
        customer_obj = attrs.get('customer', None)
        customer = Customer.objects.filter(id=customer_obj.id, home_company=attrs.get('company')).first()
        invited_vendor_obj = attrs.get('id')
        invite_vendor = InvitedVendor.objects.get(id=invited_vendor_obj.id)

        if not customer.is_super_admin and invite_vendor.customer.id != customer_obj.id:
            raise serializers.ValidationError('Only customer who invited this vendor and super admin of this company '
                                              'can remove this vendor')

        return attrs


# class AddCustomerDetailSerializer(CustomerSerializer):
#     supervisor = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), many=True, required=True)
#
#     def validate(self, attrs):
#         print('---AddCustomerDetailSerializer---attrs---', attrs)
#         if not attrs['supervisor']:
#             raise serializers.ValidationError({'supervisor': 'Supervisor is required.'})

class CompaniesSerializer(serializers.Serializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    currency_details = CustomerCompaniesCurrencySerializer()


class CustomerCompaniesUpdateSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

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


class AddCustomerSerializer(serializers.Serializer):
    customer_details = CustomerCreateUpdateSerializer()
    companies = CompaniesSerializer(many=True)


class CustomerUpdateSerializer(DynamicFieldsMixin,serializers.ModelSerializer):
    REQUIRED_TOGETHER_FIELDS = [('contact_no_dial_code', 'contact_no'),
                                ('landline_no_dial_code', 'landline_no')]

    companies = CustomerCompaniesUpdateSerializer(many=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'secondary_email', 'contact_no_dial_code', 'contact_no',
                  'landline_no_dial_code', 'landline_no', 'customer_type', 'customer_type_other', 'company',
                  'password', 'designation', 'registration_token', 'token_date', 'department', 'supervisor',
                  'home_country', 'home_company', 'client', 'is_super_admin', 'status', 'companies']
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
        company_list_by_organization_id = Company.objects.filter(
            organization=self.context['organization_id'])
        for company in attrs['companies']:
            if company['company'] not in company_list_by_organization_id:
                error_dict.update({'company': 'Invalid company ID.'})

        # Validate Department List
        department_list_by_company_id = Department.objects.filter(company=attrs['home_company'])
        for department in attrs['department']:
            if department not in department_list_by_company_id:
                error_dict.update({'department': 'Invalid department ID.'})

        # Validate supervisor
        if self.context.get('id'):
            self.is_super_admin_data = list(Customer.objects.filter(
                company=attrs['home_company'],id=self.context['id'], status=StatusBase.ACTIVE).values_list('is_super_admin', flat=True))[0]
            if self.is_super_admin_data == True:
                attrs['supervisor'] = []

        if (self.context.get('id') and self.is_super_admin_data == False) or attrs.get('is_super_admin') == False:
            if 'supervisor' in attrs and attrs['supervisor']:
                supervisor_list_by_organization_id = Customer.objects.filter(
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
        customer_companies_data = validated_data.get('companies')
        department = validated_data.get('department')
        supervisor = validated_data.get('supervisor')
        company = validated_data.get('company')

        validated_data.pop('companies', None)
        validated_data.pop('department', None)
        validated_data.pop('supervisor', None)
        validated_data.pop('company', None)

        token_hash, token = generate_token_data(validated_data.get('email'), 'customer')
        validated_data['registration_token'] = token
        validated_data['token_date'] = datetime.now()

        customer_obj = Customer.objects.create(**validated_data)
        customer_obj.department.set(department)
        customer_obj.supervisor.set(supervisor)
        customer_obj.company.set(company)

        for customer_company in customer_companies_data:
            customer_company['entity_type'] = "customer"
            customer_company['entity_id'] = customer_obj.id
            CurrencyProfile.objects.create(**customer_company)

        link = settings.FRONTEND_URL + '/set-profile/' + token_hash
        email_data = {
            'customer_name': validated_data.get('name'),
            'customer_email': validated_data.get('email'),
            'link': link,
        }
        EmailNotification.set_profile_email(email_data)

        return customer_obj

    def update(self, instance, validated_data):
        customer_companies_data = validated_data.get('companies')
        company = [i.id for i in validated_data.get('company')]

        currency_company_ids = CurrencyProfile.objects.filter(
            entity_type='customer', entity_id=instance.id).values_list('company', flat=True)

        deleted_currency_profile_ids = Diff(currency_company_ids, company)

        for customer_company in deleted_currency_profile_ids:
            CurrencyProfile.objects.filter(entity_type='customer', entity_id=instance.id, company=customer_company) \
                .delete()

        for customer_company in customer_companies_data:
            customer_company['entity_type'] = "customer"
            customer_company['entity_id'] = instance.id
            if 'id' in customer_company:
                CurrencyProfile.objects.filter(id=customer_company['id']).update(**customer_company)
            else:
                CurrencyProfile.objects.create(**customer_company)

        validated_data.pop('companies', None)

        return super(CustomerUpdateSerializer, self).update(instance, validated_data)
