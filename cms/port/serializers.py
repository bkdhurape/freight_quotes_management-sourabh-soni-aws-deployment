from django_restql.mixins import DynamicFieldsMixin
from port.models.port import Port
from rest_framework import serializers

class PortSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Port
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']
