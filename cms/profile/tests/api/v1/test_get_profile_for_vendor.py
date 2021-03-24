from profile.tests.api.v1.request_response_params import ProfileRequestParams
from rest_framework.test import APITestCase,APIClient
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
import json

client = APIClient()

class GetProfileVendor(APITestCase):

    fixtures = ProfileRequestParams.get_seed_data_list()

    def api_authentication(self):
        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)

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

        self.jwt_token = api_response_json['data'][0]['token']
        self.api_authentication()

        # add  new vendor
        response = client.post(self.vendor_add_post_api_url, data=self.params, format='json')
        self.api_response_json = json.loads(response.content)

    def test_get_profile_data(self):

        response = self.client.get(self.api_response_json['data'], format='json')
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