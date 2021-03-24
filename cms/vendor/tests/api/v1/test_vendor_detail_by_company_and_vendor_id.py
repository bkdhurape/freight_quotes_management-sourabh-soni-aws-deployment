from company.models.company import Company
from rest_framework.test import APITestCase
from vendor.models.vendor import Vendor
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json


class TestVendorDetailByCompanyAndVendorID(APITestCase):

    fixtures = VendorRequestParams.get_seed_data_list()

    def setUp(self):
        vendor_post_api_url = VendorRequestParams.api_url() + '/api/v1/vendor/'

        # Vendor register
        vendor_register_params = VendorRequestParams.post_vendor_registration_personal_details_request_set()
        vendor_register_params['vendor_details']['status'] = 1
        response = self.client.post(vendor_post_api_url, data=vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        # Add a vendor
        params = VendorRequestParams.post_add_vendor_valid_request_set()
        params['vendor_details']['status'] = 1
        response = self.client.post(vendor_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        response = params['vendor_details']['email'] = "shivo1u3@g.com"
        response = self.client.post(vendor_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        vendor_name = vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(multi=True, name=vendor_name).values_list('id','home_company'))[0]
        self.vendor_id, self.company_id = vendor

        # Login activated vendor
        response = self.client.post(VendorRequestParams.api_url() + '/user/login/', data=VendorRequestParams.login_valid_request_params(), format='json')
        api_response_json = json.loads(response.content)


    def test_get_vendor_details_by_company_and_vendor_id(self):
        vendor_get_api_url = VendorRequestParams.api_url() + '/api/v1/company/' + str(self.company_id) + '/vendor/' + str(self.vendor_id) + '/'
        response = self.client.get(vendor_get_api_url)
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor Data retrieved successfully.', api_response_json['message'])

        data = api_response_json['data']
        vendor_keys, vendor_currency_keys = VendorRequestParams.vendor_get_request_keys()

        self.assertIn('vendor_data',data)
        for vendor_key in vendor_keys:
            self.assertIn(vendor_key,data['vendor_data'])

        self.assertIn('currency_profile_data',data)
        for vendor_currency_key in vendor_currency_keys:
            for currency_profile in data['currency_profile_data']:
                self.assertIn(vendor_currency_key,currency_profile)


    def test_get_vendor_details_by_valid_company_and_invalid_vendor_id(self):
        vendor_get_api_url = VendorRequestParams.api_url() + '/api/v1/company/' + str(self.company_id) + '/vendor/99/'
        response = self.client.get(vendor_get_api_url)
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor data not found.', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])


    def test_get_vendor_details_by_invalid_company_and_valid_vendor_id(self):
        vendor_get_api_url = VendorRequestParams.api_url() + '/api/v1/company/99/vendor/' + str(self.vendor_id) + '/'
        response = self.client.get(vendor_get_api_url)
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Company not found', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0001', api_response_json['code'])


    def test_get_vendor_details_by_invalid_company_and_invalid_vendor_id(self):
        vendor_get_api_url = VendorRequestParams.api_url() + '/api/v1/company/99/vendor/99/'
        response = self.client.get(vendor_get_api_url)
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Company not found', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0001', api_response_json['code'])
