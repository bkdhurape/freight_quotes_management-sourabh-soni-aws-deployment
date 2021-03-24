from rest_framework.test import APITestCase
from vendor.models.vendor_type import VendorType
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json


class TestVendorTypeUpdate(APITestCase):

    def setUp(self):
        api_url = VendorRequestParams.api_url() + '/api/v1/vendor_type/'

        # Create vendor type
        params = VendorRequestParams.post_vendor_type_request_set()
        self.client.post(api_url, data=params, format='json')

        vendor_type_name = params['name']
        self.vendor_type_id = list(VendorType.find_by(multi=True, name=vendor_type_name).values_list('id', flat=True))[0]


    def test_vendor_type_update(self):

        api_url = VendorRequestParams.api_url() + '/api/v1/vendor_type/' + str(self.vendor_type_id) + '/'
        params = VendorRequestParams.post_vendor_type_request_set2()
        response = self.client.put(api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor type updated successfully.', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])

    def test_vendor_type_update_by_invalid_id(self):

        api_url = VendorRequestParams.api_url() + '/api/v1/vendor_type/999999999/'
        params = VendorRequestParams.post_vendor_type_request_set2()
        response = self.client.put(api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Vendor type data not found.', api_response_json['message'])
        self.maxDiff = None
        self.assertEqual({}, api_response_json['data'])
