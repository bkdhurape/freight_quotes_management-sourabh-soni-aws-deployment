from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from quote.managers.quote_manager import QuoteTransportModeManager
from quote.models.quote import Quote
from utils.base_models import QuoteChoice, StatusBase, TotalWeightVolume


class QuoteTransportMode(StatusBase, TotalWeightVolume, QuoteTransportModeManager):
    quote = models.ForeignKey(
        Quote, on_delete=models.DO_NOTHING, related_name='transport_modes')
    transport_mode = models.CharField(max_length=30, choices=QuoteChoice.QUOTE_TRANSPORT_MODE_CHOICES)

    class Meta:
        db_table = 'quote_transport_modes'
        unique_together = (('quote', 'transport_mode'))

    def __str__(self):
        return self.transport_mode
