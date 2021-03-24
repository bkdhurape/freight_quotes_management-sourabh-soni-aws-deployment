from company.models.company import Company
from rest_framework.test import APITestCase
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json


class TestVendorActivationLinkExpired(APITestCase):

    fixtures = VendorRequestParams.get_seed_data_list()

    def setUp(self):
        vendor_post_api_url = VendorRequestParams.api_url() + '/api/v1/vendor/'

        # Vendor register
        vendor_register_params = VendorRequestParams.post_vendor_registration_personal_details_request_set()
        response = self.client.post(vendor_post_api_url, data=vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        vendor_name = vendor_register_params['vendor_details']['name']
        self.company_id = list(Vendor.find_by(multi=True, name=vendor_name).values_list('home_company', flat=True))[0]
        self.vendor_register_params = vendor_register_params

        encoded_email = encode_data(vendor_register_params['vendor_details']['email'])
        self.test_vendor_send_activation_link_api_url = VendorRequestParams.api_url() + '/api/v1/company/'+ str(self.company_id) +'/vendor/send_activation_link/' + encoded_email


    def test_vendor_activation_link_expired(self):
        response = self.client.get(self.test_vendor_send_activation_link_api_url, format='json')
        api_response_json = json.loads(response.content)

        response = self.client.get(api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Your activation link has been expired. Please click here to resend the activation link or Contact admin for any other queries.', api_response_json['message'])
        self.assertEqual(200, api_response_json['code'])

    def test_vendor_resend_activation_link(self):
        response = self.client.get(self.test_vendor_send_activation_link_api_url, format='json')
        api_response_json = json.loads(response.content)

        response = self.client.get(api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        response = self.client.get(api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Resend mail sent successfully.', api_response_json['message'])
        self.assertEqual(200, api_response_json['code'])
