from django.contrib import admin
from customer.models.customer import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'secondary_email', 'contact_no',
                    'landline_no_dial_code', 'landline_no', 'customer_type', 'get_company', 'designation',
                    'get_department')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email')
    list_per_page = 20


admin.site.register(Customer, CustomerAdmin)
