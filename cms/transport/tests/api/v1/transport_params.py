from django.conf import settings


class TransportParams:

    @staticmethod
    def api_url():
        return settings.API_HOST

    # Get seed data list
    def get_seed_data_list():
        fixture_list = [
            'country/fixtures/country.json',
            'state/fixtures/state.json',
            'city/fixtures/city.json',
            'region/fixtures/region.json',
            'commodity/fixtures/commodity.json',
            'port/fixtures/port.json',
            'transport/fixtures/transport.json'
            ]
        return fixture_list

