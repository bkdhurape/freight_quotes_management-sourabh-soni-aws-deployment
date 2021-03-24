from django.conf import settings
from vendor.models.vendor_type import VendorType


class VendorRequestParams:

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
                "home_company": None
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
                    "name": "veer",
                    "email": "veero1u2@g.com",
                    "secondary_email": [
                        "veers@g.com",
                        "veermum@g.com",
                        "veerls@g.com"
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
                    "vendor_type": "freight-forwarder",
                    "company": [1,2,3],
                    "designation": "accountant",
                    "branch": [
                        1
                    ],
                    "supervisor": [
                        1
                    ],
                    "home_company": 4
                },
                "user_companies_currency": [
                    {
                        "1": {
                            "air_currency": "INR",
                            "lcl_currency": "INR",
                            "fcl_currency": "INR"
                        }
                    }
                ],
                "companies_mode": [
                    {
                        "1": ["FCLI", "FCLI", "FCLE"]
                    }
                ]
            }
        return request_params


    # Request params: Update a vendor with valid data
    def put_update_vendor_valid_request_set():
        request_params = {
            "vendor_details": {
                'name': 'shiv1',
                'email': 'shivo1u1@g.com',
                'secondary_email': ['shivs@g.com', 'shivmum@g.com', 'shivls@g.com'],
                'contact_no': None,
                'landline_no_dial_code': '+91',
                'landline_no': '9819123457',
                "vendor_type": 2,
                "company": [
                    1
                ],
                "designation": "accountant",
                "expertise": "import",
                "supervisor": [],
                "home_country": 1,
                "home_company": 1
            },
            "user_companies_currency": [
                {
                    "1": {
                        "air_currency": "INR",
                        "lcl_currency": "PHP",
                        "fcl_currency": "INR"
                    }
                }
            ],
            "companies_mode": []
        }
        return request_params


    def vendor_detail_by_company_and_vendor_id():
        response_params = {
            'vendor_data': {
                'id': 1,
                'name': 'shiv1',
                'email': 'shivo1u1@g.com',
                'secondary_email': ['shivs@g.com', 'shivmum@g.com', 'shivls@g.com'],
                'contact_no': None,
                'landline_no_dial_code': '+91',
                'landline_no': '9819123457',
                'vendor_type': 1,
                'designation': 'accountant',
                'registration_token': None,
                'token_date': None,
                'status': 1,
                'home_company': 1,
                'company': [1,2,3],
                'supervisor': [],
                'branch': []
            },
            'currency_profile_data': [{
                'entity_type': 'vendor',
                'entity_id': 1,
                'air_currency': 'INR',
                'lcl_currency': 'INR',
                'fcl_currency': 'INR'
            }]
        }
        return response_params

     # Response params: Vendor list by company ID valid respone
    def vendor_list_by_company_id_valid_response():
        response_params = [{
                'vendor_data': {
                    'id': 1,
                    'name': 'shiv1',
                    'email': 'shivo1u1@g.com',
                    'secondary_email': ['shivs@g.com', 'shivmum@g.com', 'shivls@g.com'],
                    'contact_no': None,
                    'landline_no_dial_code': '+91',
                    'landline_no': '9819123457',
                    'designation': 'accountant',
                    'registration_token': None,
                    'token_date': None,
                    'status': 1,
                    'vendor_type': 1,
                    'home_company': 4,
                    'company': [4],
                    'supervisor': [],
                    'branch': []
                },
                'currency_profile_data': [{
                    'id': 2,
                    'entity_type': 'vendor',
                    'entity_id': 1,
                    'air_currency': 'INR',
                    'lcl_currency': 'INR',
                    'fcl_currency': 'INR'
                }]
            }
        ]
        return response_params


    # Response params: Vendor list by company ID with limit valid respone
    def vendor_list_by_company_id_with_limit_valid_response():
        response_params = [{
                'vendor_data': {
                    'id': 1,
                    'name': 'shiv1',
                    'email': 'shivo1u1@g.com',
                    'secondary_email': ['shivs@g.com', 'shivmum@g.com', 'shivls@g.com'],
                    'contact_no': None,
                    'landline_no_dial_code': '+91',
                    'landline_no': '9819123457',
                    'vendor_type': 1,
                    'designation': 'accountant',
                    'registration_token': None,
                    'token_date': None,
                    'status': 1,
                    'home_company': 4,
                    'company': [4],
                    'supervisor': [],
                    'branch': []
                },
                'currency_profile_data': [{
                    'id': 2,
                    'entity_type': 'vendor',
                    'entity_id': 1,
                    'air_currency': 'INR',
                    'lcl_currency': 'INR',
                    'fcl_currency': 'INR'
                }]
            }]
        return response_params



    # Request params: Add a vendor with invalid data
    def post_add_vendor_invalid_request_set():
        request_params = Common.post_add_vendor_valid_request_set()
        request_params['vendor_details']['email'] = 'shivOACA3@demo'
        return request_params

    # Request params: Add a vendor with other email id
    def post_add_vendor_other_email_request_set(request_params):
        request_params['vendor_details']['email'] = 'fct11@demo.com'
        return request_params


    # Request params: Register vendor with invalid contact data
    def post_register_vendor_invalid_contact_detail_set(request_params):
        request_params['vendor_details']['email'] = 'shivo1uCN@g.com'
        request_params['vendor_details']['contact_no'] = [
            {
                "dial_code": "91",
                "contact_no": 9819123456
            },
            {
                "dial_code": "1321",
                "contact_no": "9819123455qwe"
            },
            {
                "dial_code": "234",
                "contact_no": 9819123454
            }
        ]
        return request_params


    # Request params: Vendor type
    def post_vendor_type_request_set():
        request_params = {
            "name": "Courier"
        }
        return request_params

    # Request params: Vendor type
    def post_vendor_type_request_set2():
        request_params = {
            "name": "Customs"
        }
        return request_params


    # Request params: Get a list of vendor
    def get_list_of_vendor_type_params_set():
        request_params = [{
            'id': 1,
            'name': 'Courier',
            'slug': 'courier',
            'status': 1
        },
        {
            'id': 2,
            'name': 'Customs',
            'slug': 'customs',
            'status': 1
        }]
        return request_params

    # Request params: Get vendor type details by ID
    def get_vendor_type_by_id_params_set():
        request_params = {
            'id': 2,
            'name': 'Customs',
            'slug': 'customs',
            'status': 1
        }
        return request_params

    # Request params: Add a vendor valid set
    def post_add_a_vendor_valid_params_set():
        request_params = {
            "vendor_details": {
                "name": "veer",
                "email": "veero1u2@g.com",
                "secondary_email": [
                    "veers@g.com",
                    "veermum@g.com",
                    "veerls@g.com"
                ],
                "contact_no": [{
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
                "vendor_type": "freight-forwarder",
                "company": [1, 2, 3],
                "designation": "accountant",
                "branch": [],
                "supervisor": [1],
                "home_company": 1
            },
            "user_companies_currency": [{
                    "1": {
                        "air_currency": "INR",
                        "lcl_currency": "INR",
                        "fcl_currency": "INR"
                    }
                },
                {
                    "2": {
                        "air_currency": "INR",
                        "lcl_currency": "EUR",
                        "fcl_currency": "EUR"
                    }
                },
                {
                    "3": {
                        "air_currency": "EUR",
                        "lcl_currency": "INR",
                        "fcl_currency": "EUR"
                    }
                }
            ],
            "companies_mode": [{
                    "1": ["FCLI", "FCLE"]
                },
                {
                    "2": ["ATC", "FCLE", "LCLE", "LCLI"]
                },
                {
                    "3": ["LCLI", "FCLE", "ATC"]
                }
            ]
        }
        return request_params

    # Request params: Update a vendor valid set
    def put_update_a_vendor_valid_params_set():
        request_params = {
            "vendor_details": {
                "name": "veer",
                "email": "veero1u2@g.com",
                "secondary_email": [
                    "veers@g.com",
                    "veermum@g.com",
                    "veerls@g.com"
                ],
                "contact_no": [{
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
                "vendor_type": 2,
                "company": [1, 2, 3],
                "designation": "accountant",
                "branch": [],
                "supervisor": [1],
                "home_company": 1
            },
            "user_companies_currency": [{
                    "1": {
                        "air_currency": "INR",
                        "lcl_currency": "INR",
                        "fcl_currency": "INR"
                    }
                },
                {
                    "2": {
                        "air_currency": "INR",
                        "lcl_currency": "EUR",
                        "fcl_currency": "EUR"
                    }
                },
                {
                    "3": {
                        "air_currency": "EUR",
                        "lcl_currency": "INR",
                        "fcl_currency": "EUR"
                    }
                }
            ],
            "companies_mode": [{
                    "1": ["FCLI", "FCLE"]
                },
                {
                    "2": ["ATC", "FCLE", "LCLE", "LCLI"]
                },
                {
                    "3": ["LCLI", "FCLE", "ATC"]
                }
            ]
        }
        return request_params
