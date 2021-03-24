from branch.managers.branch_manager import BranchTransportManager
from branch.models.branch import Branch
from commodity.models.commodity import Commodity
from country.models.country import Country
from django.contrib.postgres.fields import ArrayField
from django.db import models
from utils.base_models import StatusBase,QuoteChoice


class BranchTransportMode(StatusBase, BranchTransportManager):
    TRANSPORT_MODE_CHOICES = [
        ('AI', 'Air-Import'),
        ('AE', 'Air-Export'),
        ('ATC', 'Air-Third Country'),
        ('FCLI', 'FCL-Import'),
        ('FCLE', 'FCL-Export'),
        ('FCLTC', 'FCL-Third Country'),
        ('LCLI', 'LCL-Import'),
        ('LCLE', 'LCL-Export'),
        ('LCLTC', 'LCL-Third Country')
    ]
    branch = models.ForeignKey(
        Branch, blank=False, on_delete=models.DO_NOTHING)
    transport_mode = models.CharField(
        max_length=255, choices=TRANSPORT_MODE_CHOICES, default=None, null=False)
    container_type = ArrayField(models.CharField(
        max_length=255, choices=QuoteChoice.CONTAINER_TYPE_CHOICES, default=None), null=True, blank=True)
    hazardous = models.BooleanField(default=False)
    instant_quotes = models.BooleanField(default=False)
    trade_lanes = models.ManyToManyField(
        Country, blank=True, related_name='branch_transport_trade_lanes')
    from_trade_lanes = models.ManyToManyField(
        Country, blank=True, related_name='branch_transport_from_trade_lanes')
    to_trade_lanes = models.ManyToManyField(
        Country, blank=True, related_name='branch_transport_to_trade_lanes')
    commodity = models.ManyToManyField(
        Commodity, db_table='branch_transport_commodities')

    class Meta:
        db_table = 'branch_transport_modes'
        unique_together = (('branch', 'transport_mode'))

    def __str__(self):
        return self.transport_mode
