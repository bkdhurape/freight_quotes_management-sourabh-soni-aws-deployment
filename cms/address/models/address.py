from address.manager.address_manager import AddressManager
from city.models.city import City
from country.models.country import Country
from django.core.validators import RegexValidator
from django.db import models
from port.models.port import Port
from state.models.state import State
from utils.base_models import StatusBase


class Address(StatusBase, AddressManager):
    entity_type = models.CharField(max_length=255, null=False)
    entity_id = models.IntegerField(null=False)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(
        State, blank=True, null=True, on_delete=models.CASCADE)
    city = models.ForeignKey(City, null=True, blank=True,
                             on_delete=models.CASCADE)
    pincode = models.CharField(max_length=10, validators=[
                               RegexValidator(r'^\d{6,10}$')], blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    seaport_ids = models.ManyToManyField(
        Port, blank=True, related_name='address_seaport', db_table='address_seaport')
    airport_ids = models.ManyToManyField(
        Port, blank=True, related_name='address_airport', db_table='address_airport')

    class Meta:
        db_table = 'addresses'
