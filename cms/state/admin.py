from city.models.city import City
from django.contrib import admin
from state.models.state import State


class InlineCity(admin.TabularInline):
    model = City
    fields = ('state', 'name')
    extra = 0


class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'name')
    list_display_links = ('id', 'name')
    search_fields = ['name']
    inlines = [InlineCity]
    list_per_page = 20

admin.site.register(State, StateAdmin)
