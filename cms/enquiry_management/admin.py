from django.contrib import admin
from enquiry_management.models.company_expertise import CompanyExpertise

class EnquiryManagementInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'transport_mode', 'container_type', 'hazardous', 'instant_quotes',
                    'max_weight', 'weight_unit', 'temperature_controlled')
    list_display_links = ('id', 'company')
    list_per_page = 20

# Register your models here.
admin.site.register(CompanyExpertise,EnquiryManagementInfoAdmin)
