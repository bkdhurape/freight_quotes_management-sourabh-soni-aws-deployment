from company.models.company import Company
from contact_person.managers.contact_person_manager import ContactPersonManager
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.postgres.fields import CIEmailField
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from utils.base_models import StatusBase
from utils.dial_code import DialCode
from utils.validations import ContactNumberValidation


class ContactPerson(StatusBase, ContactPersonManager):

    DIAL_CODE_CHOICES = [(i, i) for i in DialCode.get_dial_code()]
    
    company = models.ForeignKey(
        Company, blank=False, on_delete=models.DO_NOTHING)

    name = models.CharField(max_length=255, validators=[
        RegexValidator(
            regex='^[A-Za-z]+[A-Za-z\d\._\s]+$')
    ])
    email = CIEmailField(unique=True)
    contact_no_dial_code = models.CharField(max_length=4, null=True, blank=True,
                                            choices=DIAL_CODE_CHOICES)
    contact_no = models.CharField(max_length=12, null=True, blank=True,
                                  validators=[MinLengthValidator(10), ContactNumberValidation.validate_contact_no])
    landline_no_dial_code = models.CharField(blank=True, null=True, max_length=4,
                                             choices=DIAL_CODE_CHOICES)
    landline_no = models.CharField(blank=True, null=True, max_length=12,
                                   validators=[MinLengthValidator(10), RegexValidator(regex='\d{10}')])
    designation = models.CharField(default=None, null=True, blank=True, max_length=25)

    FINANCE = 'finance'
    SHIPPER_USER = 'shipper_user'
    CONSIGNEE_USER = 'consignee_user'
    CONSIGNEE_SHIPPER_USER = 'consignee_shipper_user'

    TYPE_CHOICES = (
        (FINANCE, 'Finance'),
        (SHIPPER_USER, 'Shipper user'),
        (CONSIGNEE_USER, 'Consignee user'),
        (CONSIGNEE_SHIPPER_USER, 'Consignee Shipper user'),
    )
    contact_person_type = models.CharField(choices=TYPE_CHOICES,
                            default=FINANCE, max_length=255)

    class Meta:
        db_table = 'contact_persons'

    def __str__(self):
        return self.email
