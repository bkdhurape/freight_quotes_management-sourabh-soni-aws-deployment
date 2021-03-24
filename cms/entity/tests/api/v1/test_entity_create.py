from entity.tests.api.v1.entity_request_params import EntityRequestParams
from rest_framework.test import APITestCase
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json


class TestEntityCreate(APITestCase):

    fixtures = VendorRequestParams.get_seed_data_list()

    def setUp(self):
        self.vendor_post_api_url = VendorRequestParams.api_url() + '/api/v1/vendor/'
        self.vendor_register_params = VendorRequestParams.post_vendor_registration_personal_details_request_set()
        self.params = VendorRequestParams.post_add_vendor_valid_request_set()

        response = self.client.post(self.vendor_post_api_url, data=self.vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        vendor_name = self.vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(multi=True, name=vendor_name).values_list('id','home_company'))[0]
        self.vendor_id, self.company_id = vendor

        encoded_email = encode_data(self.vendor_register_params['vendor_details']['email'])
        test_vendor_send_activation_link_api_url = VendorRequestParams.api_url() + '/api/v1/company/'+ str(self.company_id) +'/vendor/send_activation_link/' + encoded_email

        response = self.client.get(test_vendor_send_activation_link_api_url, format='json')
        self.final_api_response_json = json.loads(response.content)
        self.vendor_add_post_api_url = VendorRequestParams.api_url() + '/api/v1/company/'+ str(self.company_id) +'/vendor/'

        response = self.client.get(self.final_api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        response = self.client.post(VendorRequestParams.api_url() + '/user/login/', data=VendorRequestParams.login_valid_request_params(), format='json')
        api_response_json = json.loads(response.content)

        self.api_url = EntityRequestParams.api_url() + '/api/v1/company/'+ str(self.company_id) +'/entity/'


    def test_entity_create(self):

        # Add entity
        params = EntityRequestParams.post_entity_request_set()
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Entity added successfully.', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])

    def test_entity_create_blank_name(self):

        # Add entity
        params = EntityRequestParams.post_entity_request_set()
        params['name'] = ""
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('name - This field may not be blank.', api_response_json['message'])
        self.assertEqual({'name': ['This field may not be blank.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])


    def test_entity_create_entity_type_not_selected(self):

        # Add entity
        params = EntityRequestParams.post_entity_request_set()
        params['is_shipper'] = False
        params['is_consignee'] = False
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('You must select atleast one entity i.e. Shipper or Consignee', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F02005', api_response_json['code'])


    def test_entity_create_with_duplicate_entry(self):

        # Add entity with duplicate entry
        params = EntityRequestParams.post_entity_request_set()
        response = self.client.post(self.api_url, data=params, format='json')

        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('non_field_errors - The fields company, name must make a unique set.', api_response_json['message'])
        self.assertEqual({'non_field_errors': ['The fields company, name must make a unique set.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])
