from customer.models.customer import Customer
from profile.tests.api.v1.request_response_params import ProfileRequestParams
from rest_framework.test import APITestCase,APIClient
from utils.helpers import encode_data
import json

client = APIClient()

class SetProfileCustomer(APITestCase):

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
        self.params = ProfileRequestParams.post_add_customer_valid_request_set()
        customer_name = self.customer_register_params['customer_details']['name']
        customer = list(Customer.find_by(multi=True, name=customer_name).values_list('id','home_company'))[0]
        self.customer_id, self.company_id =customer

        encoded_email = encode_data(self.customer_register_params['customer_details']['email'])
        self.add_customer_post_api_url = ProfileRequestParams.api_url() + '/api/v1/company/'+ str(self.company_id) +'/customer/'
      
        # customer activation
        response = client.get( api_response_json['data'], format='json')
        self.final_api_response_json = json.loads(response.content)

        # login customer
        response = client.post(ProfileRequestParams.api_url() + '/user/login/', data=ProfileRequestParams.login_valid_request_params_for_customer(), format='json')
        api_response_json = json.loads(response.content)

        self.jwt_token = api_response_json['data'][0]['token']
        self.api_authentication()

    def test_set_profile(self): 
        self.params['customer_details']['name']='surya'
        self.params['customer_details']['company'] = [4]
        self.params['customer_details']['home_company'] = 4
        self.params['customer_details']['department'] = [20]
        self.params['customer_details']['supervisor'] = [7]
        self.params['user_companies_currency']=[{"4": {"air_currency": "JPY","lcl_currency": "EUR","fcl_currency": "EUR"}}]
        response = client.post(self.add_customer_post_api_url, data= self.params, format='json')
        self.api_response_json = json.loads(response.content)

        self.customer_name = self.params['customer_details']['name']
        
        customer = list(Customer.find_by(multi=True, name=self.customer_name).values_list('id','home_company','registration_token'))[0]
        self.customer_id, self.company_id,self.registration_token=customer
        
        token_hash = self.params['customer_details']['email'] + '__' + 'customer' +'__'
        token_hash = encode_data(token_hash + str(self.registration_token))

        self.set_profile_api_url=ProfileRequestParams.api_url() + '/api/v1/profile/'+ token_hash

        response = self.client.put(self.set_profile_api_url,data=ProfileRequestParams.set_profile() ,format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('your profile has been updated successfully, please login to continue', api_response_json['message'])
        self.assertEqual(200, api_response_json['code'])
    
   
    def test_get_profile(self):
        response = client.post(self.add_customer_post_api_url, data=self.params, format='json')
        self.api_response_json = json.loads(response.content)

        self.customer_name = self.params['customer_details']['name']
        
        customer = list(Customer.find_by(multi=True, name=self.customer_name).values_list('id','home_company','registration_token'))[0]
        self.customer_id, self.company_id,self.registration_token=customer
        
        token_hash = self.params['customer_details']['email'] + '__' + 'customer' +'__'
        token_hash = encode_data(token_hash + str(self.registration_token))

        self.set_profile_api_url=ProfileRequestParams.api_url() + '/api/v1/profile/'+ token_hash

        response = self.client.put(self.set_profile_api_url,data=ProfileRequestParams.set_profile() ,format='json')

        response = self.client.get(self.set_profile_api_url, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual("You are already acivated. Please login to continue", api_response_json['message'])
        self.assertEqual('F0107', api_response_json['code'])
        self.assertEqual({}, api_response_json['data'])

    def test_get_profile_blank_password(self):
        self.params['customer_details']['name']='Ajay'
        self.params['customer_details']['company'] = [2]
        self.params['customer_details']['home_company'] =2
        self.params['customer_details']['department'] = [8]
        self.params['customer_details']['supervisor'] = [3]
        self.params['user_companies_currency']=[{"2": {"air_currency": "JPY","lcl_currency": "EUR","fcl_currency": "EUR"}}]

        response = client.post(self.add_customer_post_api_url, data=self.params, format='json')
        self.api_response_json = json.loads(response.content)

        self.customer_name = self.params['customer_details']['name']
        
        customer = list(Customer.find_by(multi=True, name=self.customer_name).values_list('id','home_company','registration_token'))[0]
        self.customer_id, self.company_id,self.registration_token=customer
        
        token_hash = self.params['customer_details']['email'] + '__' + 'customer' +'__'
        token_hash = encode_data(token_hash + str(self.registration_token))

        self.set_profile_api_url=ProfileRequestParams.api_url() + '/api/v1/profile/'+ token_hash


        response = self.client.put(self.set_profile_api_url,data=ProfileRequestParams.set_profile_blank_password(),format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual("password is required", api_response_json['message'])
        self.assertEqual('F0113', api_response_json['code'])
        self.assertEqual({}, api_response_json['data'])

    def test_get_profile_mismatch_password(self):
        self.params['customer_details']['name']='rani'
        self.params['customer_details']['company'] = [3]
        self.params['customer_details']['home_company'] = 3
        self.params['customer_details']['department'] = [12]
        self.params['customer_details']['supervisor'] = [5]
        self.params['user_companies_currency']=[{"3": {"air_currency": "JPY","lcl_currency": "EUR","fcl_currency": "EUR"}}]

        response = client.post(self.add_customer_post_api_url, data=self.params, format='json')
        self.api_response_json = json.loads(response.content)

        self.customer_name = self.params['customer_details']['name']
        
        customer = list(Customer.find_by(multi=True, name=self.customer_name).values_list('id','home_company','registration_token'))[0]
        self.customer_id, self.company_id,self.registration_token=customer
        
        token_hash = self.params['customer_details']['email'] + '__' + 'customer' +'__'
        token_hash = encode_data(token_hash + str(self.registration_token))

        self.set_profile_api_url=ProfileRequestParams.api_url() + '/api/v1/profile/'+ token_hash
        
        response = self.client.put(self.set_profile_api_url,data=ProfileRequestParams.set_profile_mismatch_password(),format='json')
        api_response_json = json.loads(response.content)
    
        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual("password did not match", api_response_json['message'])
        self.assertEqual('F0111', api_response_json['code'])
        self.assertEqual({}, api_response_json['data'])

    def test_set_profile_blank_confirm_password(self):
        self.params['customer_details']['name']='rahul'
        self.params['customer_details']['company'] = [5]
        self.params['customer_details']['home_company'] = 5
        self.params['customer_details']['department'] = [22]
        self.params['customer_details']['supervisor'] = [9]
        self.params['user_companies_currency']=[{"5": {"air_currency": "JPY","lcl_currency": "EUR","fcl_currency": "EUR"}}]

        response = client.post(self.add_customer_post_api_url, data=self.params, format='json')
        self.api_response_json = json.loads(response.content)

        self.customer_name = self.params['customer_details']['name']
        
        customer = list(Customer.find_by(multi=True, name=self.customer_name).values_list('id','home_company','registration_token'))[0]
        self.customer_id, self.company_id,self.registration_token=customer
        
        token_hash = self.params['customer_details']['email'] + '__' + 'customer' +'__'
        token_hash = encode_data(token_hash + str(self.registration_token))

        self.set_profile_api_url=ProfileRequestParams.api_url() + '/api/v1/profile/'+ token_hash

       
        response = self.client.put(self.set_profile_api_url,data=ProfileRequestParams.set_profile_blank_confirm_password(),format='json')
        api_response_json = json.loads(response.content)
    
        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual(" confirm password is required", api_response_json['message'])
        self.assertEqual('F0114', api_response_json['code'])
        self.assertEqual({}, api_response_json['data'])


    def test_set_profile_validation_on_landline_no_or_contact_no(self):
        self.params['customer_details']['name']='raina'
        self.params['customer_details']['company'] = [6]
        self.params['customer_details']['home_company'] = 6
        self.params['customer_details']['department'] = [27]
        self.params['customer_details']['supervisor'] = [11]
        self.params['user_companies_currency']=[{"6": {"air_currency": "JPY","lcl_currency": "EUR","fcl_currency": "EUR"}}]

        response = client.post(self.add_customer_post_api_url, data=self.params, format='json')
        self.api_response_json = json.loads(response.content)

        self.customer_name = self.params['customer_details']['name']
        
        customer = list(Customer.find_by(multi=True, name=self.customer_name).values_list('id','home_company','registration_token'))[0]
        self.customer_id, self.company_id,self.registration_token=customer
        
        token_hash = self.params['customer_details']['email'] + '__' + 'customer' +'__'
        token_hash = encode_data(token_hash + str(self.registration_token))

        self.set_profile_api_url=ProfileRequestParams.api_url() + '/api/v1/profile/'+ token_hash

        response = self.client.put(self.set_profile_api_url,data=ProfileRequestParams.set_profile_validation_on_contact_no(),format='json')
        api_response_json = json.loads(response.content)
    
        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual("Enter either contact no or landline no.", api_response_json['message'])
        self.assertEqual('F0118', api_response_json['code'])
        self.assertEqual({}, api_response_json['data'])