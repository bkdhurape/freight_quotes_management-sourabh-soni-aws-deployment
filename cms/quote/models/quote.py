from company.models.company import Company
from django.core.validators import MinValueValidator
from django.db import models
from quote.managers.quote_manager import QuoteServiceManager
from transport.models.transport import Transport
from utils.base_models import StatusBase
from django.contrib.postgres.fields import ArrayField
import datetime
from quote.managers.quote_manager import QuoteManager


class Quote(StatusBase, QuoteManager):

    INACTIVE = 0
    ACTIVE = 1
    PENDING = 2

    STATUS_CHOICES = [
        (INACTIVE, 'Inactive'),
        (ACTIVE, 'Active'),
        (PENDING, 'Pending')
    ]
    QUOTE_TYPE_CHOICES = [
        ('open', 'open'),
        ('expired', 'expired'),
        ('booked', 'booked'),
        ('cancelled', 'cancelled'),
        ('pending', 'pending')
    ]
    SHIPMENT_TYPE_CHOICES = [
        ('import', 'import'),
        ('export', 'export'),
        ('third-country', 'third_country'),
    ]

    SHIPMENT_TERM_CHOICES = [
        ('door_to_door', 'Door To Door'),
        ('door_to_port', 'Door To Port'),
        ('port_to_door', 'Port To Door'),
        ('port_to_port', 'Port To Port')
    ]

    company = models.ForeignKey(
        Company, blank=False, on_delete=models.DO_NOTHING)
    shipment_terms = models.CharField(
        max_length=255, choices=SHIPMENT_TERM_CHOICES)
    expected_delivery_date = models.DateField(
        validators=[MinValueValidator(datetime.date.today)], null=True, blank=True)
    expected_arrival_date = models.DateField(
        validators=[MinValueValidator(datetime.date.today)], null=True, blank=True)
    is_origin_custom = models.BooleanField(default=False)
    is_submit_quote = models.BooleanField(default=False)
    is_destination_custom = models.BooleanField(default=False)
    is_personal_courier = models.BooleanField(default=False)
    is_commercial_courier = models.BooleanField(default=False)
    po_number = ArrayField(models.CharField(max_length=255) ,default=list, blank=True, null=True)
    no_of_suppliers = models.IntegerField(blank=True, null=True)
    quote_deadline = models.DateField(
        validators=[MinValueValidator(datetime.date.today)], null=True, blank=True)

    switch_awb = models.BooleanField(default=False)
    switch_b_l = models.BooleanField(default=False)
    packaging = models.BooleanField(default=False)
    palletization = models.BooleanField(default=False)

    preference = models.ManyToManyField(
        Transport, related_name='quote_preferences', db_table='quote_preferences', blank=True)
    depreference = models.ManyToManyField(
        Transport, related_name='quote_depreferences', db_table='quote_depreferences', blank=True)

    free_days_destination = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    quote_no = models.CharField(max_length = 20, null=True, blank=True, unique = True)
    quote_status = models.CharField(max_length=10,choices=QUOTE_TYPE_CHOICES)
    shipment_type= models.CharField(max_length=20,choices=SHIPMENT_TYPE_CHOICES,default='import')
    # reason = models.CharField(max_length=255, null=True, blank=True)

    quote_no_counter = models.IntegerField(default=0)
    objects = models.Manager()  # The default manager.
    services = QuoteServiceManager()

    class Meta:
        db_table = 'quotes'

    def __str__(self):
        return self.shipment_terms
