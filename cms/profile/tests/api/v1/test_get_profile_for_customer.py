from customer.models.customer import Customer
from profile.tests.api.v1.request_response_params import ProfileRequestParams
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from utils.helpers import encode_data
import json

client = APIClient()

class GetProfileCustomer(APITestCase):

    fixtures = ProfileRequestParams.get_seed_data_list()

    def api_authentication(self):
        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)

    def setUp(self):
        # customer registration
        self.add_customer_registration_api_url = ProfileRequestParams.api_url() + '/api/v1/customer/'
        self.customer_register_params = ProfileRequestParams.post_customer_registration_personal_details_request_set()
        response=self.client.post(self.add_customer_registration_api_url, data=self.customer_register_params, format='json')
        api_response_json = json.loads(response.content)
        
        # add customer url and params set
    
        customer_name = self.customer_register_params['customer_details']['name']
        customer = list(Customer.find_by(multi=True, name=customer_name).values_list('id','home_company','supervisor'))[0]

        self.customer_id, self.company_id,self.supervisor =customer
        encoded_email = encode_data(self.customer_register_params['customer_details']['email'])
        self.customer_add_post_api_url = ProfileRequestParams.api_url() + '/api/v1/company/'+ str(self.company_id) +'/customer/'

        # customer activation
        response = self.client.get(api_response_json['data'], format='json')
        self.final_api_response_json = json.loads(response.content)

        # login customer
        response = self.client.post(ProfileRequestParams.api_url() + '/user/login/', data=ProfileRequestParams.login_valid_request_params_for_customer(), format='json')
        api_response_json = json.loads(response.content)
        self.jwt_token = api_response_json['data'][0]['token']
        self.api_authentication()

        # add  new customer
        self.params = ProfileRequestParams.post_add_customer_valid_request_set()
        self.customer_name = self.params['customer_details']['name']
       
        response = client.post(self.customer_add_post_api_url, data=self.params, format='json')
        self.api_response_json = json.loads(response.content)

    def test_get_profile(self):
        customer = list(Customer.find_by(multi=True, name=self.customer_name).values_list('id','home_company','registration_token'))[0]
        self.customer_id, self.company_id,self.registration_token=customer
        
        token_hash = self.params['customer_details']['email'] + '__' + 'customer' +'__'
        token_hash = encode_data(token_hash + str(self.registration_token))

        self.set_profile_api_url=ProfileRequestParams.api_url() + '/api/v1/profile/'+ token_hash
        response = client.get(self.set_profile_api_url, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('user data retrieve successfully.', api_response_json['message'])
        self.assertEqual(200, api_response_json['code'])

    def test_invalid_link(self):
        get_profile_wih_invalid_link= ProfileRequestParams.api_url() + '/api/v1/profile/c2hpdk9BQ0EyQGcuY29tX19jdXN0b21lcl'
        response = self.client.get(get_profile_wih_invalid_link, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Invalid Token. Please contact admin for your account activation and other queries.', api_response_json['message'])
        self.assertEqual('BF0004', api_response_json['code'])