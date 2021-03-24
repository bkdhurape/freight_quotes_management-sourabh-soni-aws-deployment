from company.models.company import Company
from customer.managers.invited_service_manager import InvitedVendorManager, InvitedServiceManager
from customer.models.customer import Customer
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from utils.base_models import StatusBase
from utils.dial_code import DialCode
from vendor.models.vendor import Vendor


class InvitedVendor(StatusBase, InvitedVendorManager):

    REJECT = 0
    ACTIVE = 1
    PENDING = 2

    DIAL_CODE_CHOICES = [(i, i) for i in DialCode.get_dial_code()]

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(default=None, blank=False, max_length=255, validators=[MinLengthValidator(4), RegexValidator(regex='^[A-Za-z]+[A-Za-z\d\._\s]+$')])
    email = models.EmailField(default=None, null=False, blank=False)
    contact_no_dial_code = models.CharField(max_length=4, null=True, blank=True,
                                            choices=DIAL_CODE_CHOICES)
    contact_no = models.CharField(default=None, blank=True, null=True, max_length=12,
                                   validators=[MinLengthValidator(10), RegexValidator(regex='\d{10}')])
    landline_no_dial_code = models.CharField(default=None, blank=True, null=True, max_length=12)
    landline_no = models.CharField(default=None, blank=True, null=True, max_length=12,
                                   validators=[MinLengthValidator(10), RegexValidator(regex='\d{10}')])
    company_name = models.CharField(null=False, blank=False, max_length=512, validators=[MinLengthValidator(4), RegexValidator(regex='^[a-zA-Z\w]+$')])
    customer_company = models.ForeignKey(Company, related_name='customer_company', on_delete=models.DO_NOTHING, blank=True, null = True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, blank=True, null = True)
    vendor_company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, blank=True, null = True)
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING, blank=True, null = True)

    STATUS_CHOICES = [
        (REJECT, 'Reject'),
        (ACTIVE, 'Active'),
        (PENDING, 'Pending')
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING )

    objects = models.Manager()  # The default manager.
    services = InvitedServiceManager()

    class Meta:
        db_table = 'invited_vendors'
        unique_together = (('customer_company', 'email'))

    def __str__(self):
        return self.name
