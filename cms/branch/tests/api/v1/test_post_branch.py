from branch.models.branch import Branch
from branch.tests.api.v1.branch_request_params import BranchRequestParams
from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APIClient
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
import json


# initialize the APIClient app
client = APIClient()


class TestPostBranch(TestCase):
    '''Test modules for deletion of branch (Update method) '''

    fixtures = BranchRequestParams.get_seed_data_list()

    def api_authentication(self):
        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)

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
        ) + 'api/v1/company/' + str(self.company_id) + '/vendor/'

        response = client.get(
            self.final_api_response_json['data'], content_type='application/json')
        api_response_json = json.loads(response.content)

        response = client.post(BranchRequestParams.api_url() + 'user/login/', data=json.dumps(
            BranchRequestParams.login_valid_request_params()), content_type='application/json')
        api_response_json = json.loads(response.content)

        self.jwt_token = api_response_json['data'][0]['token']
        self.api_authentication()

        self.api_url = BranchRequestParams.api_url() + 'api/v1/company/' + \
            str(self.company_id)+'/branch/'

    def test_branch_post(self):

        params = BranchRequestParams.post_branch_with_transport_mode_set(self)

        response = client.post(self.api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Branch created successfully',
                         api_response['message'])
        self.assertEqual(None, api_response['data'])

    def test_branch_post_company_not_found(self):

        api_company_not_found_url = BranchRequestParams.api_url(
        ) + 'api/v1/company/99999999999/branch/'

        params = BranchRequestParams.post_branch_with_transport_mode_set(self)

        response = client.post(api_company_not_found_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Access denied.',
                         api_response['message'])
        self.assertEqual(None, api_response['data'])

    def test_branch_post_name_already_exist(self):

        params = BranchRequestParams.post_branch_with_transport_mode_set_secondset(self)

        response = client.post(
            self.api_url,
            data=json.dumps(params),
            content_type='application/json'
        )

        params = BranchRequestParams.post_branch_already_exists(self)

        response = client.post(self.api_url, data=json.dumps(
            params), content_type='application/json')
            

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('non_field_errors - The fields company, name must make a unique set.',
                         api_response['message'])
        self.assertEqual(['The fields company, name must make a unique set.'],
                         api_response['data']['non_field_errors'])
        self.assertEqual('BEF0001', api_response['code'])

    def test_branch_minimum_weight_required(self):

        params = BranchRequestParams.post_branch_minimum_weight_required(self)

        response = client.post(self.api_url, data=json.dumps(
            params), content_type='application/json')
            

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Minimum weight is required',
                         api_response['message'])
        self.assertEqual({},api_response['data'])
        self.assertEqual('F0860', api_response['code'])

    def test_branch_maximum_weight_required(self):

        params = BranchRequestParams.post_branch_maximum_weight_required(self)

        response = client.post(self.api_url, data=json.dumps(
            params), content_type='application/json')
            
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Maximum weight is required',
                         api_response['message'])
        self.assertEqual({},api_response['data'])
        self.assertEqual('F0861', api_response['code'])

    def test_branch_weight_unit_validation(self):

        params = BranchRequestParams.post_branch_weight_unit_required(self)

        response = client.post(self.api_url, data=json.dumps(
            params), content_type='application/json')
            
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Weight unit is required',
                         api_response['message'])
        self.assertEqual({},api_response['data'])
        self.assertEqual('F0862', api_response['code'])

    def test_branch_maximum_weight_should_be_more_than_minimum_weight(self):

        params = BranchRequestParams.post_branch_maximum_weight_should_be_more_than_minimum_weight(self)

        response = client.post(self.api_url, data=json.dumps(
            params), content_type='application/json')
            
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Maximum weight should be more than minimum weight',
                         api_response['message'])
        self.assertEqual({},api_response['data'])
        self.assertEqual('F0863', api_response['code'])

    def test_branch_minimum_radius_required(self):

        params = BranchRequestParams.post_branch_minimum_radius_required(self)

        response = client.post(self.api_url, data=json.dumps(
            params), content_type='application/json')
            
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Minimum radius is required',
                         api_response['message'])
        self.assertEqual({},api_response['data'])
        self.assertEqual('F0864', api_response['code'])

    def test_branch_maximum_radius_required(self):

        params = BranchRequestParams.post_branch_maximum_radius_required(self)

        response = client.post(self.api_url, data=json.dumps(
            params), content_type='application/json')
            
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Maximum radius is required',
                         api_response['message'])
        self.assertEqual({},api_response['data'])
        self.assertEqual('F0865', api_response['code'])

    def test_branch_radius_unit_required(self):

        params = BranchRequestParams.post_branch_radius_unit_required(self)

        response = client.post(self.api_url, data=json.dumps(
            params), content_type='application/json')
            
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Radius unit is required',
                         api_response['message'])
        self.assertEqual({},api_response['data'])
        self.assertEqual('F0866', api_response['code'])


    def test_branch_maximum_radius_should_be_greater(self):

        params = BranchRequestParams.post_branch_maximum_radius_should_be_more_than_minimum_radius(self)

        response = client.post(self.api_url, data=json.dumps(
            params), content_type='application/json')
            
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Maximum radius should be more than minimum radius',
                         api_response['message'])
        self.assertEqual({},api_response['data'])
        self.assertEqual('F0867', api_response['code'])


    def test_branch_radius_should_be_positive(self):

        params = BranchRequestParams.post_branch_radius_should_be_positive_value(self)

        response = client.post(self.api_url, data=json.dumps(
            params), content_type='application/json')
            
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('minimum_radius - Ensure this value is greater than or equal to 0.',
                         api_response['message'])
        self.assertEqual(["Ensure this value is greater than or equal to 0."],api_response['data']['minimum_radius'])
        self.assertEqual('BEF0001', api_response['code'])