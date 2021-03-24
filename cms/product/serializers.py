from django_restql.mixins import DynamicFieldsMixin
from product.models.product import Product
from rest_framework import serializers

class ProductSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['id']
