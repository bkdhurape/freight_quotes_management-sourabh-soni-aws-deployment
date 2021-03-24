from customer.models.customer import Customer
from vendor.models.vendor import Vendor
from django_restql.mixins import DynamicFieldsMixin
from django.core.exceptions import ValidationError
from rest_framework import serializers


class CustomerProfileSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields=['profile_picture']

    def validate_profile_picture(self,image):
        if image:
            file_size = image.size
            file_size_limit = 2 * 1024 * 1024
            if file_size > file_size_limit :
                raise ValidationError("The maximum image size that can be uploaded is 2MB")
            image.name = str(self.instance.id) +'.' + image.name.split('.')[-1]
        return image

class VendorProfileSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields=['profile_picture']

    def validate(self,data):
        if data.get('profile_picture'):
            CustomerProfileSerializer.validate_profile_picture(self,data.get('profile_picture'))

        return data