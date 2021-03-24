from django.conf import settings


class CityParams:

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


    # Response Params: City list response set
    def get_city_list_response_set():
        response_params = [{
                "id": 5,
                "name": "Kochi",
                "state": 3
            }, {
                "id": 6,
                "name": "Munnar",
                "state": 3
            }]
        return response_params


    # Response Params: City Detail response set
    def get_city_detail_response_set():
        response_params = [{
                "id": 5,
                "name": "Kochi",
                "state": 3
            }]
        return response_params
