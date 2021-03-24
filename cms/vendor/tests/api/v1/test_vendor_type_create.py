from rest_framework.test import APITestCase
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json


class TestVendorTypeCreate(APITestCase):

    def setUp(self):
        self.api_url = VendorRequestParams.api_url() + '/api/v1/vendor_type/'

    def test_vendor_type_create(self):

        # Add vendor type
        params = VendorRequestParams.post_vendor_type_request_set()
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor type added successfully.', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])


    def test_vendor_type_create_with_duplicate_entry(self):

        # Add vendor type with duplicate entry
        params = VendorRequestParams.post_vendor_type_request_set()
        response = self.client.post(self.api_url, data=params, format='json')

        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('name - vendor type with this name already exists.', api_response_json['message'])
        self.assertEqual({'name': ['vendor type with this name already exists.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])
