from django.conf import settings
import datetime


class QuoteRequestParams:

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
            'port/fixtures/port.json'
        ]
        return fixture_list

    # Request params: Login credential with valid data
    def login_valid_request_params(self):
        request_params = {
            "email": "shivo1u1@g.com",
            "password": "qwerty",
            "account_type": "customer"
        }
        return request_params

    # Request params: Customer registration request params contain personal detail with valid data
    def post_customer_registration_personal_details_request_set(self):
        request_params = {
            "customer_details": {
                "name": "shiv1",
                "email": "shivo1u1@g.com",
                "secondary_email": ["shivs@g.com", "shivmum@g.com", "shivls@g.com"],
                "contact_no": None,
                "landline_no_dial_code": "+91",
                "landline_no": "9819123457",
                "customer_type": "importer_or_exporter",
                "company_name": "fct_o1cA",
                "password": "qwerty",
                "designation": "accountant",
                "expertise": "import",
                "home_country": 1,
                "home_company": None
            }
        }
        return request_params

    def quote_valid_set():
        request_params = {
            "basic_details": {
                "transport_mode": ["Air", "Air_courier"],
                "shipment_terms": "port_to_port",
                "pickup_location": [],
                "pickup_sea_port": [],
                "pickup_air_port": [1, 2],
                "drop_location": [],
                "drop_sea_port": [],
                "drop_air_port": [1, 2],
                "expected_delivery_date": str(datetime.date.today()),
                "expected_arrival_date": str(datetime.date.today()),
                "is_personal_courier": True,
                "is_commercial_courier": False,
                "is_origin_custom": False,
                "is_destination_custom": False
            }
        }
        return request_params

    def quote_invalid_params_for_door_to_door_pickup():

        request_params = QuoteRequestParams.quote_valid_set()
        request_params['basic_details']['shipment_terms'] = "door_to_door"
        return request_params

    def quote_invalid_params_for_door_to_door_drop():

        request_params = QuoteRequestParams.quote_valid_set()
        request_params['basic_details']['shipment_terms'] = "door_to_door"
        request_params['basic_details']['pickup_location'] = [{
            "street": "Bhandup",
            "country": 1
        },
            {
                "street": "Bhandup",
                "country": 1

        }
        ]
        return request_params

    def quote_invalid_params_for_port_to_port_air():

        request_params = QuoteRequestParams.quote_valid_set()

        request_params['basic_details']['pickup_air_port'] = []

        return request_params

    def quote_invalid_params_for_port_to_port_FCL_and_LCL():

        request_params = QuoteRequestParams.quote_valid_set()
        request_params['basic_details']['transport_mode'] = ["LCL", "FCL"]
        return request_params

    def date_validation():

        request_params = QuoteRequestParams.quote_valid_set()
        request_params['basic_details']['expected_arrival_date'] = "2020-04-05"
        return request_params

    def quote_invalid_params_for_door_to_port_air():
        request_params = QuoteRequestParams.quote_valid_set()
        request_params['basic_details']['shipment_terms'] = 'door_to_port'
        return request_params

    def quote_invalid_params_for_door_to_port_FCL_and_LCL():
        request_params = QuoteRequestParams.quote_valid_set()
        request_params['basic_details']['shipment_terms'] = 'door_to_port'
        request_params['basic_details']['transport_mode'] = ["FCL", "LCL"]
        request_params['basic_details']['pickup_location'] = [{
            "street": "Bhandup",
            "country": 1
        },
            {
                "street": "Bhandup",
                "country": 1

        }
        ]
        return request_params

    def quote_invalid_params_for_port_to_door_air():
        request_params = QuoteRequestParams.quote_valid_set()
        request_params['basic_details']['shipment_terms'] = 'port_to_door'
        return request_params

    def quote_invalid_params_for_port_to_door_LCL_and_FCL():
        request_params = QuoteRequestParams.quote_valid_set()
        request_params['basic_details']['transport_mode'] = ["FCL", "LCL"]
        request_params['basic_details']['shipment_terms'] = 'port_to_door'
        return request_params

    def quote_air_courier_validation():
        request_params = QuoteRequestParams.quote_valid_set()
        request_params['basic_details']['is_personal_courier'] = False
        request_params['basic_details']['is_commercial_courier'] = False
        return request_params

    def quote_get_all_keys():

        quote_keys = [
            'id',
            'status',
            'shipment_terms',
            'expected_delivery_date',
            'expected_arrival_date',
            'is_origin_custom',
            'is_destination_custom',
            'is_personal_courier',
            'is_commercial_courier',
            'po_number',
            'no_of_suppliers',
            'quote_deadline',
            'switch_awb',
            'switch_b_l',
            'packaging',
            'palletization',
            'free_days_destination',
            'company',
            'pickup_air_port',
            'pickup_sea_port',
            'drop_air_port',
            'drop_sea_port',
            'pickup_location',
            'drop_location',
            'transport_mode'
        ]

        return quote_keys

    def quote_update_air_courier_validation():
        request_params = QuoteRequestParams.quote_valid_set()
        request_params['basic_details']['transport_mode'] = ["Air_courier"]
        request_params['basic_details']['is_personal_courier'] = False
        request_params['basic_details']['is_commercial_courier'] = False
        return request_params

    def quote_update_valid_set():
        request_params = QuoteRequestParams.quote_valid_set()
        request_params['basic_details']['transport_mode'] = ["Air","Air_courier"]
        request_params['basic_details']['is_origin_custom'] = True
        return request_params

    def quote_update_sea_port_validation():
        request_params = QuoteRequestParams.quote_valid_set()
        request_params['basic_details']['transport_mode'] = ["LCL"]
        return request_params

    def quote_update_door_to_door_validation():
        request_params = QuoteRequestParams.quote_valid_set()
        request_params['basic_details']['shipment_terms'] = "door_to_door"
        return request_params

    def quote_update_quote_expected_deliver_date_reuired_for_door():
        request_params = QuoteRequestParams.quote_valid_set()
        request_params['basic_details']['shipment_terms'] = "port_to_door"
        request_params['basic_details']['drop_location'] = [{
            "street":"LBS",
            "countey":1
        }]
        request_params['basic_details']['expected_delivery_date'] = None
        return request_params

    def quote_create_transport_mode_should_not_blank():
        request_params = QuoteRequestParams.quote_valid_set()
        request_params['basic_details']['transport_mode'] = []
        return request_params

    