from branch.models.branch import Branch
from company.models.company import Company
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.postgres.fields import CIEmailField
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from utils.base_models import StatusBase
from utils.dial_code import DialCode
from utils.validations import ContactNumberValidation
from vendor.managers.vendor_manager import VendorManager, VendorServiceManager
from vendor.models.vendor_type import VendorType


class Vendor(StatusBase, VendorManager):

    INACTIVE = 0
    ACTIVE = 1
    PENDING = 2
    DIAL_CODE_CHOICES = [(i, i) for i in DialCode.get_dial_code()]
    VENDOR_TYPE_CHOICES = [
        ('foreign_agent','Foreign Agent'),
        ('freight_forwarder','Freight Forwarder'),
        ('courier','Courier'),
        ('customs','Customs'),
        ('customs_transport','Customs + Transport'),
        ('transport_only','Transport Only')

    ]
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(default=None, blank=False, max_length=255, validators=[MinLengthValidator(4), RegexValidator(regex='^[A-Za-z]+[A-Za-z\d\._\s]+$')])
    email = CIEmailField(default=None, null=False, blank=False, unique=True,
                              error_messages={'required': 'Vendor email required..!'})
    secondary_email = ArrayField(models.EmailField(), null=True, blank=True)
    contact_no_dial_code = models.CharField(max_length=6, null=True, blank=True,
                                            choices=DIAL_CODE_CHOICES)
    contact_no = models.CharField(max_length=12, null=True, blank=True,
                                  validators=[MinLengthValidator(10), ContactNumberValidation.validate_contact_no])
    landline_no_dial_code = models.CharField(blank=True, null=True, max_length=6,
                                             choices=DIAL_CODE_CHOICES)
    landline_no = models.CharField(blank=True, null=True, max_length=12,
                                   validators=[MinLengthValidator(10), RegexValidator(regex='\d{10}')])
    vendor_type = models.CharField(max_length=255, choices=VENDOR_TYPE_CHOICES)
    company = models.ManyToManyField(Company, related_name='vendor_companies', db_table='vendor_companies')
    password = models.CharField(default=None, null=True, max_length=255)
    designation = models.CharField(default=None, null=True, max_length=25)
    registration_token = models.UUIDField(default=None, blank=True, null=True)
    token_date = models.DateTimeField(blank=True, null=True)
    supervisor = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='vendors',
                                        db_table='vendor_supervisors')
    branch = models.ManyToManyField(Branch, db_table='vendor_branches', blank=True)
    home_company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    client = models.ManyToManyField(Company, related_name='vendor_clients', db_table='vendor_clients', blank=True)
    is_super_admin = models.BooleanField(default=False)
    forgot_password_link = models.CharField(default=None, null=True, blank=True, max_length=1024)
    forgot_password_date = models.DateTimeField(blank=True, null=True)

    STATUS_CHOICES = [
        (INACTIVE, 'Inactive'),
        (ACTIVE, 'Active'),
        (PENDING, 'Pending')
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    profile_picture = models.ImageField(upload_to='vendor/images/%Y/%m/%d/',blank=True,null=True)
    objects = models.Manager()  # The default manager.
    services = VendorServiceManager()

    class Meta:
        db_table = 'vendors'

    def __str__(self):
        return self.name

    def get_company(self):
        return ",".join([str(p) for p in self.company.all()])
