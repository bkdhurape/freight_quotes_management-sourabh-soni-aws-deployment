class BranchRequestParams:

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


    def post_branch_with_transport_mode_set(self):
        request_params = {
            "name": "Branch2",
            "country": 1,
            "state": [1],
            "city": [1],
            "region": [1],
            "minimum_weight":20,
            "maximum_weight":40,
            "weight_unit":"kg",
            "minimum_radius":10,
            "maximum_radius":100,
            "radius_unit":"km"
        }
        return request_params

    def post_transport_mode_set(self):
        request_params = {
          
            "transport_mode": "AI",
            "container_type": None,
            "hazardous": False,
            "instant_quotes": False,
            "trade_lanes":[1],
            "from_trade_lanes":[],
            "to_trade_lanes":[],
            "commodity": [1,2]
                            
        }
        return request_params

    def post_transport_mode_set_second_all(self):
        request_params = BranchRequestParams.post_transport_mode_set(self) 
        request_params['transport_mode']= "LCLI"
        return request_params

    def post_transport_mode_second_set(self):
        request_params = BranchRequestParams.post_transport_mode_set(self) 
        request_params['transport_mode']= "AI"
        return request_params

    def post_branch_with_transport_mode_set_secondset(self):
        request_params = BranchRequestParams.post_branch_with_transport_mode_set(self)
        request_params['name'] = "Branch_set_2"
        return request_params

    def post_transport_mode_invalid_container_type_air_set(self):
        request_params = BranchRequestParams.post_transport_mode_set(self)
        request_params['transport_mode'] = "AI"
        request_params['container_type'] = ["20GP"]
        return request_params

    def post_transport_mode_invalid_container_type_fcl_set(self):
        request_params = BranchRequestParams.post_transport_mode_set(self)
        request_params['transport_mode'] = "FCLI"
        request_params['container_type'] = None
        return request_params

    def post_transport_mode_invalid_third_country(self):
        request_params = BranchRequestParams.post_transport_mode_set(self)
        request_params['transport_mode'] = "ATC"
        request_params['from_trade_lanes'] = None
        request_params['to_trade_lanes'] = None
        return request_params

    def post_transport_mode_trade_lanes_required(self):
        request_params = BranchRequestParams.post_transport_mode_set(self)
        request_params['transport_mode'] = "AI"
        request_params['trade_lanes'] = None
        return request_params


    def post_branch_already_exists(self):
        request_params = BranchRequestParams.post_branch_with_transport_mode_set(self)
        request_params['name'] = "Branch_set_2"
        return request_params


    def branch_update(self):
        request_params = BranchRequestParams.post_branch_with_transport_mode_set(self)
        request_params['name'] = "Branch_updated"
        return request_params

    def post_branch_minimum_weight_required(self):
        request_params = BranchRequestParams.post_branch_with_transport_mode_set(self)
        request_params['minimum_weight'] = None
        return request_params

    def post_branch_maximum_weight_required(self):
        request_params = BranchRequestParams.post_branch_with_transport_mode_set(self)
        request_params['maximum_weight'] = None
        return request_params
    
    def post_branch_weight_unit_required(self):
        request_params = BranchRequestParams.post_branch_with_transport_mode_set(self)
        request_params['weight_unit'] = None
        return request_params
  

    def post_branch_maximum_weight_should_be_more_than_minimum_weight(self):
        request_params = BranchRequestParams.post_branch_with_transport_mode_set(self)
        request_params['maximum_weight'] = 10
        return request_params

    def post_branch_minimum_radius_required(self):
        request_params = BranchRequestParams.post_branch_with_transport_mode_set(self)
        request_params['minimum_radius'] = None
        return request_params

    def post_branch_maximum_radius_required(self):
        request_params = BranchRequestParams.post_branch_with_transport_mode_set(self)
        request_params['maximum_radius'] = None
        return request_params

    def post_branch_radius_unit_required(self):
        request_params = BranchRequestParams.post_branch_with_transport_mode_set(self)
        request_params['radius_unit'] = None
        return request_params
  
    def post_branch_maximum_radius_should_be_more_than_minimum_radius(self):
        request_params = BranchRequestParams.post_branch_with_transport_mode_set(self)
        request_params['maximum_radius'] = 10
        return request_params

    def post_branch_radius_should_be_positive_value(self):
        request_params = BranchRequestParams.post_branch_with_transport_mode_set(self)
        request_params['minimum_radius'] = -10
        return request_params

    def branch_get_request_keys():

        branch_keys = [
            'id',
            'status',
            'name',
            'is_head_branch',
            'company',
            'country',
            'parent',
            'state',
            'city',
            'region',
            'minimum_weight',
            'minimum_weight_kg',
            'maximum_weight',
            'maximum_weight_kg',
            'weight_unit',
            'minimum_radius',
            'minimum_radius_km',
            'maximum_radius',
            'maximum_radius_km',
            'radius_unit',

        ]

        return branch_keys

    def transport_details_key(self):

        transport_mode_keys = [
            "id",
            "status",
            "transport_mode",
            "container_type",
            "hazardous",
            "instant_quotes",
            "branch",
            "trade_lanes",
            "from_trade_lanes",
            "to_trade_lanes",
            "commodity"
            ]
        return transport_mode_keys

    def post_vendor_registration_personal_details_request_set():
        request_params = {
            "vendor_details": {
                'name': 'shiv1',
                'email': 'shivo1u1@g.com',
                'secondary_email': ['shivs@g.com', 'shivmum@g.com', 'shivls@g.com'],
                'contact_no': None,
                'landline_no_dial_code': '+91',
                'landline_no': '9819123457',
                "vendor_type": "transport-only",
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
    

    # Request params: Login credential with valid data
    def login_valid_request_params():
        request_params = {
                "email": "shivo1u1@g.com",
                "password": "apple",
                "account_type": "vendor"
            }
        return request_params