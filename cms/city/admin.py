from city.models.city import City
from django.contrib import admin


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'name')
    list_display_links = ('id', 'name')
    search_fields = ['name']
    list_per_page = 20

admin.site.register(City, CityAdmin)
