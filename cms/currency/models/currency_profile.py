from company.models.company import Company
from currency.managers.currency_manager import CurrencyManager
from django.db import models
from utils.base_models import Base, CreatedUpdatedBy


class CurrencyProfile(Base, CreatedUpdatedBy, CurrencyManager):

    CURRENCY_CHOICES = [
        ('INR','INR'),
        ('USD','USD'),
        ('PES','PES'),
        ('AUS','AUS'),
        ('LKR','LKR')

    ]

    entity_type = models.CharField(null=False, max_length=255)
    entity_id = models.IntegerField(null=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    air_currency = models.CharField(max_length=5,choices=CURRENCY_CHOICES)
    lcl_currency = models.CharField(max_length=5,choices=CURRENCY_CHOICES)
    fcl_currency = models.CharField(max_length=5,choices=CURRENCY_CHOICES)

    class Meta:
        db_table = 'currency_profiles'
