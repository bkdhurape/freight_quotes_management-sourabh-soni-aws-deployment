from country.models.country import Country
from currency.serializers import CurrencyProfileSerializer
from currency.models.currency_profile import CurrencyProfile
from django.core.exceptions import ObjectDoesNotExist
from exceptions.currency_exceptions import CurrencyException, CurrencyError


class CurrencyProfileService:

    def __init__(self, data):
        self.data = data

    def create(self):
        currency_profile_serializer = CurrencyProfileSerializer(data=self.data)

        if currency_profile_serializer.is_valid(raise_exception=True):
            currency_profile_id = (currency_profile_serializer.save()).id

        return currency_profile_id
    '''set  default country currency based on home country and if  data in request_data  then override from default currency to request_data'''

    def set_country_currency(request_data, country_id):
        country = Country.objects.get(pk=country_id)
        currency = country.currency_code
        currency_data = {}
        currency_data.update({"air_currency": request_data['air_currency']}) if 'air_currency' in request_data and request_data['air_currency'] else currency_data.update(
            {"air_currency": currency})
        currency_data.update({"fcl_currency": request_data['fcl_currency']}) if 'fcl_currency' in request_data and request_data['fcl_currency'] else currency_data.update(
            {"fcl_currency": currency})
        currency_data.update({"lcl_currency": request_data['lcl_currency']}) if 'lcl_currency' in request_data and request_data['lcl_currency'] else currency_data.update(
            {"lcl_currency": currency})

        return currency_data

    '''request data is from add new company or customer'''

    def set_currency(request_data, entity_id, entity_type, company_id, country_id):
        request_currency_data = CurrencyProfileService.set_country_currency(
            request_data, country_id)
        currency_data = CurrencyProfile.find_by(multi=True,
            entity_id=entity_id, entity_type=entity_type, company_id=company_id)
        request_currency_data.update(
                {'entity_type': entity_type, 'entity_id': entity_id, 'company': company_id})
        
        if not currency_data:     
            currency_profile_service_object = CurrencyProfileService(data=request_currency_data)
            currency_profile_service_object.create()
        else:
            currency_profile_id = list(currency_data.values_list('id', flat=True))[0]
            currency_condition={'entity_type': entity_type, 'entity_id': entity_id, 'company': company_id, 'id':currency_profile_id}
            currency_profile_data = CurrencyProfile.find_by(**currency_condition)         
            currency_profile_serializer = CurrencyProfileSerializer(
            currency_profile_data, data=request_currency_data)

            if currency_profile_serializer.is_valid(raise_exception=True):
                currency_profile_serializer.save()


    def update(self, entity_id, entity_type, id):
        currency_profile = CurrencyProfile.find_by(
            entity_id=entity_id, entity_type=entity_type, id=id)
        currency_profile_serializer = CurrencyProfileSerializer(
            currency_profile, data=self.data)

        if currency_profile_serializer.is_valid(raise_exception=True):
            currency_profile_serializer.save()

    def get_currency_profile(entity_type=None, entity_id=None):
        currency = CurrencyProfile.find_by(
            entity_type=entity_type, entity_id=entity_id, multi=True)
        # if not currency:
        #     raise CurrencyException(CurrencyError.CURRENCY_NOT_FOUND)
        currency_serializer = CurrencyProfileSerializer(currency, many=True)
        return currency_serializer.data if len(currency_serializer.data) > 0 else {}


    def delete(id=None):
        currency = CurrencyProfile.find_by(id=id) 
        currency.delete()
        
