from branch.managers.branch_manager import BranchManager, BranchServiceManager
from city.models.city import City
from company.models.company import Company
from country.models.country import Country
from decimal import Decimal
from django.contrib.postgres.fields import CICharField
from django.core.validators import MinValueValidator
from django.db import models
from region.models.region import Region
from state.models.state import State
from utils.base_models import QuoteChoice
from utils.base_models import StatusBase
from django.contrib.postgres.fields import JSONField

class Branch(StatusBase, BranchManager):

    RADIUS_UNIT_CHOICES = [ 
        ('miles','Miles'),
        ('km','KM')
    ]

    company = models.ForeignKey(
        Company, blank=False, on_delete=models.DO_NOTHING)
    country = models.ForeignKey(
        Country, blank=False, on_delete=models.DO_NOTHING)
    state = models.ManyToManyField(State, blank=True, db_table='branch_states')
    city = models.ManyToManyField(City, blank=True, db_table='branch_cities')
    region = models.ManyToManyField(
        Region, blank=True, db_table='branch_regions')
    name = CICharField(max_length=255, blank=False)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.DO_NOTHING)
    is_head_branch = models.BooleanField(default=False)
    
    minimum_weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,default=None, validators=[
                                 MinValueValidator(Decimal('0.00'))])

    maximum_weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,default=None, validators=[
                                 MinValueValidator(Decimal('0.00'))])

    minimum_weight_kg = models.FloatField(blank=True, null=True,default=None)

    maximum_weight_kg = models.FloatField(blank=True, null=True,default=None)

    weight_unit = models.CharField(
        max_length=255, choices=QuoteChoice.WEIGHT_UNIT_CHOICES, default=None, blank=True, null=True)

    minimum_radius = models.PositiveIntegerField(blank=True, null=True,default=None)

    maximum_radius = models.PositiveIntegerField(blank=True, null=True,default=None)

    minimum_radius_km = models.FloatField(blank=True, null=True,default=None)

    maximum_radius_km = models.FloatField(blank=True, null=True,default=None)

    radius_unit = models.CharField(
        max_length=255, choices=RADIUS_UNIT_CHOICES, default=None, blank=True, null=True)

    objects = models.Manager()  # The default manager.
    services = BranchServiceManager()

    class Meta:
        db_table = 'branches'
        unique_together = (('company', 'name')) 

    def __str__(self):
        return self.name
