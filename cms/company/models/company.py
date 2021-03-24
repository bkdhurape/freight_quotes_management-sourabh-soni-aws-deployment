from company.managers.company_manager import CompanyManager, CompanyServiceManager
from company.models.organization import Organization
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import CICharField
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, RegexValidator
from django.db import models
from utils.base_models import StatusBase
from utils.responses import success_response
import datetime

class Company(StatusBase, CompanyManager):

    COMPANY_TYPE_CHOICES = [
        ('sole_proprietorship', 'Sole Proprietorship'),
        ('partnership', 'Partnership'),
        ('llp', 'LLP'),
        ('pvt_ltd', 'Pvt Ltd'),
        ('public_ltd', 'Public Ltd'),
    ]
    name = CICharField(max_length=512,
                            null=False,
                            blank=False,
                            validators=[MinLengthValidator(4),
                                        RegexValidator(regex='^[A-Za-z]+[A-Za-z\d\._\s]+$')])

    company_type = models.CharField(
        max_length=30,
        choices=COMPANY_TYPE_CHOICES,
        default='sole_proprietorship',
    )

    INDUSTRY_CHOICES = (
        ('consumer_goods_or_fmcg', 'Consumer Goods/FMCG'),
        ('engineering_and_manufacturing', 'Engineering and Manufacturing'),
        ('textiles_and_fashion_apparel', 'Textiles and Fashion Apparel'),
        ('retail', 'Retail'),
        ('automotive', 'Automotive'),
        ('electronics', 'Electronics'),
        ('chemicals', 'Chemicals'),
        ('healthcare', 'Healthcare'),
        ('technology', 'Technology'),
        ('hospitality', 'Hospitality'),
        ('food_and_beverages', 'Food & Beverages'),
        ('jewellery', 'Jewellery'),
        ('renewable_energy_gas_solar_etc', 'Renewable Energy: Gas,Solar etc.'),
        ('oil_and_gas', 'Oil & Gas'),
        ('marine', 'Marine'),
        ('aerospace', 'Aerospace'),
        ('government_or_defense', 'Government / Defense'),
        ('other', 'Other'))
    industry = ArrayField(models.CharField(
        max_length=255, choices=INDUSTRY_CHOICES), default=list, null=True, blank=True)
    industry_other = models.CharField(
        default=None, null=True, blank=True, max_length=255)

    BUSINESS_ACTIVITY_CHOICES = (
        ('manufacturer', 'Manufacturer'),
        ('supplier', 'Supplier'),
        ('retailer', 'Retailer'),
        ('wholesaler', 'Wholesaler'),
        ('distributor', 'Distributor'),
        ('trader', 'Trader'),
        ('service', 'Service'),
        ('agriculture', 'Agriculture'),
        ('other', 'Other'))
    business_activity = ArrayField(models.CharField(
        max_length=255, choices=BUSINESS_ACTIVITY_CHOICES), default=list, blank=True )
    business_activity_other = models.CharField(
        default=None, null=True, blank=True, max_length=255)

    iec = models.CharField(max_length=10, validators=[
                           MinLengthValidator(10)], blank=True, null=True)
    gst = models.CharField(
        max_length=15,
        validators=[
            MinLengthValidator(15),
            RegexValidator(
                regex='^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$')
        ], blank=True, null=True)

    pan = models.CharField(
        max_length=10,
        validators=[
            MinLengthValidator(10),
            RegexValidator(regex='[A-Za-z]{5}\d{4}[A-Za-z]{1}')
        ], blank=True, null=True)
    cin = models.CharField(
        max_length=21,
        validators=[
            MinLengthValidator(21),
            RegexValidator(
                regex='^([L|U]{1})([0-9]{5})([A-Z]{2})([0-9]{4})([PLC|PTC]{3})([0-9]{6})$'
            )
        ], blank=True, null=True)

    company_bio = models.TextField(blank=True, null=True)
    company_structure = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=20,
                            choices=[
                                ('customer', 'Customer'),
                                ('vendor', 'Vendor'),
                            ])
    incorporation_year = models.IntegerField(validators=[MinValueValidator(
        1970), MaxValueValidator(datetime.date.today().year)], null=True, blank=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
    )
    company_logo = models.ImageField(upload_to='company/images/%Y/%m/%d/',blank=True,null=True)
    pan_document = models.FileField(upload_to ='company/document/pan/%Y/%m/%d/',blank=True,null=True) 
    cin_document = models.FileField(upload_to ='company/document/cin/%Y/%m/%d/',blank=True,null=True)
    gst_document = models.FileField(upload_to ='company/document/gst/%Y/%m/%d/',blank=True,null=True)
    iec_document = models.FileField(upload_to ='company/document/iec/%Y/%m/%d/',blank=True,null=True)
    # country_id = models.IntegerField()

    # CompanyServiceManager
    objects = models.Manager()  # The default manager.
    services = CompanyServiceManager()

    class Meta:
        db_table = 'companies'
        unique_together = (('name', 'user_type'))
        permissions = (('assign_task', 'Assign task'),)

    def __str__(self):
        return self.name
