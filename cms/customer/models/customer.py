from django.core.exceptions import ValidationError
from company.models.company import Company
from country.models.country import Country
from customer.managers.customer_manager import CustomerManager, CustomerServiceManager
from department.models.department import Department
from django.contrib.auth.hashers import make_password
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from utils.validations import ContactNumberValidation
from utils.base_models import StatusBase
from utils.dial_code import DialCode
import hashlib


class Customer(StatusBase, CustomerManager):

    INACTIVE = 0
    ACTIVE = 1
    PENDING = 2
    DIAL_CODE_CHOICES = [(i, i) for i in DialCode.get_dial_code()]
    CUSTOMER_TYPE_CHOICES = [
        ('importer_or_exporter', 'Importer/Exporter'),
        ('freight_agent', 'Freight Agent'),
        ('customs_agent', 'Customs Agent'),
        ('e-commerce_platform', 'E-Commerce Platform'),
        ('transporter',  'Transporter'),
        ('other', 'Other')
    ]
    name = models.CharField(max_length=255, validators=[MinLengthValidator(4),
                                                        RegexValidator(regex='^[A-Za-z]+[A-Za-z\d\._\s]+$')])
    email = models.EmailField(unique=True)
    secondary_email = ArrayField(models.EmailField(), null=True, blank=True)
    contact_no_dial_code = models.CharField(max_length=6, null=True, blank=True,
                                            choices=DIAL_CODE_CHOICES)
    contact_no = models.CharField(max_length=12, null=True, blank=True,
                                  validators=[MinLengthValidator(10), ContactNumberValidation.validate_contact_no])
    landline_no_dial_code = models.CharField(blank=True, null=True, max_length=6,
                                             choices=DIAL_CODE_CHOICES)
    landline_no = models.CharField(blank=True, null=True, max_length=12,
                                   validators=[MinLengthValidator(10), RegexValidator(regex='\d{10}')])
    customer_type = models.CharField(max_length=20, null=True, blank=True, choices=CUSTOMER_TYPE_CHOICES)
    customer_type_other = models.CharField(null=True, blank=True, max_length=255)
    company = models.ManyToManyField(Company, related_name='customer_companies', db_table='customer_companies',)
    password = models.CharField(max_length=255, null=True, blank=True)
    designation = models.CharField(null=True, blank=True, max_length=25)
    registration_token = models.UUIDField(blank=True, null=True)
    token_date = models.DateTimeField(blank=True, null=True)
    department = models.ManyToManyField(Department, db_table='customer_departments')
    supervisor = models.ManyToManyField('self', symmetrical=False, related_name='customers',
                                        db_table='customer_supervisors', blank=True)
    home_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    home_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    client = models.ManyToManyField(
        Company, related_name='customer_clients', db_table='customer_clients', blank=True)
    is_super_admin = models.BooleanField(default=False)
    forgot_password_link = models.CharField(null=True, blank=True, max_length=1024)
    forgot_password_date = models.DateTimeField(blank=True, null=True)

    STATUS_CHOICES = [
        (INACTIVE, 'Inactive'),
        (ACTIVE, 'Active'),
        (PENDING, 'Pending')
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    profile_picture = models.ImageField(upload_to='customer/images/%Y/%m/%d/',blank=True,null=True)
    objects = models.Manager()  # The default manager.
    services = CustomerServiceManager()

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return self.name

    def get_company(self):
        return ",".join([str(p) for p in self.company.all()])

    def get_department(self):
        return ",".join([str(p) for p in self.department.all()])

    def get_tag(self):
        return ",".join([str(p) for p in self.tag.all()])
