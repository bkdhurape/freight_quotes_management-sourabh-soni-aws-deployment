from django.conf import settings


class CountryParams:

    @staticmethod
    def api_url():
        return settings.API_HOST

    # Get seed data list
    def get_seed_data_list():
        fixture_list = [
            'city/fixtures/city.json',
            'commodity/fixtures/commodity.json',
            'country/fixtures/country.json',
            'port/fixtures/port.json',
            'region/fixtures/region.json',
            'state/fixtures/state.json',
            'vendor/fixtures/vendor_type.json',
            ]
        return fixture_list


    # Response Params: Country list response set
    def get_country_list_response_set():
        response_params = [{
                "id": 3,
                "name": "Colombia",
                "code": "CO",
                "currency_code": "PES"
            }, {
                "id": 2,
                "name": "United States",
                "code": "US",
                "currency_code": "USD"
            }, {
                "id": 1,
                "name": "India",
                "code": "IN",
                "currency_code": "INR"
            }]
        return response_params


    # Response Params: Country Detail response set
    def get_country_detail_response_set():
        response_params = [{
                "id": 3,
                "name": "Colombia",
                "code": "CO",
                "currency_code": "PES"
            }]
        return response_params