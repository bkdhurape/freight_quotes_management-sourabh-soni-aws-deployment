from country.models.country import Country
from django.contrib import admin
from state.models.state import State


class InlineState(admin.TabularInline):
    model = State
    fields = ('country', 'name')
    extra = 0


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'currency_code')
    list_display_links = ('id', 'name')
    search_fields = ['name']
    list_per_page = 20
    inlines = [InlineState]

admin.site.register(Country, CountryAdmin)
