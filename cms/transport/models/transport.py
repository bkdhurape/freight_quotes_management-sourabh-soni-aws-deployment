from django.db import models
from transport.managers.transport_manager import TransportManager
from utils.base_models import StatusBase


class Transport(StatusBase, TransportManager):
    AIRLINE = 'air_line'
    SHIPLINE = 'ship_line'

    TRANSPORT_TYPE_CHOICES = [
        (AIRLINE, 'Airline'),
        (SHIPLINE, 'Shipline')
    ]

    type = models.CharField(
        max_length=512,
        choices=TRANSPORT_TYPE_CHOICES,
        default=AIRLINE
    )

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=5, blank=True, null=True) #IATA/code
    digit_code = models.CharField(max_length=25,blank=True, null=True)
    agency_code = models.CharField(max_length=255,blank=True, null=True) #just storing name of country, yet no confirmation on it use

    class Meta:
        db_table = 'transports'

    def __str__(self):
        return self.name