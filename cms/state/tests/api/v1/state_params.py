from django.conf import settings


class StateParams:

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


    # Response Params: State list response set
    def get_state_list_response_set():
        response_params = [{
                "id": 2,
                "name": "Goa",
                "country": 1
            }, {
                "id": 3,
                "name": "Kerala",
                "country": 1
            }, {
                "id": 1,
                "name": "Punjab",
                "country": 1
            }]
        return response_params


    # Response Params: State Detail response set
    def get_state_detail_response_set():
        response_params = [{
                "id": 3,
                "name": "Kerala",
                "country": 1
            }]
        return response_params
