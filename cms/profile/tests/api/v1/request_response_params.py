from country.models.country import Country
from django.conf import settings


class ProfileRequestParams:

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

    def login_valid_request_params():
        request_params = {
            "email": "rashmita123@g.com",
            "password": "rashmita123",
            "account_type": "vendor"
        }
        return request_params

    def login_valid_request_params_for_customer():
        request_params = {
            "email": "shivo1u1@g.com",
            "password": "qwerty",
            "account_type": "customer"
        }
        return request_params

    def post_customer_registration_personal_details_request_set():
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

    def post_add_customer_valid_request_set():
        request_params = {
            "customer_details": {
                "name": "shiv",
                "email": "shivOACA2@g.com",
                "secondary_email": ["shivs@g.com", "shivmum@g.com", "shivls@g.com"],
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
                "customer_type": "importer_or_exporter",
                "company": [
                    1
                ],
                "designation": "accountant",
                "expertise": "import",
                "department": [
                    1, 2, 3
                ],
                "supervisor": [
                    1
                ],
                "home_country": 1,
                "home_company": 1
            },
            "user_companies_currency": [{
                "1": {
                "air_currency": "INR",
                "lcl_currency": "INR",
                "fcl_currency": "INR"
                }
            }],
        }
        return request_params
        
    def post_vendor_registration_personal_details_request_set():
        request_params = {
        "vendor_details": {
            "name":"rashmita",
            "email": "rashmita123@g.com",
            "secondary_email": ["shivs@g.com", "shivsmum@g.com", "shivsin@g.com"],
            "contact_no": [],
            "landline_no_dial_code": "+91",
            "landline_no": "9819123457",
            "vendor_type": "freight-forwarder",
            "company_name": "nf11221ngf",
            "password": "rashmita123",
            "designation": "accountant",
            "expertise": "import",
            "home_company":None,
            "incorporation_year":202111
        },
        "address_details": {
            "pincode": "123114",
            "country":2,
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
                "email": "shivOACA2@g.com",
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
            "companies_mode": [
            {
            "1": [
                "FCLI",
                "FCLE"
            ]
            }],
            "user_companies_currency": [
            {
            "1": {
                "air_currency": "INR",
                "lcl_currency": "INR",
                "fcl_currency": "INR"
            }
            }]
        }
        return request_params

    def set_profile():
        request_params = {
            "name": "shiv",
            "email": "shivOACA2@g.com",
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
            "password":"111",
            "confirm_password":"111"
        }
        
        return request_params

    def set_profile_blank_password():
        request_params=ProfileRequestParams.set_profile()
        request_params['password'] = "" 
        return request_params

    def set_profile_mismatch_password():
        request_params=ProfileRequestParams.set_profile()
        request_params['password'] = "12345"
        request_params['confirm_password'] = "123451" 
        return request_params

    def set_profile_blank_confirm_password():
        request_params=ProfileRequestParams.set_profile()
        request_params['password'] = "12345"
        request_params['confirm_password'] = "" 
        return request_params

    def set_profile_validation_on_contact_no():
        request_params=ProfileRequestParams.set_profile()
        request_params['contact_no'] = None
        request_params['landline_no'] = None 
        return request_params