from port.tests.api.v1.port_request_params import PortRequestParams
from rest_framework.test import APITestCase
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json


class TestPortCreate(APITestCase):

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

        self.api_url = PortRequestParams.api_url() + '/api/v1/port/'


    def test_port_create(self):

        # Add port
        params = PortRequestParams.post_port_request_set()
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Port added successfully.', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])

    def test_port_create_blank_name(self):

        # Add port
        params = PortRequestParams.post_port_request_set()
        params['name'] = ""
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('name - This field may not be blank.', api_response_json['message'])
        self.assertEqual({'name': ['This field may not be blank.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])


    def test_port_create_port_invalid_latitude(self):

        # Add port
        params = PortRequestParams.post_port_request_set()
        params['lat'] = ""
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('lat - A valid number is required.', api_response_json['message'])
        self.assertEqual({'lat': ['A valid number is required.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])


    def test_port_create_port_invalid_longitude(self):

        # Add port
        params = PortRequestParams.post_port_request_set()
        params['lng'] = ""
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('lng - A valid number is required.', api_response_json['message'])
        self.assertEqual({'lng': ['A valid number is required.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])


    def test_port_create_port_invalid_port_type(self):

        # Add port
        params = PortRequestParams.post_port_request_set()
        params['type'] = "seaport12"
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('type - \"seaport12\" is not a valid choice.', api_response_json['message'])
        self.assertEqual({'type': ['\"seaport12\" is not a valid choice.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])


    def test_port_create_port_blank_seaport_code(self):
        # Add port
        params = PortRequestParams.post_port_request_set()
        params['type'] = "seaport"
        params['code'] = ""
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Port Code required.', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F02009', api_response_json['code'])


    def test_port_create_port_blank_airport_iata(self):
        # Add port
        params = PortRequestParams.post_port_request_set()
        params['type'] = "airport"
        params['iata'] = ""
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Port IATA required.', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F02010', api_response_json['code'])


    def test_port_create_with_duplicate_entry(self):

        # Add port with duplicate entry
        params = PortRequestParams.post_port_request_set()
        response = self.client.post(self.api_url, data=params, format='json')

        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('name - port with this name already exists.', api_response_json['message'])
        self.assertEqual({'name': ['port with this name already exists.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])
