from rest_framework.test import APITestCase
from vendor.models.vendor_type import VendorType
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json


class TestVendorTypeDeleteById(APITestCase):

    def setUp(self):
        api_url = VendorRequestParams.api_url() + '/api/v1/vendor_type/'

        # Vendor type
        params = VendorRequestParams.post_vendor_type_request_set()
        self.client.post(api_url, data=params, format='json')

        # Add a vendor type
        params = VendorRequestParams.post_vendor_type_request_set2()
        self.client.post(api_url, data=params, format='json')

        vendor_type_name = params['name']
        self.vendor_type_id = list(VendorType.find_by(multi=True, name=vendor_type_name).values_list('id', flat=True))[0]



    def test_vendor_type_delete_by_id(self):
        api_url = VendorRequestParams.api_url() + '/api/v1/vendor_type/' + str(self.vendor_type_id) + '/'
        response = self.client.delete(api_url)
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor type removed successfully', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])


    def test_vendor_type_delete_by_invalid_id(self):
        api_url = VendorRequestParams.api_url() + '/api/v1/vendor_type/99999999999/'
        response = self.client.delete(api_url)
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Vendor type data not found.', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0951', api_response_json['code'])
