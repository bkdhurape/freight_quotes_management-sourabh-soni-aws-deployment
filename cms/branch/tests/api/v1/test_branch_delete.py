from branch.models.branch import Branch
from branch.tests.api.v1.branch_request_params import BranchRequestParams
from django.test import TestCase, Client
from rest_framework import status
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
import json

# initialize the APIClient app
client = Client()


class TestBranchDelete(TestCase):
    '''Test modules for deletion of branch (DELETE method) '''
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
        self.vendor_id, self.company_id_setup = vendor

        encoded_email = encode_data(
            self.vendor_register_params['vendor_details']['email'])
        test_vendor_send_activation_link_api_url = BranchRequestParams.api_url(
        ) + 'api/v1/company/' + str(self.company_id_setup) + '/vendor/send_activation_link/' + encoded_email

        response = client.get(
            test_vendor_send_activation_link_api_url, content_type='application/json')
        self.final_api_response_json = json.loads(response.content)
        self.vendor_add_post_api_url = BranchRequestParams.api_url(
        ) + '/api/v1/company/' + str(self.company_id_setup) + '/vendor/'

        response = client.get(
            self.final_api_response_json['data'], content_type='application/json')
        api_response_json = json.loads(response.content)



        response = client.post(BranchRequestParams.api_url() + 'user/login/', data=json.dumps(
            BranchRequestParams.login_valid_request_params()), content_type='application/json')
        api_response_json = json.loads(response.content)

        api_url = BranchRequestParams.api_url() + 'api/v1/company/' + \
            str(self.company_id_setup)+'/branch/'
        params = BranchRequestParams.post_branch_with_transport_mode_set(self)

        response = client.post(
            api_url,
            data=json.dumps(params),
            content_type='application/json'
        )

        branch_name = params['name']

        self.branch_id = list(Branch.find_by(
            multi=True, name=branch_name).values_list('id', flat=True))[0]

    # Delete branch successfully
    def test_branch_delete(self):

        api_url_delete = BranchRequestParams.api_url() + 'api/v1/company/' + \
            str(self.company_id_setup)+'/branch/' + \
            str(self.branch_id)+'/'
        response = client.delete(api_url_delete)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Branch removed successfully',
                         api_response['message'])
        self.assertEqual(None, api_response['data'])

    # Branch delete but company not found
    def test_branch_delete_company_not_found(self):

        api_company_not_found_url = BranchRequestParams.api_url(
        ) + 'api/v1/company/99999999999/branch/'+str(self.branch_id)+'/'

        response = client.delete(api_company_not_found_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Company not found', api_response['message'])
        self.assertEqual({}, api_response['data'])
        self.assertEqual('F0001', api_response['code'])

    # Branch delete but branch id does not exist
    def test_branch_data_not_found(self):

        api_data_not_found_url = BranchRequestParams.api_url(
        ) + 'api/v1/company/'+str(self.company_id_setup)+'/branch/9999999999/'

        response = client.delete(api_data_not_found_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Branch not found', api_response['message'])
        self.assertEqual({}, api_response['data'])
        self.assertEqual('F0851', api_response['code'])

    # Deleting branch if branch has been already deleted it will give error as Branch not found
    def test_branch_delete_again_data_not_found(self):

        api_url_delete = BranchRequestParams.api_url() + 'api/v1/company/' + \
            str(self.company_id_setup)+'/branch/' + \
            str(self.branch_id)+'/'
        response = client.delete(api_url_delete)

        response = client.delete(api_url_delete)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F0851',  api_response['code'])
        self.assertEqual('failure',  api_response['status'])
        self.assertEqual('Branch not found',  api_response['message'])
        self.assertEqual({},  api_response['data'])

    def test_delete_vendor_hq_branch(self):

        # Getting id of HQ branch
        branch_id = list(Branch.find_by(multi=True, name='HQ', company=self.company_id_setup,
                                        status=Vendor.ACTIVE).values_list('id', flat=True))[0]

        api_url_hq_delete = BranchRequestParams.api_url() + 'api/v1/company/' + \
            str(self.company_id_setup)+'/branch/'+str(branch_id)+'/'

        response = client.delete(api_url_hq_delete)
        api_response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('You can not delete Head Branch',
                         api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0859', api_response_json['code'])
