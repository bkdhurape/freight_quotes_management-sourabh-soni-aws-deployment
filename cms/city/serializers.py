from city.models.city import City
from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers


class CitySerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = City
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']