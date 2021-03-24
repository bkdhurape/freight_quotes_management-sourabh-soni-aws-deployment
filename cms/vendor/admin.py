
from django.contrib import admin
from vendor.models.vendor import Vendor


class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'secondary_email', 'contact_no',
                    'landline_no_dial_code', 'landline_no', 'vendor_type',  'designation'
                   )
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email')
    list_per_page = 20


admin.site.register(Vendor,VendorAdmin)