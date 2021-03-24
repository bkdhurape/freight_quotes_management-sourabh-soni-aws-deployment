from rest_framework.test import APITestCase
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json


class TestVendorRegistration(APITestCase):

    fixtures = VendorRequestParams.get_seed_data_list()

    def setUp(self):
        self.vendor_post_api_url = VendorRequestParams.api_url() + '/api/v1/vendor/'
        self.vendor_register_params = VendorRequestParams.post_vendor_registration_personal_details_request_set()

    def test_register_vendor_with_valid_details(self):

        response = self.client.post(self.vendor_post_api_url, data=self.vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor added successfully.', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])

    def test_register_vendor_with_duplicate_entry(self):

        response = self.client.post(self.vendor_post_api_url, data=self.vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        response = self.client.post(self.vendor_post_api_url, data=self.vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Company already exists. Please contact your admin to register.', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0905', api_response_json['code'])


    def test_register_vendor_with_invalid_contact(self):
        params = VendorRequestParams.post_register_vendor_invalid_contact_detail_set(self.vendor_register_params)
        response = self.client.post(self.vendor_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Invalid contact no.', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('BF0003', api_response_json['code'])
