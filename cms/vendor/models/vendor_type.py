from django.db import models
from django.template.defaultfilters import slugify
from utils.base_models import StatusBase
from vendor.managers.vendor_type_manager import VendorTypeManager
import hashlib


class VendorType(StatusBase, VendorTypeManager):

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(default=None, blank=False, unique=True, max_length=255)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    class Meta:
        db_table = 'vendor_types'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug =  slugify(self.name)
        super(VendorType, self).save(*args, **kwargs)
