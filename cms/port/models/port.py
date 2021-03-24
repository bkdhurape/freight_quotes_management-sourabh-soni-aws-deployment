from city.models.city import City
from country.models.country import Country
from django.core.validators import RegexValidator
from django.db import models
from port.managers.port_manager import PortManager
from utils.base_models import StatusBase
from state.models.state import State
import hashlib


class Port(StatusBase, PortManager):

    AIRPORT = 'airport'
    SEAPORT = 'seaport'

    id = models.AutoField(primary_key=True, editable=False)
    code = models.CharField(default=None, null=True, blank=True, max_length=255, validators=[RegexValidator(regex='^[A-Za-z]+[A-Za-z\d\._\s]+$')])
    iata = models.CharField(default=None, null=True, blank=True, max_length=255, validators=[RegexValidator(regex='^[A-Za-z]+[A-Za-z\d\._\s]+$')])
    name = models.CharField(default=None, unique=True, max_length=255, validators=[RegexValidator(regex='^[A-Za-z]+[A-Za-z\d\._\s]+$')])
    country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING)
    state = models.ForeignKey(
        State, blank=True, null=True, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(
        City, blank=True, null=True, on_delete=models.DO_NOTHING)

    PORT_TYPES = [
        (AIRPORT, 'Airport'),
        (SEAPORT, 'Seaport')
    ]
    type = models.CharField(choices=PORT_TYPES, default=AIRPORT, max_length=50 )
    lat = models.FloatField(default=None, blank=False, max_length=255)
    lng = models.FloatField(default=None, blank=False, max_length=255)

    class Meta:
        db_table = 'ports'

    def __str__(self):
        return self.name
