from django.conf import settings
import datetime


class AdditionalDetailsRequestParams:

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

    def quote_valid_set():
        request_params = {
            "basic_details": {
                "transport_mode": ["Air", "FCL"],
                "shipment_terms": "door_to_door",
                "pickup_location": [{
                    "street": "Bhandup",
                    "country": 1
                }],
                "pickup_sea_port": [],
                "pickup_air_port": [],
                "drop_location": [{
                    "street": "kurla",
                    "country": 1
                }],
                "drop_sea_port": [],
                "drop_air_port": [],
                "expected_delivery_date": str(datetime.date.today()),
                "is_personal_courier": True,
                "is_commercial_courier": False,
                "is_origin_custom": False,
                "is_destination_custom": False
            }
        }
        return request_params

    def additional_details_valid_set():
        request_params = {
            "no_of_suppliers": 2,
            "switch_awb": True,
            "preference": [1,2],
            "depreference":[]
        }
        return request_params

    def additional_details_invalid_set():
        request_params = {
            "switch_awb": True,
            "preference": [1,2],
            "depreference":[]
        }
        return request_params

    def additional_details_can_not_select_both():
        request_params = AdditionalDetailsRequestParams.additional_details_valid_set()
        request_params['preference'] = [1,2]
        request_params['depreference'] = [1,2]
        return request_params

    def additional_details_maximum_five_preference_can_be_selected():
        request_params = AdditionalDetailsRequestParams.additional_details_valid_set()
        request_params['preference'] = [1,2,1,2,1,2,1]
        return request_params

    def additional_details_maximum_five_depreference_can_be_selected():
        request_params = AdditionalDetailsRequestParams.additional_details_valid_set()
        request_params['preference'] = []
        request_params['depreference'] = [1,2,1,2,1,2,1]
        return request_params