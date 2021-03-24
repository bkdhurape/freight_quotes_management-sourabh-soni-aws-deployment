from commodity.models.commodity import Commodity
from company.models.company import Company
from country.models.country import Country
from decimal import Decimal
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from enquiry_management.manager.company_expertise_manager import CompanyExpertiseManager
from utils.base_models import StatusBase,QuoteChoice,CompanyExpertiseChoice

class CompanyExpertise(StatusBase,CompanyExpertiseManager):
    TRANSPORT_MODE_CHOICES = [
        ('AI', 'Air-Import'),
        ('AE', 'Air-Export'),
        ('ATC', 'Air-Third Country'),
        ('ACI', 'Air-Courier Import'),
        ('ACE', 'Air-Courier Export'),
        ('ACTC', 'Air-Courier Third Country'),
        ('FCLI', 'FCL-Import'),
        ('FCLE', 'FCL-Export'),
        ('FCLTC', 'FCL-Third Country'),
        ('LCLI', 'LCL-Import'),
        ('LCLE', 'LCL-Export'),
        ('LCLTC', 'LCL-Third Country')
    ]
    company = models.ForeignKey(Company,on_delete=models.DO_NOTHING)
    transport_mode = models.CharField(
        max_length=255, choices=TRANSPORT_MODE_CHOICES,default=None,null=False)
    container_type=ArrayField(models.CharField(
        max_length=255,choices=QuoteChoice.CONTAINER_TYPE_CHOICES,default=None), null=True, blank=True)
    hazardous = models.BooleanField(default=True)
    instant_quotes = models.BooleanField(default=True)
    max_weight = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True,validators=[
                                 MinValueValidator(Decimal('0.00'))])
    weight_unit = models.CharField(max_length=255, choices=CompanyExpertiseChoice.WEIGHT_UNIT_CHOICES, default=None,null=True,blank=True)
    temperature_controlled = models.BooleanField(default=True,null=True)
    trade_lanes = models.ManyToManyField(
    Country, blank=True, related_name='company_expertise_trade_lanes')
    from_trade_lanes = models.ManyToManyField(
        Country,blank=True, related_name='company_expertise_from_trade_lanes')
    to_trade_lanes = models.ManyToManyField(
        Country, blank=True, related_name='company_expertise_to_trade_lanes')
    commodity = models.ManyToManyField(Commodity,db_table='company_expertise_commodities')

    class Meta:
        db_table = 'company_experties'
        unique_together = (('company', 'transport_mode'))


    def __str__(self):
        return self.transport_mode
