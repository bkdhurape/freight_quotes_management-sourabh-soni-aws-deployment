from django.conf import settings
from entity.models.entity import Entity


class EntityRequestParams:

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
            'vendor/fixtures/vendor_type.json'
        ]
        return fixture_list


    def vendor_get_request_keys():
        vendor_keys = [
            'id',
            'name',
            'email',
            'secondary_email',
            'contact_no',
            'landline_no_dial_code',
            'landline_no',
            'designation',
            'registration_token',
            'token_date',
            'status',
            'vendor_type',
            'home_company',
            'company',
            'supervisor',
            'branch'
        ]

        vendor_currency_keys = [
            'id',
            'entity_type',
            'entity_id',
            'air_currency',
            'lcl_currency',
            'fcl_currency'
        ]

        return vendor_keys, vendor_currency_keys

    # Request params: Login credential with valid data
    def login_valid_request_params():
        request_params = {
                "email": "shivo1u1@g.com",
                "password": "apple",
                "account_type": "vendor"
            }
        return request_params

    # Request params: Vendor registration request params contain personal detail with valid data
    def post_vendor_registration_personal_details_request_set():
        request_params = {
            "vendor_details": {
                'name': 'shiv1',
                'email': 'shivo1u1@g.com',
                'secondary_email': ['shivs@g.com', 'shivmum@g.com', 'shivls@g.com'],
                'contact_no': None,
                'landline_no_dial_code': '+91',
                'landline_no': '9819123457',
                "vendor_type": 'freight-forwarder',
                "company_name": "fct_o1cA",
                "password": "apple",
                "designation": "accountant",
                "expertise": "import",
                "home_country": 1,
                "home_company": None,
                "branch": []
            },
            "address_details": {
            	"pincode": "123456",
                "country":1,
                "state":1,
                "city": 1,
                "street": "1234infisa56"
            }
        }
        return request_params

    # Request params: Add a vendor with valid data
    def post_add_vendor_valid_request_set():
        request_params = {
            "vendor_details": {
                "name": "FCT1Name",
                "email": "fct1@g.demo",
                "secondary_email": [
                    "shivs@g.com",
                    "shivmum@g.com",
                    "shivls@g.com"
                ],
                "contact_no": [
                    {
                        "dial_code": "91",
                        "contact_no": 9819123456
                    },
                    {
                        "dial_code": "1",
                        "contact_no": 9819123455
                    },
                    {
                        "dial_code": "234",
                        "contact_no": 9819123454
                    }
                ],
                "landline_no_dial_code": "+91",
                "landline_no": "9819123457",
                "vendor_type": 'freight-forwarder',
                "company": [
                    1
                ],
                "designation": "accountant",
                "branch": [
                    1
                ],
                "supervisor": [
                    1
                ],
                "home_company": 1
            },
            "currency_profile_detail": {
                "air_currency": "USD",
                "lcl_currency": "USD",
                "fcl_currency": "USD"
            }
        }
        return request_params



    # Request params: Vendor type
    def post_entity_request_set():
        request_params = {
            "name": "Entity1",
            "is_shipper": True,
            "is_consignee": False,
            "company": 1
        }
        return request_params

    # Request params: Vendor type
    def post_entity_request_set2():
        request_params = {
            "name": "Entity2",
            "is_shipper": True,
            "is_consignee": False,
            "company": 1
        }
        return request_params


    # Request params: Get a list of vendor
    def get_list_of_entity_params_set():
        request_params = [{
            'id': 2,
            "name": "Entity2",
            "is_shipper": True,
            "is_consignee": False,
            "company": 1,
            'status': 1
        },{
            'id': 1,
            "name": "Entity1",
            "is_shipper": True,
            "is_consignee": False,
            "company": 1,
            'status': 1
        }]
        return request_params

    # Request params: Get vendor type details by ID
    def get_entity_by_id_params_set():
        request_params = {
            'id': 2,
            "name": "Entity2",
            "is_shipper": True,
            "is_consignee": False,
            "company": 1,
            'status': 1
        }
        return request_params
