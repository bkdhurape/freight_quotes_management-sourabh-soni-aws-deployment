from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers
from transport.models.transport import Transport

class TransportSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Transport
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']