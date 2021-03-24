from django.conf import settings


class CustomerParams:

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


    # Request Params: Customer Register with Required valid params set
    def post_register_required_request_params():
        request_params = {
                "customer_details": {
                    "name": "Calvin",
                    "email": "calvino1u1@g.com",
                    "secondary_email": [
                        "calvincrew@g.com",
                        "calvinmum@g.com",
                        "calvinin@g.com"
                    ],
                    "contact_no": [],
                    "landline_no_dial_code": "+91",
                    "landline_no": "9819123457",
                    "customer_type": "importer_or_exporter",
                    "company_name": "canon_o1cA",
                    "password": "qwerty",
                    "designation": "accountant",
                    "expertise": "import",
                    "home_country": 2,
                    "home_company": None
                }
            }
        return request_params


    # Request Params: Customer Register with valid params set
    def post_register_request_params():
        request_params = {
                "company_details": {
                    "industry": [
                        "consumer_goods_or_fmcg",
                        "engineering_and_manufacturing",
                        "retail",
                        "other"
                    ],
                    "industry_other": "i_abc_2",
                    "business_activity": [
                        "manufacturer",
                        "supplier",
                        "wholesaler",
                        "other"
                    ],
                    "business_activity_other": "ba_abc_2",
                    "iec": 1233214567,
                    "pan": "asdfg2344n",
                    "gst": "12ABCDE1234A1Z1",
                    "cin": "U67190TN2014PTC096978",
                    "annual_revenue": 234,
                    "address_details": {
                        "pincode": "123456",
                        "country": 1,
                        "state": 1,
                        "city": 1,
                        "street": "1234infisa56"
                    }
                },
                "customer_details": {
                    "name": "Calvin",
                    "email": "calvino2u1@g.com",
                    "secondary_email": [
                        "calvincrew@g.com",
                        "calvinmum@g.com",
                        "calvinin@g.com"
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
                    "customer_type": "importer_or_exporter",
                    "company_name": "canon_o2cA",
                    "password": "qwerty",
                    "designation": "accountant",
                    "expertise": "import",
                    "home_country": 1,
                    "home_company": None
                },
                "currency_profile_detail": {
                    "air_currency": "USD",
                    "lcl_currency": "USD",
                    "fcl_currency": "USD"
                },
                "additional_details": {
                    "annaul_logistic_spend_currency": "USD",
                    "annual_logistic_spend": 3000,
                    "annual_air_shipments": 300,
                    "annual_lcl_shipments": 300,
                    "annual_fcl_shipments": 300,
                    "total_shipments": 900,
                    "annual_air_volume": 300,
                    "annual_lcl_volume": 300,
                    "annual_fcl_volume": 300,
                    "incorporation_year": 2019,
                    "incorporation_number": "ABCXYZ",
                    "annual_revenue_currency": "USD",
                    "annual_revenue": 2000
                }
            }
        return request_params


    # Request Params: Add a Customer with valid params set
    def post_add_customer_request_params():
        request_params = {
                "customer_details": {
                    "name": "Calvin",
                    "email": "calvino1u2@g.com",
                    "secondary_email": [
                        "calvincrew@g.com",
                        "calvinmum@g.com",
                        "calvinin@g.com"
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
                    "customer_type": "importer_or_exporter",
                    "company": [
                        1,2,3
                    ],
                    "password": "qwerty",
                    "designation": "accountant",
                    "expertise": "import",
                    "department": [
                        1,2,3
                    ],
                    "supervisor": [
                        1
                    ],
                    "home_country": 1,
                    "home_company": 1
                },
                "user_companies_currency": [
                    {
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
                ]
            }
        return request_params


    # Request Params: Login Customer with valid params set
    def post_login_customer_request_params():
        request_params = {
                "email": "calvino1u1@g.com",
                "password": "qwerty",
                "account_type": "customer"
            }
        return request_params


    # Request Params: Add a Customer Company with valid params set
    def post_add_customer_company_request_params():
        request_params = {
                "name": "canon_o1cB",
                "company_type": "sole_proprietorship",
                "industry": [
                    "consumer_goods_or_fmcg",
                    "engineering_and_manufacturing",
                    "retail"
                ],
                "industry_other": "",
                "business_activity": [
                    "manufacturer",
                    "supplier",
                    "wholesaler",
                    "other"
                ],
                "business_activity_other": "ba_abc_2",
                "iec": "1234567890",
                "gst": "22ABCDE1234F1Z6",
                "pan": "ABCDE1234F",
                "cin": "U67190TN2014PTC096978",
                "company_bio": None,
                "company_structure": None,
                "type": "customer",
                "address_details": {
                    "pincode": "123456",
                    "country": 1,
                    "state": 1,
                    "city": 1,
                    "street": "1234infisa56"
                },
                "organization": 1
            }
        return request_params


    # Request Params: Update a Customer with valid params set
    def put_update_customer_request_params():
        request_params = {
                "customer_details": {
                    "name": "Calvin",
                    "email": "calvino1u2@g.com",
                    "secondary_email": [
                        "calvincrew@g.com",
                        "calvinmum@g.com",
                        "calvinin@g.com"
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
                    "customer_type": "importer_or_exporter",
                    "designation": "accountant",
                    "expertise": "import",
                    "home_country": 1,
                    "home_company": 1,
                    "company": [
                        1,2,3
                    ],
                    "department": [
                        1,2,3
                    ],
                    "supervisor": [
                        1
                    ]
                },
                "user_companies_currency": [
                    {
                        "1": {
                            "air_currency": "JPY",
                            "lcl_currency": "INR",
                            "fcl_currency": "INR"
                        }
                    },
                    {
                        "2": {
                            "air_currency": "INR",
                            "lcl_currency": "JPY",
                            "fcl_currency": "EUR"
                        }
                    },
                    {
                        "3": {
                            "air_currency": "PHP",
                            "lcl_currency": "EUR",
                            "fcl_currency": "JPY"
                        }
                    }
                ]
            }
        return request_params


    # Response Params: Get a List of Customer, Response params set
    def get_customer_list_response_params():
        response_params = [{
                "customer_data": {
                    "id": 3,
                    "name": "Calvin",
                    "email": "calvino1u3@g.com",
                    "secondary_email": ["calvincrew@g.com", "calvinmum@g.com", "calvinin@g.com"],
                    "contact_no": [{
                        "dial_code": "91",
                        "contact_no": 9819123456
                    }, {
                        "dial_code": "1",
                        "contact_no": 9819123455
                    }, {
                        "dial_code": "234",
                        "contact_no": 9819123454
                    }],
                    "landline_no_dial_code": "+91",
                    "landline_no": "9819123457",
                    "customer_type": "importer_or_exporter",
                    "designation": "accountant",
                    "expertise": "import",
                    "registration_token": None,
                    "token_date": None,
                    "is_super_admin": False,
                    "status": 1,
                    "home_country": 1,
                    "home_company": 1,
                    "company": [1, 2, 3],
                    "department": [1, 2, 3],
                    "supervisor": [1],
                    "client": []
                },
                "currency_profile_data": [{
                    "id": 8,
                    "entity_type": "customer",
                    "entity_id": 3,
                    "air_currency": "INR",
                    "lcl_currency": "INR",
                    "fcl_currency": "INR",
                    "company": 1
                }, {
                    "id": 9,
                    "entity_type": "customer",
                    "entity_id": 3,
                    "air_currency": "INR",
                    "lcl_currency": "EUR",
                    "fcl_currency": "EUR",
                    "company": 2
                }, {
                    "id": 10,
                    "entity_type": "customer",
                    "entity_id": 3,
                    "air_currency": "EUR",
                    "lcl_currency": "INR",
                    "fcl_currency": "EUR",
                    "company": 3
                }]
            }, {
                "customer_data": {
                    "id": 2,
                    "name": "Calvin",
                    "email": "calvino1u2@g.com",
                    "secondary_email": ["calvincrew@g.com", "calvinmum@g.com", "calvinin@g.com"],
                    "contact_no": [{
                        "dial_code": "91",
                        "contact_no": 9819123456
                    }, {
                        "dial_code": "1",
                        "contact_no": 9819123455
                    }, {
                        "dial_code": "234",
                        "contact_no": 9819123454
                    }],
                    "landline_no_dial_code": "+91",
                    "landline_no": "9819123457",
                    "customer_type": "importer_or_exporter",
                    "designation": "accountant",
                    "expertise": "import",
                    "registration_token": None,
                    "token_date": None,
                    "is_super_admin": False,
                    "status": 1,
                    "home_country": 1,
                    "home_company": 1,
                    "company": [1, 2, 3],
                    "department": [1, 2, 3],
                    "supervisor": [1],
                    "client": []
                },
                "currency_profile_data": [{
                    "id": 5,
                    "entity_type": "customer",
                    "entity_id": 2,
                    "air_currency": "INR",
                    "lcl_currency": "INR",
                    "fcl_currency": "INR",
                    "company": 1
                }, {
                    "id": 6,
                    "entity_type": "customer",
                    "entity_id": 2,
                    "air_currency": "INR",
                    "lcl_currency": "EUR",
                    "fcl_currency": "EUR",
                    "company": 2
                }, {
                    "id": 7,
                    "entity_type": "customer",
                    "entity_id": 2,
                    "air_currency": "EUR",
                    "lcl_currency": "INR",
                    "fcl_currency": "EUR",
                    "company": 3
                }]
            }, {
                "customer_data": {
                    "id": 1,
                    "name": "Calvin",
                    "email": "calvino1u1@g.com",
                    "secondary_email": ["calvincrew@g.com", "calvinmum@g.com", "calvinin@g.com"],
                    "contact_no": [],
                    "landline_no_dial_code": "+91",
                    "landline_no": "9819123457",
                    "customer_type": "importer_or_exporter",
                    "designation": "accountant",
                    "expertise": "import",
                    "registration_token": None,
                    "token_date": None,
                    "is_super_admin": True,
                    "status": 1,
                    "home_country": 2,
                    "home_company": 1,
                    "company": [1],
                    "department": [5],
                    "supervisor": [],
                    "client": []
                },
                "currency_profile_data": [{
                    "id": 2,
                    "entity_type": "customer",
                    "entity_id": 1,
                    "air_currency": "USD",
                    "lcl_currency": "USD",
                    "fcl_currency": "USD",
                    "company": 1
                }]
            }]
        return response_params


    # Response Params: Get a List of Customer with pagination, Response params set
    def get_customer_list_pagination_response_params():
        response_params = [{
                "customer_data": {
                    "id": 1,
                    "name": "Calvin",
                    "email": "calvino1u1@g.com",
                    "secondary_email": ["calvincrew@g.com", "calvinmum@g.com", "calvinin@g.com"],
                    "contact_no": [],
                    "landline_no_dial_code": "+91",
                    "landline_no": "9819123457",
                    "customer_type": "importer_or_exporter",
                    "designation": "accountant",
                    "expertise": "import",
                    "registration_token": None,
                    "token_date": None,
                    "is_super_admin": True,
                    "status": 1,
                    "home_country": 2,
                    "home_company": 1,
                    "company": [1],
                    "department": [5],
                    "supervisor": [],
                    "client": []
                },
                "currency_profile_data": [{
                    "id": 2,
                    "entity_type": "customer",
                    "entity_id": 1,
                    "air_currency": "USD",
                    "lcl_currency": "USD",
                    "fcl_currency": "USD",
                    "company": 1
                }]
            }]
        return response_params


    # Response Params: Get a Customer Detail, Response params set
    def get_customer_detail_response_params():
        response_params = {
                "customer_data": {
                    "id": 2,
                    "name": "Calvin",
                    "email": "calvino1u2@g.com",
                    "secondary_email": ["calvincrew@g.com", "calvinmum@g.com", "calvinin@g.com"],
                    "contact_no": [{
                        "dial_code": "91",
                        "contact_no": 9819123456
                    }, {
                        "dial_code": "1",
                        "contact_no": 9819123455
                    }, {
                        "dial_code": "234",
                        "contact_no": 9819123454
                    }],
                    "landline_no_dial_code": "+91",
                    "landline_no": "9819123457",
                    "customer_type": "importer_or_exporter",
                    "designation": "accountant",
                    "expertise": "import",
                    "registration_token": None,
                    "token_date": None,
                    "is_super_admin": False,
                    "status": 1,
                    "home_country": 1,
                    "home_company": 1,
                    "company": [1, 2, 3],
                    "department": [1, 2, 3],
                    "supervisor": [1],
                    "client": []
                },
                "currency_profile_data": [{
                    "id": 5,
                    "entity_type": "customer",
                    "entity_id": 2,
                    "air_currency": "INR",
                    "lcl_currency": "INR",
                    "fcl_currency": "INR",
                    "company": 1
                }, {
                    "id": 6,
                    "entity_type": "customer",
                    "entity_id": 2,
                    "air_currency": "INR",
                    "lcl_currency": "EUR",
                    "fcl_currency": "EUR",
                    "company": 2
                }, {
                    "id": 7,
                    "entity_type": "customer",
                    "entity_id": 2,
                    "air_currency": "EUR",
                    "lcl_currency": "INR",
                    "fcl_currency": "EUR",
                    "company": 3
                }]
            }
        return response_params


    # Request params: Vendor registration request params contain personal detail with valid data
    def post_vendor_registration_personal_details_request_set():
        request_params = {
            "vendor_details": {
                'name': 'shiv1',
                'email': 'shiv_fct72@g.com',
                'secondary_email': ['shivs@g.com', 'shivmum@g.com', 'shivls@g.com'],
                'contact_no': None,
                'landline_no_dial_code': '+91',
                'landline_no': '9819123457',
                "vendor_type": 'freight-forwarder',
                "company_name": "fct85",
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


    def post_invite_vendor_request_set():
        request_params = {
            "name": "fct861 Name",
            "email": "shiv_fct72@g.com",
            "contact_no": None,
            "landline_no_dial_code": "+91",
            "landline_no": "9819123457",
            "company_name": "fct85"
        }
        return request_params


    def get_vendor_client_list_request_set():
        request_params = [{
            "id": 1,
            "name": "fct861 Name",
            "email": "shiv_fct72@g.com",
            "contact_no": None,
            "landline_no_dial_code": "+91",
            "landline_no": "9819123457",
            "company_name": "canon_o1cA",
            "status": 2,
            "customer_company": 1,
            "customer": 1,
            "vendor_company": 2,
            "vendor": 1,
            "action": "PENDING"
        }]
        return request_params


    def get_invite_vendor_list_request_set():
        request_params = [{
            "id": 1,
            "name": "fct861 Name",
            "email": "shiv_fct72@g.com",
            "contact_no": None,
            "landline_no_dial_code": "+91",
            "landline_no": "9819123457",
            "company_name": "fct85",
            "status": 2,
            "customer_company": 1,
            "customer": 1,
            "vendor_company": 2,
            "vendor": 1,
            "action": "PENDING"
        }]
        return request_params
