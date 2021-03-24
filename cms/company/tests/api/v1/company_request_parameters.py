from company.models.organization import Organization
from django.conf import settings


class CompanyRequestParams:

    @staticmethod
    def api_url():
        return settings.API_HOST

    def get_seed_data_list():
        fixture_list = [
            'country/fixtures/country.json',
            'state/fixtures/state.json',
            'city/fixtures/city.json'

        ]
        return fixture_list
    def company_get_id(self):
        company_key={
        'id':1, 
        'status': 1,
        'name': 'fct_o1cA',
        'company_type': 'sole_proprietorship',
        'industry': [], 
        'industry_other': None, 
        'business_activity': [], 
        'business_activity_other': None, 
        'iec': None,
        'gst': None, 
        'pan': None,
        'cin': None, 
        'company_bio': None,
        'company_structure': None, 
        'type': 'vendor', 
        'incorporation_year': None, 
        'organization':1, 
        'address_details': {
            'id': 1, 
            'address2': None, 
            'state': {
                'id': 1,
                'name': 'Punjab', 
                'country': 1},
            'city': {
                'id': 1, 
                'name': 'Ludhiana',
                 'state': 1},
            'country': {
                'id': 1, 
                'name': 'India',
                'code': 'IN', 
                'currency_code': 'INR'
                }, 
                'pincode': '123456', 
                'type': None,
                'entity_type': 'company',
                'entity_id': 1, 
                'street': '1234infisa56'
            }
        }
            
        return company_key
    def company_get_all(self):
        company_key=[{
        'id':1, 
        'status': 1,
        'name': 'fct_o1cA',
        'company_type': 'sole_proprietorship',
        'industry': [], 
        'industry_other': None, 
        'business_activity': [], 
        'business_activity_other': None, 
        'iec': None,
        'gst': None, 
        'pan': None,
        'cin': None, 
        'company_bio': None,
        'company_structure': None, 
        'type': 'vendor', 
        'incorporation_year': None, 
        'organization': 1, 
        'address_details': {
            'id': 1, 
            'address2': None, 
            'state': {
                'id': 1,
                'name': 'Punjab', 
                'country': 1},
            'city': {
                'id': 1, 
                'name': 'Ludhiana',
                 'state': 1},
            'country': {
                'id': 1, 
                'name': 'India',
                'code': 'IN', 
                'currency_code': 'INR'
                }, 
                'pincode': '123456', 
                'type': None,
                'entity_type': 'company',
                'entity_id': 1, 
                'street': '1234infisa56'
            }
        }]
            
        return company_key

    def login_valid_request_params():
        request_params = {
                "email": "calvino1u1@g.com",
                "password": "qwerty",
                "account_type": "customer"
            }
        return request_params

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


    def create_company_valid_response():
        request_response = {
            "name": "company_o1cA",
            "company_type": "sole_proprietorship",
            "industry": ["consumer_goods_or_fmcg", "engineering_and_manufacturing", "retail"],
            "business_activity": ["manufacturer", "supplier", "wholesaler"],
            "iec": "1234567890",
            "gst": "22ABCDE1234F1Z6",
            "pan": "ABCDE1234F",
            "cin": "U67190TN2014PTC096978",
            "company_bio": None,
            "company_structure": None,
            "type": "customer",
            "registered_address": "kurla",
            "contact_address": "dadar"
        }
        return request_response

    def create_company_valid_response():
        organization = Organization.objects.create(name='fc')
        organization.save()
        organization_id = organization.id
        request_response = {
            "name": "company_test_i11dia",
            "company_type": "sole_proprietorship",
            "company_bio": "bio",
            "company_structure": "company_structure",
            "industry": ["other"],
            "industry_other": "hekko",
            "business_activity": ["manufacturer", "supplier", "wholesaler"],
            "business_activity_other": "",
            "iec": 1233214567,
            "pan": "asdfg2344n",
            "gst": "12ABCDE1234A1Z1",
            "cin": "U67190TN2014PTC096978",
            "annual_revenue": 234,
            "organization": organization_id,
            "type": "customer",
            "address_details": {
                'id':1,
                "street": "street123",
                "country":2,
                "city": 1,
                "state": 1,
                "pincode": "1234567"

            },
            "annaul_logistic_spend_currency": "USD",
            "annual_logistic_spend": 3000,
            "annual_air_shipments": 300,
            "annual_lcl_shipments": 300,
            "annual_fcl_shipments": 300,
            "total_shipments": 900,
            "annual_air_volume": 300,
            "annual_lcl_volume": 300,
            "annual_fcl_volume": 300,
            "annual_revenue_currency": "USD",
            "annual_revenue": 2000,
            "air_currency": "usd",
            "fcl_currency": "usd",
            "lcl_currency": "usd"
        }

        return request_response

    def create_company_with_Blank_street():
        request_response = CompanyRequestParams.create_company_valid_response()
        request_response['name'] = "company_test_01"
        request_response['address_details']['street'] = ""
        return request_response

    def create_company_with_null_street():
        request_response = CompanyRequestParams.create_company_valid_response()
        request_response['name'] = "company_test_02"
        request_response["address_details"]["street"] = None
        return request_response

    def create_company_with_null_country():
        request_response = CompanyRequestParams.create_company_valid_response()
        request_response['name'] = "company_test_03"
        request_response['address_details']['id']=10
        request_response['address_details']['country'] = None
        return request_response
    

    def update_company_with_another_country():
        request_response = CompanyRequestParams.create_company_valid_response()
        request_response['name'] = "company_test_03"
        request_response['address_details']['id']=6
        request_response['address_details']['country']=2
        return request_response

    def create_or_update_company_blank_address_details():
        organization = Organization.objects.create(name='fcct')
        organization.save()
        organization_id = organization.id
        request_response = {
            "name": "company_o1cb",
            "company_type": "sole_proprietorship",
            "industry": ["consumer_goods_or_fmcg", "engineering_and_manufacturing", "retail"],
            "business_activity": ["manufacturer", "supplier", "wholesaler"],
            "business_activity_other": "",
            "industry_other": "",
            "iec": "1234567890",
            "gst": "22ABCDE1234F1Z6",
            "pan": "ABCDE1234F",
            "cin": "U67190TN2014PTC096978",
            "company_bio": None,
            "company_structure": None,
            "type": "customer",
            "organization": organization_id}
        return request_response

    def get_all_company_based_on_organization_id():
        request_params = [{
            "id": 1,
            "name": "company_test_i11dia"
        }]
        return request_params

    def create_company_with_defaut_currency_based_on_home_country():
        organization = Organization.objects.create(name='fc')
        organization.save()
        organization_id = organization.id
        request_response = {
            "name": "company_test_0001",
            "company_type": "sole_proprietorship",
            "company_bio": "bio",
            "company_structure": "company_structure",
            "industry": ["other"],
            "industry_other": "hekko",
            "business_activity": ["manufacturer", "supplier", "wholesaler"],
            "business_activity_other": "",
            "iec": 1233214567,
            "pan": "asdfg2344n",
            "gst": "12ABCDE1234A1Z1",
            "cin": "U67190TN2014PTC096978",
            "customer_type":"importer_or_exporter",
            "annual_revenue": 234,
            "organization": organization_id,
            "type": "customer",
            "address_details": {
                "street": "street123",
                "country": 1,
                "city": 1,
                "state": 1,
                "pincode": "1234567"

            },
            "annaul_logistic_spend_currency": "USD",
            "annual_logistic_spend": 3000,
            "annual_air_shipments": 300,
            "annual_lcl_shipments": 300,
            "annual_fcl_shipments": 300,
            "total_shipments": 900,
            "annual_air_volume": 300,
            "annual_lcl_volume": 300,
            "annual_fcl_volume": 300,
            "annual_revenue_currency": "USD",
            "annual_revenue": 2000
        }
        return request_response
    
    def create_company_valid_response_other_than_country_india():
        organization = Organization.objects.create(name='fc')
        organization.save()
        organization_id = organization.id
        request_response = {
            "name": "company_test_i11dia",
            "company_type": "sole_proprietorship",
            "company_bio": "bio",
            "company_structure": "company_structure",
            "industry": ["other"],
            "industry_other": "hekko",
            "business_activity": ["manufacturer", "supplier", "wholesaler"],
            "business_activity_other": "",
            "annual_revenue": 234,
            "organization": organization_id,
            "type": "customer",
            "address_details": {
                "street": "street123",
                "country": 2,
                "city": 1,
                "state": 1,
                "pincode": "1234567"

            },
            "annaul_logistic_spend_currency": "USD",
            "annual_logistic_spend": 3000,
            "annual_air_shipments": 300,
            "annual_lcl_shipments": 300,
            "annual_fcl_shipments": 300,
            "total_shipments": 900,
            "annual_air_volume": 300,
            "annual_lcl_volume": 300,
            "annual_fcl_volume": 300,
            "annual_revenue_currency": "USD",
            "annual_revenue": 2000,
            "air_currency": "usd",
            "fcl_currency": "usd",
            "lcl_currency": "usd"
        }

        return request_response


    def create_company_with_blank_gst_when_country_is_india():
        request_params=CompanyRequestParams.create_company_with_defaut_currency_based_on_home_country()
        request_params['gst']=None
        return request_params

    def create_company_with_blank_cin_when_country_is_india():
        request_params=CompanyRequestParams.create_company_with_defaut_currency_based_on_home_country()
        request_params['cin']=None 
        return request_params

    def create_company_with_blank_pan_when_country_is_india():
        request_params=CompanyRequestParams.create_company_with_defaut_currency_based_on_home_country()
        request_params['pan']=None
        return request_params

    def create_company_with_blank_iec_when_country_is_india():
        request_params=CompanyRequestParams.create_company_with_defaut_currency_based_on_home_country()
        request_params['iec']=None
        return request_params

    def create_company_with_invalid_iec_when_country_is_india():
        request_params=CompanyRequestParams.create_company_with_defaut_currency_based_on_home_country()
        request_params['iec']=12344
        return request_params

    def create_company_with_invalid_gst_when_country_is_india():
        request_params=CompanyRequestParams.create_company_with_defaut_currency_based_on_home_country()
        request_params['gst']="aserfg"
        return request_params

    def create_company_with_invalid_pan_when_country_is_india():
        request_params=CompanyRequestParams.create_company_with_defaut_currency_based_on_home_country()
        request_params['pan']="abcde" 
        return request_params
    
    def create_company_with_invalid_cin_when_country_is_india():
        request_params=CompanyRequestParams.create_company_with_defaut_currency_based_on_home_country()
        request_params['cin']="12345" 
        return request_params

    def add_new_company_for_vendor():
        organization = Organization.objects.create(name='fc')
        organization.save()
        organization_id = organization.id
        request_response = {
        "name":"company_test_01213312",
        "company_type": "sole_proprietorship",
        "gst":"12ABCDE1234A1Z1",
        "pan": "asdfg2344o",
        "cin": "U67190TN2014PTC096978",
        "type": "vendor",
        "organization":organization_id,
        "incorporation_year":1996,
        "address_details": {
            "pincode": 123456,
            "country":1,
            "state":1,
            "city": 1,
            "street": "k11111urla"
        }
        }
        return request_response

    def update_new_company_for_vendor():
        organization = Organization.objects.create(name='fc')
        organization.save()
        organization_id = organization.id
        request_response = {
        "name":"company_test_01213312",
        "company_type": "sole_proprietorship",
        "gst":"12ABCDE1234A1Z1",
        "pan": "asdfg2344o",
        "cin": "U67190TN2014PTC096978",
        "type": "vendor",
        "organization":organization_id,
        "incorporation_year":1996,
        "address_details": {
            "id":2,
            "pincode": 123456,
            "country":1,
            "state":1,
            "city": 1,
            "street": "k11111urla"
        }
        }
        return request_response

    def update_company_with_Blank_street_for_vendor():
        request_response = CompanyRequestParams.update_new_company_for_vendor()
        request_response['name'] = "company_test_01"
        request_response['address_details']['street'] = ""
        return request_response

    def update_company_with_null_street_for_vendor():
        request_response = CompanyRequestParams.update_new_company_for_vendor()
        request_response['name'] = "company_test_02"
        request_response["address_details"]["street"] = None
        return request_response

    def update_company_with_null_country_for_vendor():
        request_response = CompanyRequestParams.update_new_company_for_vendor()
        request_response['name'] = "company_test_03"
        request_response['address_details']['id'] = 10
        request_response['address_details']['country'] = None
        return request_response
    

    def update_company_with_another_country_for_vendor():
        request_response = CompanyRequestParams.update_new_company_for_vendor()
        request_response['name'] = "company_test_03"
        request_response['address_details']['id'] = 6
        request_response['address_details']['country'] = 2

        return request_response



    def create_company_with_invalid_incorporation_year_with_string_for_vendor():
        request_params=CompanyRequestParams.update_new_company_for_vendor()
        request_params['incorporation_year']="rtyujj" 
        return request_params

    def create_company_with_invalid_incorporation_year_with_less_year_for_vendor():
        request_params=CompanyRequestParams.add_new_company_for_vendor()
        request_params['incorporation_year']=1111
        return request_params

    def create_company_with_invalid_incorporation_year_with_more_than_current_year_for_vendor():
        request_params=CompanyRequestParams.add_new_company_for_vendor()
        request_params['incorporation_year']=19968
        return request_params

    def create_company_with_blank_gst_when_country_is_india_for_vendor():
        request_params=CompanyRequestParams.add_new_company_for_vendor()
        request_params['gst']=None
        return request_params

    def create_company_with_blank_cin_when_country_is_india_for_vendor():
        request_params=CompanyRequestParams.add_new_company_for_vendor()
        request_params['cin']=None 
        return request_params

    def create_company_with_blank_pan_when_country_is_india_for_vendor():
        request_params=CompanyRequestParams.add_new_company_for_vendor()
        request_params['pan']=None
        return request_params

    def create_company_with_invalid_gst_when_country_is_india_for_vendor():
        request_params=CompanyRequestParams.add_new_company_for_vendor()
        request_params['gst']="aserfg"
        return request_params

    def create_company_with_invalid_pan_when_country_is_india_for_vendor():
        request_params=CompanyRequestParams.add_new_company_for_vendor()
        request_params['pan']="abcde" 
        return request_params
    
    def create_company_with_invalid_cin_when_country_is_india_for_vendor():
        request_params=CompanyRequestParams.add_new_company_for_vendor()
        request_params['cin']="12345" 
        return request_params

    def create_company_other_than_country_india():
        organization = Organization.objects.create(name='fc')
        organization.save()
        organization_id = organization.id
        request_response = {
        "name": "company_test_01213312",
        "company_type": "sole_proprietorship",
        "gst":"12ABCDE1234A1Z1",
        "pan": "asdfg2344o",
        "cin": "U67190TN2014PTC096978",
        "type": "vendor",
        "organization":organization_id,
        "incorporation_year":1996,
        "address_details": {
            "pincode": 123456,
            "country":2,
            "state":1,
            "city": 1,
            "street": "k11111urla"
        }
        }
        return request_response
