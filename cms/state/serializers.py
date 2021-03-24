from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers
from state.models.state import State


class StateSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = State
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']