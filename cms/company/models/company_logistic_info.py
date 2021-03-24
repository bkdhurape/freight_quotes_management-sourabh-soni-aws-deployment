from company.managers.company_logistic_info_manager import CompanyLogisticInfoManager, CompanyAdditionalDetailServiceManager
from company.models.company import Company
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from utils.base_models import StatusBase


class CompanyLogisticInfo(StatusBase, CompanyLogisticInfoManager):

    CURRENCY_CHOICES = [
        ('INR','INR'),
        ('USD','USD'),
        ('PES','PES'),
        ('AUS','AUS'),
        ('LKR','LKR')

    ]

    annaul_logistic_spend_currency = models.CharField(max_length=5, null=True, blank=True,choices=CURRENCY_CHOICES)
    annual_logistic_spend = models.DecimalField(max_digits=10, decimal_places=3, default=0, blank=True,null=True,validators=[
        MinValueValidator(Decimal('0.00'))])

    annual_air_shipments = models.PositiveIntegerField(default=0)
    annual_lcl_shipments = models.PositiveIntegerField(default=0)
    annual_fcl_shipments = models.PositiveIntegerField(default=0)
    total_shipments = models.PositiveIntegerField(default=0)

    annual_air_volume = models.DecimalField(max_digits=10, decimal_places=3, default=0 ,validators=[
        MinValueValidator(Decimal('0.00'))])
    annual_lcl_volume = models.DecimalField(max_digits=10, decimal_places=3, default=0 ,validators=[
        MinValueValidator(Decimal('0.00'))])
    annual_fcl_volume = models.DecimalField(max_digits=10, decimal_places=3, default=0, validators=[
        MinValueValidator(Decimal('0.00'))])
    annual_revenue_currency = models.CharField(max_length=5,null=True,blank=True,choices=CURRENCY_CHOICES)
    annual_revenue = models.DecimalField(max_digits=10, decimal_places=3, default=0, blank=True,null=True,validators=[
        MinValueValidator(Decimal('0.00'))])

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        default=None
    )

    objects = models.Manager()  # The default manager.
    services = CompanyAdditionalDetailServiceManager()

    class Meta:
        db_table = 'company_logistic_infos'
