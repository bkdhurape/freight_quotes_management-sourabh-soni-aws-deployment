from profile.tests.api.v1.request_response_params import ProfileRequestParams
from rest_framework.test import APITestCase
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
import json

class TokenExpiredLinkVendor(APITestCase):

    fixtures = ProfileRequestParams.get_seed_data_list()

    def setUp(self):  
        self.vendor_post_api_url = ProfileRequestParams.api_url() + '/api/v1/vendor/'
        self.vendor_register_params = ProfileRequestParams.post_vendor_registration_personal_details_request_set()
        self.params = ProfileRequestParams.post_add_vendor_valid_request_set()

        # vendor registration
        response = self.client.post(self.vendor_post_api_url, data=self.vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        vendor_name = self.vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(multi=True, name=vendor_name).values_list('id','home_company'))[0]
        self.vendor_id, self.company_id = vendor

        # vendor activation
        encoded_email = encode_data(self.vendor_register_params['vendor_details']['email'])
        test_vendor_send_activation_link_api_url = ProfileRequestParams.api_url() + '/api/v1/company/'+ str(self.company_id) +'/vendor/send_activation_link/' + encoded_email

        response = self.client.get(test_vendor_send_activation_link_api_url, format='json')
        self.final_api_response_json = json.loads(response.content)
        self.vendor_add_post_api_url = ProfileRequestParams.api_url() + '/api/v1/company/'+ str(self.company_id) +'/vendor/'

        response = self.client.get(self.final_api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)
        
        # login vendor
        response = self.client.post(ProfileRequestParams.api_url() + '/user/login/', data=ProfileRequestParams.login_valid_request_params(), format='json')
        api_response_json = json.loads(response.content)

    def test_get_profile(self):
        response = self.client.post(self.vendor_add_post_api_url, data=self.params, format='json')
        self.api_response_json = json.loads(response.content)
        
        response = self.client.get(self.api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Your activation link has been expired. Please click here to resend the activation link or Contact admin for any other queries.', api_response_json['message'])
        self.assertEqual(200, api_response_json['code'])


    def test_resend_link(self):
        self.params['vendor_details']['company'] = [2]
        self.params['vendor_details']['home_company'] = 2
        self.params['vendor_details']['branch'] = [2]
        self.params['vendor_details']['supervisor'] = [3]
        self.params['user_companies_currency']=[{"2": {"air_currency": "JPY","lcl_currency": "EUR","fcl_currency": "EUR"}}]
        self.params['companies_mode']=[ {"2": ["FCLI","FCLE"]}]


        response = self.client.post(self.vendor_add_post_api_url, data=self.params, format='json')
        self.api_response_json = json.loads(response.content)
        response = self.client.get(self.api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        response = self.client.get(api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Resend mail sent successfully', api_response_json['message'])
        self.assertEqual(200, api_response_json['code'])