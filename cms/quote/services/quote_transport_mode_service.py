from quote.models.quote import Quote
from quote.models.quote_transport_mode import QuoteTransportMode
from quote.serializers import QuoteTransportModeSerializer

class QuoteTransportModeService:

    def __init__(self, data):
        self.data = data


    #  Get transport modes by quote id
    def get(quote_id):
        quote_transport_mode = QuoteTransportMode.find_by(
            multi=True, join=False, status__ne=Quote.INACTIVE, quote_id=quote_id)
        transport_mode_serializer = QuoteTransportModeSerializer(quote_transport_mode, many=True)

        return transport_mode_serializer.data


    def create(self):

        transport_mode_serializer = QuoteTransportModeSerializer(
            data=self.data)

        if transport_mode_serializer.is_valid(raise_exception=True):
            transport_mode_serializer.save()


    def update(self, id):

        transport_mode = QuoteTransportMode.find_by(id=id)
        transport_mode_serializer = QuoteTransportModeSerializer(transport_mode, data=self.data)
        if transport_mode_serializer.is_valid(raise_exception=True):
            transport_mode_serializer.save()

        return True


    def get_transport_mode_by_quote_id(quote_id, transport_mode = None):

        if transport_mode is None:
            filter_data = {'quote_id': quote_id}
        else:
            filter_data = {'quote_id': quote_id, 'transport_mode': transport_mode}

        quote_transport_mode_data = QuoteTransportMode.find_by(
            multi=True, join=False, status=Quote.ACTIVE, **filter_data)

        quote_transport_mode_serializer = QuoteTransportModeSerializer(quote_transport_mode_data, many=True)

        return quote_transport_mode_serializer.data


    def delete(quote_id, transport_mode = None):
        if transport_mode is None:
            filter_data = {'quote_id': quote_id}
        else:
            filter_data = {'quote_id': quote_id, 'transport_mode': transport_mode}

        transport_mode = QuoteTransportMode.find_by(multi=True, **filter_data)  
        if transport_mode:
            transport_mode[0].delete()