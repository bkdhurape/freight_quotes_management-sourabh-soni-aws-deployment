from rest_framework import serializers
from rest_framework import validators
from django_restql.mixins import DynamicFieldsMixin
from tag.models.tag import Tag

class TagSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']

    

