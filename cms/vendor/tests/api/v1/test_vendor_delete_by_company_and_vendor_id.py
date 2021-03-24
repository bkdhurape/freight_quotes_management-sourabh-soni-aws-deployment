from company.models.company import Company
from rest_framework.test import APITestCase
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
from vendor.models.vendor import Vendor
import json


class TestVendorDeleteByCompanyAndVendorId(APITestCase):

    fixtures = VendorRequestParams.get_seed_data_list()

    def setUp(self):
        vendor_post_api_url = VendorRequestParams.api_url() + '/api/v1/vendor/'

        # Vendor register
        vendor_register_params = VendorRequestParams.post_vendor_registration_personal_details_request_set()
        vendor_register_params['vendor_details']['status'] = 1
        response = self.client.post(vendor_post_api_url, data=vendor_register_params, format='json')

        # Add a vendor
        add_vendor_params = VendorRequestParams.post_add_vendor_valid_request_set()
        add_vendor_params['vendor_details']['status'] = 1
        response = self.client.post(vendor_post_api_url, data=add_vendor_params, format='json')

        vendor_name = vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(multi=True, name=vendor_name).values_list('id','home_company'))[0]
        self.vendor_id, self.company_id = vendor

        # Login activated vendor
        response = self.client.post(VendorRequestParams.api_url() + '/user/login/', data=VendorRequestParams.login_valid_request_params(), format='json')
        api_response_json = json.loads(response.content)

    def test_delete_vendor_by_id(self):
        vender_delete_api_url = VendorRequestParams.api_url() + '/api/v1/company/' + str(self.company_id) + '/vendor/' + str(self.vendor_id) + '/'
        response = self.client.delete(vender_delete_api_url)
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor removed successfully', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])


    def test_delete_vendor_by_invalid_id(self):
        vender_delete_api_url = VendorRequestParams.api_url() + '/api/v1/company/' + str(self.company_id) + '/vendor/99/'
        response = self.client.delete(vender_delete_api_url)
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Vendor data not found.', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0901', api_response_json['code'])
