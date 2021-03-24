class CompanyExpertiseRequestParams:

    @staticmethod
    def api_url():
        return 'http://localhost:8000/'

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

    def company_expertise_post_set(self):
        request_params = {
        "transport_mode": "AE",
        "container_type": [],
        "hazardous": False,
        "instant_quotes": False,
        "trade_lanes": [
            1
        ],
        "from_trade_lanes": [],
        "to_trade_lanes": [],
        "temperature_controlled": True,
        "commodity": [
            1,
            2
        ]}
        return request_params
    def company_expertise_get(self):
        company_expertise_keys = [
            "id",
            "status",
            "transport_mode",
            "container_type",
            "hazardous",
            "instant_quotes",
            "company",
            "trade_lanes",
            "from_trade_lanes",
            "to_trade_lanes",
            "commodity"
            ]
        return company_expertise_keys


    def company_expertise_post_second_set(self):
        request_params = CompanyExpertiseRequestParams.company_expertise_post_set(self) 
        request_params['transport_mode']= "LCLI"
        return request_params

    def post_transport_mode_invalid_transport_mode_set(self):
        request_params = CompanyExpertiseRequestParams.company_expertise_post_set(self) 
        request_params['transport_mode']= "LCLIT"
        return request_params


    def company_expertise_invalid_container_type_fcl_set(self):
        request_params = CompanyExpertiseRequestParams.company_expertise_post_set(self)
        request_params['transport_mode'] = "FCLI"
        request_params['container_type'] = None
        return request_params

    def post_company_expertise_invalid_third_country(self):
        request_params =CompanyExpertiseRequestParams.company_expertise_post_set(self)
        request_params['transport_mode'] = "ATC"
        request_params['from_trade_lanes'] = None
        request_params['to_trade_lanes'] = None
        return request_params

    def post_company_expertise_trade_lanes_required(self):
        request_params = CompanyExpertiseRequestParams.company_expertise_post_set(self)
        request_params['transport_mode'] = "AI"
        request_params['trade_lanes'] = None
        return request_params

    def post_company_expertise_blank_commodity(self):
        request_params = CompanyExpertiseRequestParams.company_expertise_post_set(self)
        request_params['transport_mode'] = "AI"
        request_params['commodity'] = None
        return request_params

    def post_company_expertise_blank_list_commodity(self):
        request_params = CompanyExpertiseRequestParams.company_expertise_post_set(self)
        request_params['transport_mode'] = "AI"
        request_params['commodity'] = []
        return request_params


    def post_vendor_registration_personal_details_request_set():
        request_params = {
            "vendor_details": {
                'name': 'shiv1',
                'email': 'shivo1u1@g.com',
                'secondary_email': ['shivs@g.com', 'shivmum@g.com', 'shivls@g.com'],
                'contact_no': None,
                'landline_no_dial_code': '+91',
                'landline_no': '9819123457',
                "vendor_type": "courier",
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
    

    # Request params: Login credential with valid data for vendor
    def login_valid_request_params():
        request_params = {
                "email": "shivo1u1@g.com",
                "password": "apple",
                "account_type": "vendor"
            }
        return request_params