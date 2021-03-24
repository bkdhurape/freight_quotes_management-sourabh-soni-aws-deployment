from customer.models.customer import Customer
from profile.tests.api.v1.request_response_params import ProfileRequestParams
from rest_framework.test import APITestCase
from utils.helpers import encode_data
import json

class TokenExpiredLinkCustomer(APITestCase):

    fixtures = ProfileRequestParams.get_seed_data_list()

    def setUp(self): 

        # customer registration
        self.add_customer_registration_api_url = ProfileRequestParams.api_url() + '/api/v1/customer/'
        self.customer_register_params = ProfileRequestParams.post_customer_registration_personal_details_request_set()
        response=self.client.post(self.add_customer_registration_api_url, data=self.customer_register_params, format='json')
        self.api_response_json = json.loads(response.content)
        
        # add customer url and params set
        self.params = ProfileRequestParams.post_add_customer_valid_request_set()
        customer_name = self.customer_register_params['customer_details']['name']
        customer = list(Customer.find_by(multi=True, name=customer_name).values_list('id','home_company'))[0]
        self.customer_id, self.company_id =customer
        encoded_email = encode_data(self.customer_register_params['customer_details']['email'])
        self.customer_add_post_api_url = ProfileRequestParams.api_url() + '/api/v1/company/'+ str(self.company_id) +'/customer/'

        # customer activation
        response = self.client.get(self.api_response_json['data'], format='json')
        self.final_api_response_json = json.loads(response.content)

        # login customer
        response = self.client.post(ProfileRequestParams.api_url() + '/user/login/', data=ProfileRequestParams.login_valid_request_params_for_customer(), format='json')
        api_response_json = json.loads(response.content)

    def test_get_profile(self):
        customer_register_params = ProfileRequestParams.post_add_customer_valid_request_set()
        response = self.client.post(self.customer_add_post_api_url, data=self.params, format='json')
        self.api_response_json = json.loads(response.content)
        
        response = self.client.get(self.api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Your activation link has been expired. Please click here to resend the activation link or Contact admin for any other queries.', api_response_json['message'])
        self.assertEqual(200, api_response_json['code'])


    def test_resend_link(self):
        self.params['user_companies_currency']=[{"2": {"air_currency": "JPY","lcl_currency": "EUR","fcl_currency": "EUR"}}]
        self.params['customer_details']['company'] = [2]
        self.params['customer_details']['home_company'] = 2
        self.params['customer_details']['department'] = [8]
        self.params['customer_details']['supervisor'] = [3]

        response = self.client.post(self.customer_add_post_api_url, data=self.params, format='json')
        self.api_response_json = json.loads(response.content)
    
        response = self.client.get(self.api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)
        
        response = self.client.get(api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Resend mail sent successfully', api_response_json['message'])
        self.assertEqual(200, api_response_json['code'])