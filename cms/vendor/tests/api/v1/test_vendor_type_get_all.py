from rest_framework.test import APITestCase
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json


class TestVendorTypeGetAll(APITestCase):

    def setUp(self):
        api_url = VendorRequestParams.api_url() + '/api/v1/vendor_type/'

        # Vendor type register
        params = VendorRequestParams.post_vendor_type_request_set()
        self.client.post(api_url, data=params, format='json')

        # Add a vendor type
        params = VendorRequestParams.post_vendor_type_request_set2()
        self.client.post(api_url, data=params, format='json')

        self.api_url = api_url


    def test_vendor_type_get_all(self):

        response = self.client.get(self.api_url, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor type data retrieved successfully.', api_response_json['message'])
        self.maxDiff = None
        self.assertEqual(VendorRequestParams.get_list_of_vendor_type_params_set(), api_response_json['data'])
