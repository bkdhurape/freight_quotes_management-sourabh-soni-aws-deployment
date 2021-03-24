from company.models import Company, Organization, CompanyLogisticInfo
from django.contrib import admin


# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company_type', 'industry', 'business_activity', 'iec',
                    'pan', 'gst', 'user_type', 'company_structure', 'organization')
    list_display_links = ('id', 'name', 'user_type')
    search_fields = ('name', 'user_type')
    list_per_page = 20

class CompanyLogisticsInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'annaul_logistic_spend_currency', 'annual_logistic_spend', 'annual_lcl_shipments', 'annual_fcl_shipments', 'total_shipments',
                    'annual_air_volume', 'annual_lcl_volume', 'annual_fcl_volume', 'annual_revenue_currency', 'annual_revenue','company')
    list_display_links = ('id', 'company')
    list_per_page = 20


admin.site.register(Company, CompanyAdmin),
admin.site.register(CompanyLogisticInfo, CompanyLogisticsInfoAdmin),
admin.site.register(Organization),
