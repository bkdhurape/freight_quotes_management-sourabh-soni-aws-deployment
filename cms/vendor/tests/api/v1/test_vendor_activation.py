from company.models.company import Company
from rest_framework.test import APITestCase
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
from branch.models.branch import Branch
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json


class TestVendorActivation(APITestCase):

    fixtures = VendorRequestParams.get_seed_data_list()

    def setUp(self):
        vendor_post_api_url = VendorRequestParams.api_url() + '/api/v1/vendor/'

        # Vendor register
        vendor_register_params = VendorRequestParams.post_vendor_registration_personal_details_request_set()
        response = self.client.post(vendor_post_api_url, data=vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        vendor_name = vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(multi=True, name=vendor_name).values_list('id','home_company'))[0]
        self.vendor_id, self.company_id = vendor
        self.vendor_register_params = vendor_register_params

        encoded_email = encode_data(vendor_register_params['vendor_details']['email'])
        self.test_vendor_send_activation_link_api_url = VendorRequestParams.api_url() + '/api/v1/company/'+ str(self.company_id) +'/vendor/send_activation_link/' + encoded_email



    def test_vendor_send_activation_link(self):
        response = self.client.get(self.test_vendor_send_activation_link_api_url, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Activation link sent successfully.', api_response_json['message'])
        self.assertEqual(200, api_response_json['code'])


    def test_vendor_activation(self):
        response = self.client.get(self.test_vendor_send_activation_link_api_url, format='json')
        api_response_json = json.loads(response.content)

        response = self.client.get(api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor activated successfully.', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])
        self.assertEqual(200, api_response_json['code'])


    def test_vendor_already_activated(self):
        response = self.client.get(self.test_vendor_send_activation_link_api_url, format='json')
        initial_api_response_json = json.loads(response.content)

        response = self.client.get(initial_api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        response = self.client.get(initial_api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('You are already acivated. Please login to continue', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0906', api_response_json['code'])


    def test_vendor_activation_invalid_token(self):
        response = self.client.get(self.test_vendor_send_activation_link_api_url, format='json')
        api_response_json = json.loads(response.content)

        invalid_token_vendor_activation_api_url = VendorRequestParams.api_url() + '/api/v1/company/'+ str(self.company_id) +'/vendor/activate/aaa'
        response = self.client.get(invalid_token_vendor_activation_api_url, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Invalid Token. Please contact admin for your account activation and other queries.', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0907', api_response_json['code'])


    def test_inactive_vender_activation(self):
        vendor_post_api_url = VendorRequestParams.api_url() + '/api/v1/vendor/'

        # Vendor register
        vendor_register_params = VendorRequestParams.post_vendor_registration_personal_details_request_set()
        vendor_register_params['vendor_details']['name'] = 'shiv2'
        vendor_register_params['vendor_details']['email'] = 'shivo2u2@g.com'
        vendor_register_params['vendor_details']['company_name'] = 'fct_o1cB'
        vendor_register_params['vendor_details']['status'] = 0

        response = self.client.post(vendor_post_api_url, data=vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        vendor_name = vendor_register_params['vendor_details']['name']
        company_id = list(Vendor.find_by(multi=True, name=vendor_name).values_list('home_company', flat=True))[0]

        encoded_email = encode_data(vendor_register_params['vendor_details']['email'])
        test_vendor_send_activation_link_api_url = VendorRequestParams.api_url() + '/api/v1/company/'+ str(company_id) +'/vendor/send_activation_link/' + encoded_email

        response = self.client.get(test_vendor_send_activation_link_api_url, format='json')
        api_response_json = json.loads(response.content)

        response = self.client.get(api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Please contact admin for your account activation and other queries.', api_response_json['message'])
        self.assertEqual('F0909', api_response_json['code'])


    def test_vendor_default_branch(self):
        response = self.client.get(self.test_vendor_send_activation_link_api_url, format='json')
        api_response_json = json.loads(response.content)

        response = self.client.get(api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        branch = list(Branch.find_by(multi=True, name='HQ', company=self.company_id,status=Vendor.ACTIVE).values_list('id'))

        self.assertEqual(1, len(branch))
        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor activated successfully.', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])
        self.assertEqual(200, api_response_json['code'])
