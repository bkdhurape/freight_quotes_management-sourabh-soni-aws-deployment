from contact_person.models.contact_person import ContactPerson
from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers


class ContactPersonSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = ContactPerson
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']
    
class ContactPersonBaseSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    REQUIRED_TOGETHER_FIELDS = [('contact_no_dial_code', 'contact_no'),
                                ('landline_no_dial_code', 'landline_no')]

    class Meta:
        model = ContactPerson
        fields = ['name','email', 'contact_no_dial_code', 'contact_no', 'landline_no_dial_code', 'landline_no',
                  'designation', 'contact_person_type', 'company']
        read_only_fields = ['id']


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

        if error_dict:
            raise serializers.ValidationError(error_dict)
        return attrs