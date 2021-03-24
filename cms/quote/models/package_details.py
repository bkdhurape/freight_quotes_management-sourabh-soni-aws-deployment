from address.models.address import Address
from commodity.models.commodity import Commodity
from decimal import Decimal
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from quote.managers.quote_manager import PackageDetailsManager
from quote.models.quote import Quote
from quote.models.quote_transport_mode import QuoteTransportMode
from utils.base_models import QuoteChoice, StatusBase, TotalWeightVolume
import datetime


class PackageDetails(StatusBase, TotalWeightVolume, PackageDetailsManager):
    quote = models.ForeignKey(
        Quote, blank=False, on_delete=models.DO_NOTHING,related_name='package_details')
    transport_mode = models.ManyToManyField(
        QuoteTransportMode, blank=False, related_name='transport_mode_package_details')
    commodity = models.ManyToManyField(
        Commodity, db_table='package_details_commodities', blank=True)
    pickup_location = models.ForeignKey(Address, blank=True, null=True, default=None,
                                        on_delete=models.DO_NOTHING, related_name='package_details_pickup_location')
    drop_location = models.ForeignKey(Address, blank=True, null=True, default=None,
                                      on_delete=models.DO_NOTHING, related_name='package_details_drop_location')
    product = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(
        max_length=255, choices=QuoteChoice.PACKAGE_TYPE_CHOICES, blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    length = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, validators=[
        MinValueValidator(0.00)])
    width = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, validators=[
        MinValueValidator(0.00)])
    height = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, validators=[
        MinValueValidator(0.00)])
    dimension_unit = models.CharField(
        max_length=255, choices=QuoteChoice.DIMENSION_UNIT_CHOICES, default=None, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, validators=[
        MinValueValidator(0.00)])
    weight_unit = models.CharField(
        max_length=255, choices=QuoteChoice.WEIGHT_UNIT_CHOICES, default=None, null=True)
    is_hazardous = models.BooleanField(default=False)
    is_stackable = models.BooleanField(default=False)
    container_type = models.CharField(
        max_length=255, choices=QuoteChoice.CONTAINER_TYPE_CHOICES, blank=True, null=True)
    container_subtype = models.CharField(
        max_length=255, choices=QuoteChoice.CONTAINER_SUBTYPE_CHOICES, blank=True, null=True)
    no_of_containers = models.PositiveIntegerField(blank=True, null=True)
    stuffing = models.CharField(
        max_length=255, choices=QuoteChoice.STUFFING_DESTUFFING_CHOICES, blank=True, null=True)
    destuffing = models.CharField(
        max_length=255, choices=QuoteChoice.STUFFING_DESTUFFING_CHOICES, blank=True, null=True)

    package_detail_type = models.CharField(max_length=255, choices=QuoteChoice.PACKAGE_DETAIL_TYPE,
                                           default=QuoteChoice.PACKAGE, null=True)
    container = models.ForeignKey(
        "self", blank=True, null=True, default=None, on_delete=models.DO_NOTHING,
        related_name='container_package_details')

    temperature = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    temperature_unit = models.CharField(
        max_length=255, choices=QuoteChoice.TEMPERATURE_UNIT_CHOICES, blank=True, null=True)
    shipper_details = models.CharField(max_length=255, null=True, blank=True, validators=[
        RegexValidator(
            regex='^[A-Za-z\d\._\s]+$')
    ])
    consignee_details = models.CharField(max_length=255, null=True, blank=True, validators=[
        RegexValidator(
            regex='^[A-Za-z\d\._\s]+$')
    ])
    is_fcl_container = models.BooleanField(default=False)
    cargo_type = models.CharField(max_length=255, null=True, blank=True)

    is_order_ready = models.BooleanField(default=False)
    order_ready_date = models.DateField(validators=[MinValueValidator(datetime.date.today)] , null=True, blank=True)
    invoice_value = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    invoice_value_currency = models.CharField(default='INR', max_length=5)
    handover_date = models.DateField(validators=[MinValueValidator(datetime.date.today)] , null=True, blank=True)


    class Meta:
        db_table = 'package_details'

    def __str__(self):
        return str(self.transport_mode)
