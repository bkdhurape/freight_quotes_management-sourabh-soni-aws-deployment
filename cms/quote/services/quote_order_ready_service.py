from quote.models.quote import Quote
from quote.models.quote_order_ready import QuoteOrderReady
from quote.serializers import QuoteOrderReadySerializer

class QuoteOrderReadyService:

    def __init__(self, data):
        self.data = data


    #  Get order ready by quote id
    def get(quote_id):
        quote_order_ready = QuoteOrderReady.find_by(
            multi=True, join=False, status__ne=Quote.INACTIVE, quote_id=quote_id)
        quote_order_ready_serializer = QuoteOrderReadySerializer(quote_order_ready, many=True)

        return quote_order_ready_serializer.data


    def create(self):

        order_ready_serializer = QuoteOrderReadySerializer(
            data=self.data)

        if order_ready_serializer.is_valid(raise_exception=True):
            order_ready_serializer.save()


    def update(self, id):
        order_ready_details = QuoteOrderReady.find_by(id=id)
        order_ready_serializer = QuoteOrderReadySerializer(order_ready_details, data=self.data)

        if order_ready_serializer.is_valid(raise_exception=True):
            order_ready_serializer.save()

        return True
