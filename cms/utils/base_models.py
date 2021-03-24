from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CreatedUpdatedBy(models.Model):
    created_by = models.CharField(max_length=512, default='system')
    updated_by = models.CharField(max_length=512, default='system')

    class Meta:
        abstract = True


class StatusBase(Base, CreatedUpdatedBy):
    INACTIVE = 0
    ACTIVE = 1

    STATUS_CHOICES = [
        (INACTIVE, 'Inactive'),
        (ACTIVE, 'Active')
    ]

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )

    class Meta:
        abstract = True


class QuoteChoice:

    PACKAGE = 'package'
    TOTAL = 'total'

    CONTAINER_TYPE_CHOICES = [
        ('20GP', '20-GP'),
        ('40GP', '40-GP'),
        ('20Flat-Rack', '20-Flat-Rack'),
        ('40Flat-Rack', '40-Flat-Rack'),
        ('20OT', '20-OT'),
        ('40OT', '40-OT'),
        ('20Reefer', '20-Reefer'),
        ('40Reefer', '40-Reefer'),
        ('20Tank', '20-Tank'),
        ('40HC', '40-HC'),
        ('45HC', '45-HC'),
    ]

    CONTAINER_SUBTYPE_CHOICES = [
        ('GP', 'GP'),
        ('FR', 'Flat-Rack'),
        ('OT', 'Open-Top'),
        ('RF', 'Reefer'),
        ('Tank', 'Tank'),
        ('HC', 'HC'),
    ]

    QUOTE_TRANSPORT_MODE_CHOICES = [
        ('Air', 'Air'),
        ('LCL', 'LCL'),
        ('FCL', 'FCL'),
        ('Air_courier', 'Air Courier')
    ]

    WEIGHT_UNIT_CHOICES = [
        ('kg', 'KG'),
        ('tonnes', 'TONS'),
        ('lbs','LBS')
    ]

    VOLUME_UNIT_CHOICES = [
        ('cbm', 'CBM')
    ]

    VOLUMETRIC_UNIT_CHOICES = [
        ('kg', 'KGS')
    ]

    PACKAGE_DETAIL_TYPE = [
        (PACKAGE,'Package'),
        (TOTAL, 'Total')
    ]

    DIMENSION_UNIT_CHOICES = [
        ('feet', 'FEET'),
        ('inch', 'INCH'),
        ('cm', 'CM'),
        ('mm', 'MM'),
        ('m', 'M')
    ]

    STUFFING_DESTUFFING_CHOICES = [
        ('dock', 'DOCK'),
        ('factory', 'FACTORY')
    ]

    PACKAGE_TYPE_CHOICES = [
        ('bale', 'BALE'),
        ('bundles', 'BUNDLES'),
        ('carton', 'CARTON'),
        ('pallte', 'PALLET'),
        ('case', 'CASE'),
        ('drums', 'DRUMS'),
        ('sack', 'SACK'),
        ('bag', 'BAG'),
        ('unpacked', 'UNPACKED')
    ]

    TEMPERATURE_UNIT_CHOICES = [
        ('C', 'C'),
        ('F', 'F')
    ]

class CompanyExpertiseChoice:
    WEIGHT_UNIT_CHOICES = [
        ('kg', 'KG'),
        ('lbs','LBS')
    ]

class TotalWeightVolume(models.Model, QuoteChoice):
    total_weight_unit = models.CharField(max_length=255, choices=QuoteChoice.WEIGHT_UNIT_CHOICES, default=None, null=True)
    total_weight = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    total_volume_unit = models.CharField(max_length=255, choices=QuoteChoice.VOLUME_UNIT_CHOICES, default=None, null=True)
    total_volume = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    total_volumetric_weight_unit = models.CharField(max_length=255, choices=QuoteChoice.VOLUMETRIC_UNIT_CHOICES, default=None, null=True)
    total_volumetric_weight = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        abstract = True
