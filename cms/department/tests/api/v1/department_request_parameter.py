from django.conf import settings

class DepartmentRequestParameter:

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
                "secondary_email": ["shivs@g.com","shivmum@g.com","shivls@g.com"],
                "contact_no": None,
                "landline_no_dial_code": "+91",
                "landline_no": "9819123457",
                "customer_type": "impoter_or_exporter",
                "company_name": "fct_o1cA",
                "password": "qwerty",
                "designation": "accountant",
                "expertise": "import",
                "home_country": 1,
                "home_company": None
            }
        }
        return request_params

    # Request params: Add a customer with valid data
    def post_add_customer_valid_request_set(self):
        request_params = {
            "customer_details": {
                "name": "shiv",
                "email": "shivOACA2@g.com",
                "secondary_email": ["shivs@g.com","shivmum@g.com","shivls@g.com"],
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
                "customer_type": "impoter_or_exporter",
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
            "currency_profile_detail": {
                "air_currency": "INR",
                "lcl_currency": "INR",
                "fcl_currency": "INR"
            }
        }
        return request_params
    
    def post_department_set(self):
        request_params = {
            "name":"Department_test_1"
        }
        return request_params

    def post_department_second_set(self):
        request_params = {
            "name":"Department_test_2"
        }
        return request_params

    def post_department_name_already_exist(self):
        request_params = {
            "name":"Department_test_1"
        }
        return request_params

    def post_department_cant_be_blank(self):
        request_params = {
            "name":""
        }
        return request_params
    
    def department_get_request_keys(self):

        department_keys = [
            'id',
            'status',
            'name',
            'type',
            'company',
        ]

        return department_keys

    def department_update(self):
        request_params = {
            "name":"Department_updated"
        }
        return request_params