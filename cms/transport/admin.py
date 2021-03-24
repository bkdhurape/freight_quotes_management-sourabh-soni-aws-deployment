from transport.models.transport import Transport
from django.contrib import admin


class TransportAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'type')
    list_display_links = ('id', 'name')
    search_fields = ['name']
    list_per_page = 20

admin.site.register(Transport, TransportAdmin)
