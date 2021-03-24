from django.conf import settings


class RequestResponseParams:

    @staticmethod
    def api_url():
        return settings.API_HOST

    # Request params: Login credential with valid data
    def login_valid_request_params():
        request_params = {
                "email": "calvino1u1@g.com",
                "password": "qwerty",
                "account_type": "customer"
            }
        return request_params

    # Response params: Customer List
    def after_login_get_customer_list_response_params():
        response_params = [{
                'customer_data': {
                    'id': 1,
                    'name': 'Calvin',
                    'email': 'calvino1u1@g.com',
                    'secondary_email': ['calvincrew@g.com', 'calvinmum@g.com', 'calvinin@g.com'],
                    'contact_no': [],
                    'landline_no_dial_code': '+91',
                    'landline_no': '9819123457',
                    'customer_type': 'impoter_or_exporter',
                    'designation': 'accountant',
                    'expertise': 'import',
                    'registration_token': None,
                    'token_date': None,
                    'is_super_admin': True,
                    'status': 1,
                    'home_country': 2,
                    'home_company': 1,
                    'company': [1],
                    'department': [5],
                    'supervisor': [],
                    'client': []
                },
                'currency_profile_data': [{
                    'id': 2,
                    'entity_type': 'customer',
                    'entity_id': 1,
                    'air_currency': 'USD',
                    'lcl_currency': 'USD',
                    'fcl_currency': 'USD',
                    'company': 1
                }]
            }]
        return response_params


    # Request Params: Change Password of a Customer with valid params set
    def put_change_password_customer_request_params():
        request_params = {
            "old_password": "qwerty",
            "new_password": "qwerty123"
        }
        return request_params


    # Request Params: Change Password of a Vendor with valid params set
    def put_change_password_vendor_request_params():
        request_params = {
            "old_password": "apple",
            "new_password": "apple123"
        }
        return request_params


    # Request Params: Create Forgot Password Link of a Customer with valid params set
    def put_create_forgot_password_customer_request_params():
        request_params = {
            "email": "calvino1u1@g.com",
            "account_type": "customer"
        }
        return request_params


    # Request Params: Create Forgot Password Link of a Vendor with valid params set
    def put_create_forgot_password_vendor_request_params():
        request_params = {
            "email": "shivo1u1@g.com",
            "account_type": "vendor"
        }
        return request_params


    # Request Params: Action Forgot Password Link with valid params set
    def put_action_forgot_password_request_params():
        request_params = {
            "new_password": "qwerty234"
        }
        return request_params