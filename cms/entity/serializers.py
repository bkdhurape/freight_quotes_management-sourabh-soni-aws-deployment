from django_restql.mixins import DynamicFieldsMixin
from entity.models.entity import Entity
from rest_framework import serializers


class EntitySerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Entity
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']
