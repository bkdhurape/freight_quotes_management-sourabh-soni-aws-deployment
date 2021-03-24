from address.models.address import Address
from django.contrib import admin


# Register your models here.

class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'address1', 'address2', 'city', 'country', 'pincode',
                    'entity_id','entity_type','type','state')
    list_display_links = ('id', 'address1')
    search_fields = ('address1','entity_id','entity_type','entity_id')
    list_per_page = 20


admin.site.register(Address, AddressAdmin)

