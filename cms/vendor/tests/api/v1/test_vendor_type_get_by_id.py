from rest_framework.test import APITestCase
from vendor.models.vendor_type import VendorType
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json


class TestVendorTypeGetById(APITestCase):

    def setUp(self):
        api_url = VendorRequestParams.api_url() + '/api/v1/vendor_type/'

        # Add Vendor type
        params = VendorRequestParams.post_vendor_type_request_set()
        self.client.post(api_url, data=params, format='json')

        # Add a vendor type
        params = VendorRequestParams.post_vendor_type_request_set2()
        self.client.post(api_url, data=params, format='json')

        name = params['name']
        self.vendor_type_id = list(VendorType.find_by(multi=True, name=name).values_list('id', flat=True))[0]


    def test_vendor_type_get_by_id(self):

        api_url = VendorRequestParams.api_url() + '/api/v1/vendor_type/' + str(self.vendor_type_id) + '/'
        response = self.client.get(api_url, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor type data retrieved successfully.', api_response_json['message'])
        self.maxDiff = None
        self.assertEqual(VendorRequestParams.get_vendor_type_by_id_params_set(), api_response_json['data'])


    def test_vendor_type_get_by_invalid_id(self):

        api_url = VendorRequestParams.api_url() + '/api/v1/vendor_type/999999999/'
        response = self.client.get(api_url, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Vendor type data not found.', api_response_json['message'])
        self.maxDiff = None
        self.assertEqual({}, api_response_json['data'])
