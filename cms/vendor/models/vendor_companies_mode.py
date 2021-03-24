from company.models.company import Company
from django.contrib.postgres.fields import ArrayField
from django.db import models
from utils.base_models import Base, CreatedUpdatedBy
from vendor.managers.vendor_companies_mode_manager import VendorCompaniesModeManager
from vendor.models.vendor import Vendor


class VendorCompaniesMode(Base, CreatedUpdatedBy, VendorCompaniesModeManager):

    MODE_CHOICES = [
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

    id = models.AutoField(primary_key=True, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    mode = ArrayField(base_field=models.CharField(choices=MODE_CHOICES, max_length=255), size=9)

    class Meta:
        db_table = 'vendor_company_modes'

