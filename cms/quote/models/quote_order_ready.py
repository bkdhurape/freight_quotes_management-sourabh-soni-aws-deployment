from address.models.address import Address
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from quote.managers.quote_manager import QuoteOrderReadyManager
from quote.models.quote import Quote
from quote.models.quote_transport_mode import QuoteTransportMode
from utils.helpers import present_or_future_date
from utils.base_models import StatusBase, TotalWeightVolume

class QuoteOrderReady(StatusBase, TotalWeightVolume, QuoteOrderReadyManager):

    quote = models.ForeignKey(
        Quote, blank=False, on_delete=models.DO_NOTHING)
    transport_mode = models.ForeignKey(QuoteTransportMode, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='order_ready_transport_mode')
    address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='order_ready_address')

    is_order_ready = models.BooleanField(default=False)
    order_ready_date = models.DateField(validators=[present_or_future_date] , null=True, blank=True)
    invoice_value = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    invoice_value_currency = models.CharField(default='INR', max_length=5)

    handover_date = models.DateField(validators=[present_or_future_date] , null=True, blank=True)

    class Meta:
        db_table = 'quote_order_readies'

    def __str__(self):
        return self.quote
