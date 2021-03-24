from address.serializers import AddressBaseSerializer
from company.models import Company, Organization, CompanyLogisticInfo
from country.models.country import Country
from currency.models.currency_profile import CurrencyProfile
from customer.models.customer import Customer
from django.core.exceptions import NON_FIELD_ERRORS
from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from utils.base_models import StatusBase
from drf_extra_fields.fields import Base64ImageField,Base64FileField
from django.core.exceptions import ValidationError
import io
import PyPDF2


class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ['pdf']

    def get_file_extension(self, filename, decoded_file):
        try:
            PyPDF2.PdfFileReader(io.BytesIO(decoded_file))
        except PyPDF2.utils.PdfReadError as e:
            raise serializers.ValidationError(e)
        else:
            return 'pdf'

class CompanyValidationSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    def validate_company_details(country, data, errors):
        if country:
            if country and country.code == "IN":
                cin, cin_document = data.get('cin'), data.get('cin_document')
                gst, gst_document = data.get('gst'), data.get('gst_document')
                pan, pan_document = data.get('pan'), data.get('pan_document')
                iec, iec_document = data.get('iec'), data.get('iec_document')
                customer_type = data.get('customer_type')

                # validate company details fields like cin,pan,gst,iec number
                if not cin:
                    errors.update({'cin': 'CIN is required.'})

                if not pan:
                    errors.update({'pan': 'PAN is required.'})

                if not gst:
                    errors.update({'gst': 'GST is required.'})

                if customer_type and customer_type == "importer_or_exporter" and not iec:
                    errors.update({'iec': 'IEC is required.'})

                # validate company details fields iec documents and their size
                if customer_type and customer_type == "importer_or_exporter" and not iec_document:
                    errors.update(
                        {'iec_document': 'IEC document is required.'})

                if customer_type and customer_type == "importer_or_exporter" and iec_document:
                    CompanyBaseSerializer.validate_files_size(
                        iec_document, 'iec_document', errors)

                # validate company details fields cin documents
                if not cin_document:
                    errors.update(
                        {'cin_document': 'CIN document is required.'})
                else:
                    CompanyBaseSerializer.validate_files_size(
                        cin_document, 'cin_document', errors)

                # validate company details fields gst documents
                if not gst_document:
                    errors.update(
                        {'gst_document': 'GST document is required.'})
                else:
                    CompanyBaseSerializer.validate_files_size(
                        gst_document, 'gst_document', errors)

                # validate company details fields pan documents
                if not pan_document:
                    errors.update(
                        {'pan_document': 'PAN document is required.'})
                else:
                    CompanyBaseSerializer.validate_files_size(
                        pan_document, 'pan_document', errors)

                # when user type is vendor or customer_type is not importer_or_exporter set iec and iec document null
                if customer_type and not customer_type == "importer_or_exporter":
                    data['iec'], data['iec_document'] = None, None

            else:
                data['cin'], data['cin_document'] = None, None
                data['gst'], data['gst_document'] = None, None
                data['pan'], data['pan_document'] = None, None
                data['iec'], data['iec_document'] = None, None

        if errors:
            return errors
        return data

class CompanyBaseSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    """
         Base Serializer for company info.
    """
    company_logo = Base64ImageField(required=False, allow_null=True)
    pan_document = PDFBase64File(required=False, allow_null=True)
    gst_document = PDFBase64File(required=False, allow_null=True)
    cin_document = PDFBase64File(required=False, allow_null=True)
    iec_document = PDFBase64File(required=False, allow_null=True)
    customer_type = serializers.ChoiceField(
        write_only=True, required=False, allow_null=True, choices=Customer.CUSTOMER_TYPE_CHOICES)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),
                                                 write_only=True)

    class Meta:
        model = Company
        fields = ('name', 'company_type', 'industry', 'industry_other', 'business_activity', 'business_activity_other',
                  'iec', 'gst', 'pan', 'cin', 'country', 'customer_type', 'organization', 'user_type', 'incorporation_year', 'company_logo', 'iec_document', 'gst_document', 'pan_document', 'cin_document')

        validators = [UniqueTogetherValidator(queryset=Company.objects.all(), fields=[
                                              'name', 'user_type'], message='Company with this name already exists')]

    def validate(self, data):
        errors = {}
        # Validate industry and business activity for customer
        if self.context.get('id'):
            self.user_type = list(Company.objects.filter(
                id=self.context['id'], status=StatusBase.ACTIVE).values_list('user_type', flat=True))[0]

        if data.get('user_type') == 'customer' or (self.context.get('id') and self.user_type == 'customer'):
            data['incorporation_year'] = None

            if 'customer_type' not in data or not data['customer_type']:
                errors.update(
                    {'customer_type': 'customer_type is required for customer'})

            if 'industry' not in data or not data.get('industry'):
                errors.update(
                    {'industry': 'This field is required for customer'})

            if 'business_activity' not in data or not data.get('business_activity'):
                errors.update(
                    {'business_activity': 'This field is required for customer'})

            if 'other' in data.get('industry', []) and not data.get('industry_other'):
                errors.update({'industry_other': 'This is required.'})

            if 'other' not in data.get('industry', []):
                data['industry_other'] = None

            if 'other' in data.get('business_activity', []) and not data.get('business_activity_other'):
                errors.update({'business_activity_other': 'This is required.'})

            if 'other' not in data.get('business_activity', []):
                data['business_activity_other'] = None

        # validate company logo size
        if data.get('company_logo'):
            CompanyBaseSerializer.validate_files_size(
                data.get('company_logo'), 'company_logo', errors)

        # Set below fields to null as it is not required for vendor
        if data.get('user_type') == 'vendor' or (self.context.get('id') and self.user_type == 'vendor'):
            data['industry'] = []
            data['industry_other'] = None
            data['business_activity'] = []
            data['business_activity_other'] = None

        CompanyValidationSerializer.validate_company_details(
            data.get('country'), data, errors)

        if errors:
            raise serializers.ValidationError(errors)
        data.pop('customer_type', None)
        data.pop('country', None)
        return data

    def validate_files_size(document, document_type, error):
        if document:
            file_size = document.size
            file_size_limit = 2*1024*1024
            if file_size > file_size_limit:
                return error.update({document_type: "The maximum file size that can be uploaded is 2MB"})
        return document


class CompanySerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Company
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']

        extra_kwargs = {
            'non_field_errors': {
                'error_messages': {
                    'unique_together': 'my custom error message for title'
                }
            }
        }


class OrganizationSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Organization
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']


class CompanyLogisticInfoSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = CompanyLogisticInfo
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']


class CompanyLogisticsSerializer(serializers.ModelSerializer):

    """
        Serializer for company logistic info profile for additional details.
    """

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
                  'annual_fcl_volume',
                  'annual_revenue_currency',
                  'annual_revenue',
                  'company'
                  ]
        read_only_fields = ['id']

    def validate(self, data):
        errors = {}
        company_obj = Company.objects.get(id=data['company'].id)
        company_type = company_obj.user_type
        if company_type == 'customer':
            if 'annaul_logistic_spend_currency' in data and not data.get('annaul_logistic_spend_currency'):
                errors.update(
                    {'annaul_logistic_spend_currency': "This field is required"})
            data['annual_revenue_currency'] = None
            data['annual_revenue'] = None

        if company_type == 'vendor':
            if 'annual_revenue_currency' in data and not data.get('annual_revenue_currency'):
                errors.update(
                    {'annual_revenue_currency': "This field is required"})
            data['annaul_logistic_spend_currency'] = None
            data['annual_logistic_spend'] = None

        if errors:
            raise serializers.ValidationError(errors)

        return data


class CurrencyProfileSerializer(serializers.ModelSerializer):

    """
        Serializer for currency profile for additional details.
    """
    class Meta:
        model = CurrencyProfile
        fields = ['air_currency', 'lcl_currency', 'fcl_currency']
        read_only_fields = ['id']


class AdditionalDetailsCompanySerializer(serializers.Serializer):

    """
        Additional details update serializer.
    """
    company_logistics = CompanyLogisticsSerializer()
    currency_profile_details = CurrencyProfileSerializer()

class CompanyUpdateSerializer(serializers.Serializer):

    """
        Company update serializer with address details.
    """
    company_info = CompanyBaseSerializer(exclude=['organization', 'user_type', 'company_logo'])
    address_details = AddressBaseSerializer(exclude=['country'])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_info'].instance = self.instance


class CompanyAddSerializer(serializers.Serializer):

    """
        Company add serializer with address details.
    """
    company_info = CompanyBaseSerializer()
    address_details = AddressBaseSerializer()

