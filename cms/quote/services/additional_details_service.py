from company.services.company_service import CompanyService
from exceptions import AdditionalDetailsException, AdditionalDetailsError
from quote.models.quote import Quote
from quote.serializers import QuoteSerializer
from quote.models.quote_transport_mode import QuoteTransportMode
from utils.responses import get_paginated_data


class AdditionalDetailsService:

    def __init__(self, data):
        self.data = data

    def update(self, company_id, quote_id):

        quote_data = Quote.find_by(status__ne=Quote.INACTIVE, company_id=company_id, id=quote_id)

        if 'no_of_suppliers' not in self.data or not self.data['no_of_suppliers']:
            raise AdditionalDetailsException(
                AdditionalDetailsError.NO_OF_SUPPLIERS_REQUIRED)

        transport_mode_type_data = list(QuoteTransportMode.find_by(
            multi=True, quote_id=quote_id, status=Quote.ACTIVE).values_list('transport_mode', flat=True))

        if 'Air' in transport_mode_type_data:

            if (('preference' not in self.data or not self.data['preference']) and (
                    'depreference' not in self.data or not self.data['depreference'])):
                raise AdditionalDetailsException(
                    AdditionalDetailsError.ONE_SHOULD_BE_SELECTED)

            if (('preference' in self.data and self.data['preference']) and (
                    'depreference' in self.data and self.data['depreference'])):
                raise AdditionalDetailsException(
                    AdditionalDetailsError.ONLY_ONE_CAN_BE_SELECTED)

            if ('preference' in self.data and len(self.data['preference']) > 5):
                raise AdditionalDetailsException(
                    AdditionalDetailsError.MAXIMUM_PREFERENCE_VALIDATION)

            if ('depreference' in self.data and len(self.data['depreference']) > 5):
                raise AdditionalDetailsException(
                    AdditionalDetailsError.MAXIMUM_DEPREFERENCE_VALIDATION)

            if ('preference' in self.data and self.data['preference']):
                self.data['depreference'] = []

            if ('depreference' in self.data and self.data['depreference']):
                self.data['preference'] = []
        else:
            self.data['preference'] = []
            self.data['depreference'] = []

        additional_details_serializer = QuoteSerializer(
            quote_data, data=self.data, partial=True)

        if additional_details_serializer.is_valid(raise_exception=True):
            additional_details_serializer.save()

        return True
