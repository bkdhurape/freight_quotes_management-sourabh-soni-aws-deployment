from port.models.port import Port
from port.tests.api.v1.port_request_params import PortRequestParams
from rest_framework.test import APITestCase
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json


class TestPortUpdate(APITestCase):

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


        api_url = PortRequestParams.api_url() + '/api/v1/port/'

        # Vendor type
        params = PortRequestParams.post_port_request_set()
        self.client.post(api_url, data=params, format='json')

        port_name = params['name']
        self.port_id = list(Port.find_by(multi=True, name=port_name).values_list('id', flat=True))[0]


    def test_entiy_update(self):
        api_url = PortRequestParams.api_url() + '/api/v1/port/' + str(self.port_id) + '/'
        params = PortRequestParams.post_port_request_set2()
        response = self.client.put(api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Port updated successfully.', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])

    def test_entiy_update_by_invalid_id(self):
        api_url = PortRequestParams.api_url() + '/api/v1/port/99999999999/'
        params = PortRequestParams.post_port_request_set2()
        response = self.client.put(api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Port data not found.', api_response_json['message'])
        self.maxDiff = None
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F02005', api_response_json['code'])
