from company.tests.api.v1.company_request_parameters import CompanyRequestParams
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json

client = APIClient()

class TestAddCompany(APITestCase):

    fixtures = VendorRequestParams.get_seed_data_list()
    def api_authentication(self):
        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)

    def setUp(self):
        self.vendor_post_api_url = VendorRequestParams.api_url() + '/api/v1/vendor/'
        self.vendor_register_params = VendorRequestParams.post_vendor_registration_personal_details_request_set()
        self.params = VendorRequestParams.post_add_vendor_valid_request_set()

        response = self.client.post(
            self.vendor_post_api_url, data=self.vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        vendor_name = self.vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(
            multi=True, name=vendor_name).values_list('id', 'home_company'))[0]
        self.vendor_id, self.company_id = vendor

        encoded_email = encode_data(
            self.vendor_register_params['vendor_details']['email'])
        test_vendor_send_activation_link_api_url = VendorRequestParams.api_url(
        ) + '/api/v1/company/' + str(self.company_id) + '/vendor/send_activation_link/' + encoded_email

        response = self.client.get(
            test_vendor_send_activation_link_api_url, format='json')
        self.final_api_response_json = json.loads(response.content)
        self.vendor_add_post_api_url = VendorRequestParams.api_url(
        ) + '/api/v1/company/' + str(self.company_id) + '/vendor/'

        response = self.client.get(
            self.final_api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        response = self.client.post(VendorRequestParams.api_url(
        ) + '/user/login/', data=VendorRequestParams.login_valid_request_params(), format='json')
        api_response_json = json.loads(response.content)
        self.jwt_token = api_response_json['data'][0]['token']
        self.api_authentication()
        self.add_company_post_api_url = VendorRequestParams.api_url() + '/api/v1/company/'
    
    
    def test_company_get_by_id(self):

        api_url_get_by_id =VendorRequestParams.api_url() + '/api/v1/company/' + \
            str(self.company_id)+'/'

        response = client.get(api_url_get_by_id)
        api_response = json.loads(response.content)


        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Company Data retrived successfully', api_response['message'])

        data = api_response['data']
        self.maxDiff = None

        company_get_keys = CompanyRequestParams.company_get_id(self)
        self.assertEqual(company_get_keys,data)

    def test_company_id_not_found(self):

        api_data_not_found_url = VendorRequestParams.api_url()+ '/api/v1/company/'+'9/'

        response = client.get(api_data_not_found_url)
        api_response = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Access denied.', api_response['message'])
        self.assertEqual(None, api_response['data'])
        self.assertEqual(200, api_response['code'])

        
      