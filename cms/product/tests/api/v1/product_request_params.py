from django.conf import settings
from product.models.product import Product


class ProductRequestParams:

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
            'vendor/fixtures/vendor_type.json',
            'port/fixtures/port.json'
        ]
        return fixture_list


    # Request params: Login credential with valid data
    def login_valid_request_params():
        request_params = {
                "email": "shivo1u1@g.com",
                "password": "qwerty",
                "account_type": "customer"
            }
        return request_params

    # Request params: Customer registration request params contain personal detail with valid data
    def post_customer_registration_personal_details_request_set():
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
    def post_add_customer_valid_request_set():
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



    # Request params: Vendor type
    def post_product_request_set():
        request_params = {
            "name": "Product 1",
        	"transport_modes": ["Air","LCL"],
            "addresses": [{
        		"street": "Test Address 1",
        		"pincode": "400004",
        		"city": 1,
        		"country": 1,
        		"state": 1
        	}],
        	"airports": [1,2],
        	"seaports": [5,6]
        }
        return request_params

    # Request params: Vendor type
    def post_product_request_set2():
        request_params = {
        	"name": "Product 2",
            "addresses": [{
        		"street": "Test Address 2",
        		"pincode": "400004",
        		"city": 1,
        		"country": 1,
        		"state": 1
        	}],
        	"transport_modes": ["Air","LCL"],
        	"airports": [1,2],
        	"seaports": [5,6]
        }
        return request_params


    # Request params: Get a list of vendor
    def get_list_of_product_params_set():
        request_params = [{
            'id': 2,
            "name": "Product 2",
            "addresses": [{
                "id": 3,
        		"address1": "Test Address 2",
        		"pincode": "400004",
        		"city": 1,
        		"country": 1,
        		"state": 1
        	}],
        	"transport_modes": ["Air","LCL"],
            "entity": 1,
        	"airports": [1,2],
        	"seaports": [],
            'status': 1
        },{
            'id': 1,
            "name": "Product 1",
            "addresses": [{
                "id": 2,
        		"address1": "Test Address 1",
        		"pincode": "400004",
        		"city": 1,
        		"country": 1,
        		"state": 1
        	}],
        	"transport_modes": ["Air","LCL"],
            "entity": 1,
        	"airports": [1,2],
        	"seaports": [],
            'status': 1
        }]
        return request_params

    # Request params: Get vendor type details by ID
    def get_product_by_id_params_set():
        request_params = {
            'id': 2,
            "name": "Product 2",
            "addresses": [{
                "id": 3,
        		"address1": "Test Address 2",
        		"pincode": "400004",
        		"city": 1,
        		"country": 1,
        		"state": 1
        	}],
        	"transport_modes": ["Air","LCL"],
            "entity": 1,
        	"airports": [1,2],
        	"seaports": [],
            'status': 1
        }
        return request_params
