from company.tests.api.v1.company_request_parameters import CompanyRequestParams
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json

client = APIClient()

class TestAddCompany(APITestCase):

    fixtures = VendorRequestParams.get_seed_data_list()
    def api_authentication(self):
        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)

    def setUp(self):
        self.vendor_post_api_url = VendorRequestParams.api_url() + '/api/v1/vendor/'
        self.vendor_register_params = VendorRequestParams.post_vendor_registration_personal_details_request_set()
        self.params = VendorRequestParams.post_add_vendor_valid_request_set()

        response = self.client.post(
            self.vendor_post_api_url, data=self.vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        vendor_name = self.vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(
            multi=True, name=vendor_name).values_list('id', 'home_company'))[0]
        self.vendor_id, self.company_id = vendor

        encoded_email = encode_data(
            self.vendor_register_params['vendor_details']['email'])
        test_vendor_send_activation_link_api_url = VendorRequestParams.api_url(
        ) + '/api/v1/company/' + str(self.company_id) + '/vendor/send_activation_link/' + encoded_email

        response = self.client.get(
            test_vendor_send_activation_link_api_url, format='json')
        self.final_api_response_json = json.loads(response.content)
        self.vendor_add_post_api_url = VendorRequestParams.api_url(
        ) + '/api/v1/company/' + str(self.company_id) + '/vendor/'

        response = self.client.get(
            self.final_api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        response = self.client.post(VendorRequestParams.api_url(
        ) + '/user/login/', data=VendorRequestParams.login_valid_request_params(), format='json')
        api_response_json = json.loads(response.content)
        self.jwt_token = api_response_json['data'][0]['token']
        self.api_authentication()
        self.add_company_post_api_url = VendorRequestParams.api_url() + '/api/v1/company/'

    def test_add_company_valid_incorporation_year_in_vendor(self):
        params = CompanyRequestParams.add_new_company_for_vendor()
        response = client.post(
            self.add_company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Company added successfully',
                         api_response_json['message'])
        self.assertEqual(5, api_response_json['data'])

    def test_add_company_invalid_incorporation_year_in_vendor(self):
        params = CompanyRequestParams.create_company_with_invalid_incorporation_year_with_string_for_vendor()
        response = client.post(
            self.add_company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual(
            "incorporation_year - A valid integer is required.", api_response_json['message'])
        self.assertEqual({'incorporation_year': [
                         'A valid integer is required.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])

    def test_add_company_invalid_incorporation_year_less_than_year_in_vendor(self):
        params = CompanyRequestParams.create_company_with_invalid_incorporation_year_with_less_year_for_vendor()
        response = client.post(
            self.add_company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)
        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual(
            "incorporation_year - Ensure this value is greater than or equal to 1970.", api_response_json['message'])
        self.assertEqual({'incorporation_year': [
                         'Ensure this value is greater than or equal to 1970.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])

    def test_add_company_invalid_incorporation_year_max_than_current_year_in_vendor(self):
        params = CompanyRequestParams.create_company_with_invalid_incorporation_year_with_more_than_current_year_for_vendor()
        response = client.post(
            self.add_company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual(
            'incorporation_year - Ensure this value is less than or equal to 2020.', api_response_json['message'])
        self.assertEqual({'incorporation_year': [
                         'Ensure this value is less than or equal to 2020.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])

    def test_add_company_when_country_is_india(self):
        params = CompanyRequestParams.add_new_company_for_vendor()
        response = client.post(
            self.add_company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Company added successfully',
                         api_response_json['message'])
        self.assertEqual(7, api_response_json['data'])

    def test_create_company_with_blank_gst_when_country_is_india(self):
        params = CompanyRequestParams.create_company_with_blank_gst_when_country_is_india_for_vendor()
        response = client.post(
            self.add_company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('gst is required', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0008', api_response_json['code'])

    def test_create_company_with_blank_cin_when_country_is_india(self):
        params = CompanyRequestParams.create_company_with_blank_cin_when_country_is_india_for_vendor()
        response = client.post(
            self.add_company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('cin is required', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0010', api_response_json['code'])

    def test_create_company_with_blank_pan_when_country_is_india(self):
        params = CompanyRequestParams.create_company_with_blank_pan_when_country_is_india_for_vendor()
        response = client.post(
            self.add_company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('pan is required', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0009', api_response_json['code'])

    def test_create_company_with_invalid_pan_when_country_is_india(self):
        params = CompanyRequestParams.create_company_with_invalid_pan_when_country_is_india_for_vendor()
        response = client.post(
            self.add_company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual(
            'pan - Enter a valid value.Ensure this field has at least 10 characters.', api_response_json['message'])
        self.assertEqual({'pan': [
                         'Enter a valid value.', 'Ensure this field has at least 10 characters.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])

    def test_create_company_with_invalid_cin_when_country_is_india(self):
        params = CompanyRequestParams.create_company_with_invalid_cin_when_country_is_india_for_vendor()
        response = client.post(
            self.add_company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual(
            'cin - Enter a valid value.Ensure this field has at least 21 characters.', api_response_json['message'])
        self.assertEqual({'cin': [
                         'Enter a valid value.', 'Ensure this field has at least 21 characters.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])

    def test_create_company_with_invalid_gst_when_country_is_india(self):
        params = CompanyRequestParams.create_company_with_invalid_gst_when_country_is_india_for_vendor()
        response = client.post(
            self.add_company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual(
            'gst - Enter a valid value.Ensure this field has at least 15 characters.', api_response_json['message'])
        self.assertEqual({'gst': [
                         'Enter a valid value.', 'Ensure this field has at least 15 characters.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])

    def test_create_company_when_country_is_other_than_india(self):
        params = CompanyRequestParams.create_company_other_than_country_india()
        response = client.post(
            self.add_company_post_api_url, data=params, format='json')

        api_response_json = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Company added successfully',
                         api_response_json['message'])
        self.assertEqual(9, api_response_json['data'])
