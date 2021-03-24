from django.contrib import admin
from quote.models import Quote,PackageDetails,QuoteTransportMode


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id','company','shipment_terms','quote_status', 'expected_delivery_date','expected_arrival_date','is_origin_custom',
    'is_submit_quote','is_destination_custom','is_personal_courier','is_commercial_courier','po_number','no_of_suppliers','quote_deadline',
    'switch_awb','switch_b_l','packaging' ,'palletization','free_days_destination','status','quote_no','quote_status',
    'quote_no_counter')
    search_fields = ('id','quote_no','quote_status','quote_deadline','is_submit_true')
    list_per_page = 20

class PackageDetailsAdmin(admin.ModelAdmin):
    list_display = ('id','quote','pickup_location','drop_location','no_of_containers','product','type','quantity','length','width','height','dimension_unit',
    'weight','weight_unit','is_hazardous','is_stackable','container_type','container_subtype','no_of_containers','stuffing','destuffing','package_detail_type',
    'container','temperature','temperature_unit','shipper_details','consignee_details','is_fcl_container','cargo_type','is_order_ready','order_ready_date',
    'invoice_value','invoice_value_currency','handover_date')
    list_per_page = 20


class QuoteTransportModesAdmin(admin.ModelAdmin):
    list_display = ('id','quote_id','transport_mode')
    list_per_page = 20


# Register your models here.
admin.site.register(Quote,QuoteAdmin),
admin.site.register(PackageDetails,PackageDetailsAdmin),
admin.site.register(QuoteTransportMode,QuoteTransportModesAdmin)
