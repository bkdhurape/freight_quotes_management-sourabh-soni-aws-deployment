from country.models.country import Country
from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers


class CountrySerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Country
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']