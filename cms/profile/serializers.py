from customer.models.customer import Customer
from vendor.models.vendor import Vendor
from rest_framework import serializers
from django_restql.mixins import DynamicFieldsMixin

class CustomerSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    REQUIRED_TOGETHER_FIELDS = [('contact_no_dial_code', 'contact_no'),
                                ('landline_no_dial_code', 'landline_no')]
    confirm_password = serializers.CharField(max_length=255,write_only=True)

    class Meta:
        model = Customer
        fields = ['name','contact_no_dial_code','contact_no', 'landline_no_dial_code', 'landline_no',  'password', 'registration_token', 'token_date','status','confirm_password','email']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, 'allow_blank': False, 'allow_null': False},
            'confirm_password': {'required': True, 'allow_null': False, 'allow_blank': False}
            }

    def validate(self, data):
        errors = {}
        for field1, field2 in self.REQUIRED_TOGETHER_FIELDS:
            msg = 'This field is required.'
            if data.get(field1) and not data.get(field2):
                errors.update({field2: msg})
            elif not data.get(field1) and data.get(field2):
                errors.update({field1: msg})

        msg = 'This field is required.'
        if  ('name' in data and (not data.get('contact_no') and not data.get('landline_no'))):
            msg = 'Please fill either Mobile Number or Landline Number.'
            errors.update({'contact_no': msg, 'landline_no': msg})

        if data.get('password') != data.get('confirm_password'):
            errors.update({'password':'password did not match'})
        data.pop('confirm_password', None)

        if errors:
            raise serializers.ValidationError(errors)
        return data

class VendorSerializer(CustomerSerializer):

    class Meta(CustomerSerializer.Meta): 
        model = Vendor
