from profile.tests.api.v1.request_response_params import ProfileRequestParams
from rest_framework.test import APITestCase,APIClient
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
import json

client = APIClient()


class SetProfileVendor(APITestCase):

    fixtures = ProfileRequestParams.get_seed_data_list()

    def api_authentication(self):
        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)

    def setUp(self):
        self.vendor_post_api_url = ProfileRequestParams.api_url() + '/api/v1/vendor/'
        self.vendor_register_params = ProfileRequestParams.post_vendor_registration_personal_details_request_set()
        self.params = ProfileRequestParams.post_add_vendor_valid_request_set()

        # vendor registration
        response = self.client.post(
            self.vendor_post_api_url, data=self.vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        vendor_name = self.vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(
            multi=True, name=vendor_name).values_list('id', 'home_company','branch'))[0]
        self.vendor_id, self.company_id,self.branch = vendor

        # vendor activation
        encoded_email = encode_data(
            self.vendor_register_params['vendor_details']['email'])
        test_vendor_send_activation_link_api_url = ProfileRequestParams.api_url(
        ) + '/api/v1/company/' + str(self.company_id) + '/vendor/send_activation_link/' + encoded_email

        response = self.client.get(
            test_vendor_send_activation_link_api_url, format='json')
        self.final_api_response_json = json.loads(response.content)

        self.vendor_add_post_api_url = ProfileRequestParams.api_url(
        ) + '/api/v1/company/' + str(self.company_id) + '/vendor/'

        response = self.client.get(
            self.final_api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        # login vendor
        self.vendor_login_api_url = ProfileRequestParams.api_url() + '/user/login/'
        response = self.client.post(
            self.vendor_login_api_url, data=ProfileRequestParams.login_valid_request_params(), format='json')
        api_response_json = json.loads(response.content)

        self.jwt_token = api_response_json['data'][0]['token']
        self.api_authentication()

    def test_set_profile(self):
        self.params['vendor_details']['company'] = [4]
        self.params['vendor_details']['branch'] = [4]
        self.params['vendor_details']['supervisor'] = [7]
        self.params['vendor_details']['home_company'] = 4
        self.params['user_companies_currency'] = [
            {"4": {"air_currency": "JPY", "lcl_currency": "EUR", "fcl_currency": "EUR"}}]
        self.params['companies_mode'] = [{"4": ["FCLI", "FCLE"]}]

        response = client.post(
            self.vendor_add_post_api_url, data=self.params, format='json')
        self.api_response_json = json.loads(response.content)

        response = self.client.put(
            self.api_response_json['data'], data=ProfileRequestParams.set_profile(), format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual(
            'your profile has been updated successfully, please login to continue', api_response_json['message'])
        self.assertEqual(200, api_response_json['code'])

    def test_get_profile(self):
        response = client.post(
            self.vendor_add_post_api_url, data=self.params, format='json')
        self.api_response_json = json.loads(response.content)

        response = self.client.put(
            self.api_response_json['data'], data=ProfileRequestParams.set_profile(), format='json')
        response = self.client.get(
            self.api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual(
            "You are already acivated. Please login to continue", api_response_json['message'])
        self.assertEqual('F0906', api_response_json['code'])
        self.assertEqual({}, api_response_json['data'])

    def test_get_profile_blank_password(self):
        self.params['vendor_details']['company'] = [2]
        self.params['vendor_details']['home_company'] = 2
        self.params['vendor_details']['branch'] = [2]
        self.params['vendor_details']['supervisor'] = [3]
        self.params['user_companies_currency'] = [
            {"2": {"air_currency": "JPY", "lcl_currency": "EUR", "fcl_currency": "EUR"}}]
        self.params['companies_mode'] = [{"2": ["FCLI", "FCLE"]}]

        response = client.post(
            self.vendor_add_post_api_url, data=self.params, format='json')
        self.api_response_json = json.loads(response.content)

        response = self.client.put(
            self.api_response_json['data'], data=ProfileRequestParams.set_profile_blank_password(), format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual("password is required", api_response_json['message'])
        self.assertEqual('F0914', api_response_json['code'])
        self.assertEqual({}, api_response_json['data'])

    def test_get_profile_mismatch_password(self):
        self.params['vendor_details']['company'] = [3]
        self.params['vendor_details']['home_company'] = 3
        self.params['vendor_details']['branch'] = [3]
        self.params['vendor_details']['supervisor'] = [5]
        self.params['user_companies_currency'] = [
            {"3": {"air_currency": "JPY", "lcl_currency": "EUR", "fcl_currency": "EUR"}}]
        self.params['companies_mode'] = [{"3": ["FCLI", "FCLE"]}]

        response = client.post(
            self.vendor_add_post_api_url, data=self.params, format='json')
        self.api_response_json = json.loads(response.content)

        response = self.client.put(
            self.api_response_json['data'], data=ProfileRequestParams.set_profile_mismatch_password(), format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual("password did not match",
                         api_response_json['message'])
        self.assertEqual('F0912', api_response_json['code'])
        self.assertEqual({}, api_response_json['data'])

    def test_set_profile_blank_confirm_password(self):
        self.params['vendor_details']['company'] = [5]
        self.params['vendor_details']['home_company'] = 5
        self.params['vendor_details']['branch'] = [5]
        self.params['vendor_details']['supervisor'] = [9]
        self.params['user_companies_currency'] = [
            {"5": {"air_currency": "JPY", "lcl_currency": "EUR", "fcl_currency": "EUR"}}]
        self.params['companies_mode'] = [{"5": ["FCLI", "FCLE"]}]

        response = client.post(
            self.vendor_add_post_api_url, data=self.params, format='json')
        self.api_response_json = json.loads(response.content)

        response = self.client.put(
            self.api_response_json['data'], data=ProfileRequestParams.set_profile_blank_confirm_password(), format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual(" confirm password is required",
                         api_response_json['message'])
        self.assertEqual('F0915', api_response_json['code'])
        self.assertEqual({}, api_response_json['data'])


    def test_set_profile_validation_on_contact_or_landline_no(self):
        self.params['vendor_details']['company'] = [6]
        self.params['vendor_details']['home_company'] = 6
        self.params['vendor_details']['branch'] = [6]
        self.params['vendor_details']['supervisor'] = [11]
        self.params['user_companies_currency'] = [
            {"6": {"air_currency": "JPY", "lcl_currency": "EUR", "fcl_currency": "EUR"}}]
        self.params['companies_mode'] = [{"6": ["FCLI", "FCLE"]}]

        response = client.post(
            self.vendor_add_post_api_url, data=self.params, format='json')
        self.api_response_json = json.loads(response.content)

        response = self.client.put(
            self.api_response_json['data'], data=ProfileRequestParams.set_profile_validation_on_contact_no(), format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual("Enter Either contact no or landline no.",
                         api_response_json['message'])
        self.assertEqual('F0919', api_response_json['code'])
        self.assertEqual({}, api_response_json['data'])

