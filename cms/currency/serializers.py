from company.models.company import Company
from .models.currency_profile import CurrencyProfile
from company.serializers import CompanySerializer
from rest_framework import serializers


class CurrencyProfileSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()

    class Meta:
        model = CurrencyProfile
        fields = ['id', 'entity_type', 'entity_id', 'company', 'air_currency', 'lcl_currency', 'fcl_currency']
        read_only_fields = ['id']

    def get_company(self, obj):
        return CompanySerializer(obj.company, read_only=True,
                                 fields=('id', 'name')).data


class CustomerCompaniesCurrencySerializer(CurrencyProfileSerializer):
    entity_type = serializers.CharField(required=False)
    entity_id = serializers.IntegerField(required=False)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False)