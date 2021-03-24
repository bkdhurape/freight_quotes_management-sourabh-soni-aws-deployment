from branch.models.branch import Branch
from branch.tests.api.v1.branch_request_params import BranchRequestParams
from django.test import TestCase, Client
from rest_framework import status
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
import json


# initialize the APIClient app
client = Client()


class TestBranchTransportModeGetAll(TestCase):
    '''Test modules for deletion of branch (GET method) '''
    fixtures = BranchRequestParams.get_seed_data_list()

    def setUp(self):
        
        self.vendor_post_api_url = BranchRequestParams.api_url() + 'api/v1/vendor/'
        self.vendor_register_params = BranchRequestParams.post_vendor_registration_personal_details_request_set()

        response = client.post(self.vendor_post_api_url, data=json.dumps(
            self.vendor_register_params), content_type='application/json')
        api_response_json = json.loads(response.content)

        vendor_name = self.vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(
            multi=True, name=vendor_name).values_list('id', 'home_company'))[0]
        self.vendor_id, self.company_id = vendor

        encoded_email = encode_data(
            self.vendor_register_params['vendor_details']['email'])
        test_vendor_send_activation_link_api_url = BranchRequestParams.api_url(
        ) + 'api/v1/company/' + str(self.company_id) + '/vendor/send_activation_link/' + encoded_email

        response = client.get(
            test_vendor_send_activation_link_api_url, content_type='application/json')
        self.final_api_response_json = json.loads(response.content)
        self.vendor_add_post_api_url = BranchRequestParams.api_url(
        ) + '/api/v1/company/' + str(self.company_id) + '/vendor/'

        response = client.get(
            self.final_api_response_json['data'], content_type='application/json')
        api_response_json = json.loads(response.content)

        response = client.post(BranchRequestParams.api_url() + 'user/login/', data=json.dumps(
            BranchRequestParams.login_valid_request_params()), content_type='application/json')
        api_response_json = json.loads(response.content)

        self.api_url = BranchRequestParams.api_url() + 'api/v1/company/' + \
            str(self.company_id)+'/branch/'

        params = BranchRequestParams.post_branch_with_transport_mode_set(self)

        response = client.post(
            self.api_url,
            data=json.dumps(params),
            content_type='application/json'
        )

        branch_name = params['name']

        self.branch_id = list(Branch.find_by(
            multi=True, name=branch_name).values_list('id', flat=True))[0]

        self.api_url_transport_mode_create = BranchRequestParams.api_url(
        )+'api/v1/branch/'+str(self.branch_id)+'/branch_transport_mode/'

        params = BranchRequestParams.post_transport_mode_set(self)

        response = client.post(
            self.api_url_transport_mode_create,
            data=json.dumps(params),
            content_type='application/json'
        )

        params = BranchRequestParams.post_transport_mode_set_second_all(self)

        response = client.post(
            self.api_url_transport_mode_create,
            data=json.dumps(params),
            content_type='application/json'
        )

    def test_transport_mode_get_all(self):

        response = client.get(self.api_url_transport_mode_create)
        api_response = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual(
            'Branch transport mode details retrieved successfully.', api_response['message'])

        data = api_response['data']
        transport_mode_keys = BranchRequestParams.transport_details_key(self)

        for transport_mode in data:
            for transport_mode_key in transport_mode_keys:
                self.assertIn(transport_mode_key, transport_mode)

    def test_transport_mode_get_all_pagination(self):

        api_url = BranchRequestParams.api_url()+'api/v1/branch/'+str(self.branch_id) + \
            '/branch_transport_mode/?page=1&limit=2'

        response = client.get(api_url)
        api_response = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual(
            'Branch transport mode details retrieved successfully.', api_response['message'])

        data = api_response['data']
        transport_mode_keys = BranchRequestParams.transport_details_key(self)

        for transport_mode in data:
            for transport_mode_key in transport_mode_keys:
                self.assertIn(transport_mode_key, transport_mode)

    def test_transport_mode_get_all_pagination_no_more_data(self):

        api_url = BranchRequestParams.api_url()+'api/v1/branch/'+str(self.branch_id) + \
            '/branch_transport_mode/?page=100&limit=2'

        response = client.get(api_url)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual(
            'No more records', api_response['message'])
        self.assertEqual(None, api_response['data'])
    

    def test_transport_mode_branch_not_found(self):

        api_url = BranchRequestParams.api_url()+'api/v1/branch/99999/branch_transport_mode/'

        response = client.get(api_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Branch not found', api_response['message'])
        self.assertEqual({}, api_response['data'])
        self.assertEqual('F0851', api_response['code'])
