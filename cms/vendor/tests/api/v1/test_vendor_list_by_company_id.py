from company.models.company import Company
from rest_framework.test import APITestCase
from vendor.models.vendor import Vendor
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json


class TestVendorListByCompanyID(APITestCase):

    fixtures = VendorRequestParams.get_seed_data_list()

    def setUp(self):
        vendor_post_api_url = VendorRequestParams.api_url() + '/api/v1/vendor/'

        # Vendor register
        vendor_register_params = VendorRequestParams.post_vendor_registration_personal_details_request_set()
        vendor_register_params['vendor_details']['status'] = 1
        response = self.client.post(vendor_post_api_url, data=vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        company_name = vendor_register_params['vendor_details']['company_name']
        company_id = list(Company.find_by(multi=True, name=company_name).values_list('id', flat=True))[0]
        self.company_id = company_id

        # Login activated vendor
        response = self.client.post(VendorRequestParams.api_url() + '/user/login/', data=VendorRequestParams.login_valid_request_params(), format='json')
        api_response_json = json.loads(response.content)


    def test_get_vendor_list_by_company_id(self):
        vendor_get_api_url = VendorRequestParams.api_url() + '/api/v1/company/' + str(self.company_id) + '/vendor/'
        response = self.client.get(vendor_get_api_url)
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor Data retrieved successfully.', api_response_json['message'])

        data = api_response_json['data']
        vendor_keys, vendor_currency_keys = VendorRequestParams.vendor_get_request_keys()


        for vendor in data:
            self.assertIn('vendor_data',vendor)
            for vendor_key in vendor_keys:
                self.assertIn(vendor_key,vendor['vendor_data'])

            self.assertIn('currency_profile_data',vendor)
            for vendor_currency_key in vendor_currency_keys:
                for currency_profile in vendor['currency_profile_data']:
                    self.assertIn(vendor_currency_key,currency_profile)


    def test_get_vendor_list_by_invalid_company_id(self):
        vendor_get_api_url = VendorRequestParams.api_url() + '/api/v1/company/999999999/vendor/'
        response = self.client.get(vendor_get_api_url)
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Company not found', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0001', api_response_json['code'])


    def test_get_vendor_list_by_company_id_with_pagination(self):
        vendor_get_api_url = VendorRequestParams.api_url() + '/api/v1/company/' + str(self.company_id) + '/vendor/?page=1'
        response = self.client.get(vendor_get_api_url)
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor Data retrieved successfully.', api_response_json['message'])

        data = api_response_json['data']
        vendor_keys, vendor_currency_keys = VendorRequestParams.vendor_get_request_keys()

        for vendor in data:
            self.assertIn('vendor_data',vendor)
            for vendor_key in vendor_keys:
                self.assertIn(vendor_key,vendor['vendor_data'])

            self.assertIn('currency_profile_data',vendor)
            for vendor_currency_key in vendor_currency_keys:
                for currency_profile in vendor['currency_profile_data']:
                    self.assertIn(vendor_currency_key,currency_profile)


    def test_get_vendor_list_by_company_id_with_page_and_limit(self):
        vendor_get_api_url = VendorRequestParams.api_url() + '/api/v1/company/' + str(self.company_id) + '/vendor/?page=1&limit=3'
        response = self.client.get(vendor_get_api_url)
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor Data retrieved successfully.', api_response_json['message'])

        data = api_response_json['data']
        vendor_keys, vendor_currency_keys = VendorRequestParams.vendor_get_request_keys()

        for vendor in data:
            self.assertIn('vendor_data',vendor)
            for vendor_key in vendor_keys:
                self.assertIn(vendor_key,vendor['vendor_data'])

            self.assertIn('currency_profile_data',vendor)
            for vendor_currency_key in vendor_currency_keys:
                for currency_profile in vendor['currency_profile_data']:
                    self.assertIn(vendor_currency_key,currency_profile)


    def test_get_vendor_list_by_company_id_with_page_limit_and_no_record(self):
        vendor_get_api_url = VendorRequestParams.api_url() + '/api/v1/company/' + str(self.company_id) + '/vendor/?page=4&limit=4'
        response = self.client.get(vendor_get_api_url)
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('No more records', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])
