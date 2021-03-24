from company.tests.api.v1.company_request_parameters import CompanyRequestParams
from django.test import Client, TestCase
from login.tests.api.v1.request_response_params import RequestResponseParams
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
import json

# initialize the APIClient app
client = APIClient()


class TestAddCompany(APITestCase):

    fixtures = CompanyRequestParams.get_seed_data_list()
    def api_authentication(self):
        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)

    def setUp(self):
        self.api_url_host = RequestResponseParams.api_url()

        # Customer Registration
        response = client.post(self.api_url_host + '/api/v1/customer/',
                               data=json.dumps(
                                   CompanyRequestParams.post_register_required_request_params()),
                               content_type='application/json')
        api_response = json.loads(response.content)
        activation_link = api_response['data']
        client.get(activation_link)
        response = self.client.post(self.api_url_host + '/user/login/', data=json.dumps(
            RequestResponseParams.login_valid_request_params()), content_type='application/json')
        api_response_json = json.loads(response.content)

        self.jwt_token = api_response_json['data'][0]['token']
        self.api_authentication()

        self.company_post_api_url = CompanyRequestParams.api_url() + '/api/v1/company/'
        self.add_company_params = CompanyRequestParams.create_company_with_defaut_currency_based_on_home_country()

    def test_add_company_when_country_is_india(self):
        response =client.post(
            self.company_post_api_url, data=self.add_company_params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Company added successfully',
                         api_response_json['message'])
        self.assertEqual(2, api_response_json['data'])

    def test_create_company_with_blank_gst_when_country_is_india(self):
        params = CompanyRequestParams.create_company_with_blank_gst_when_country_is_india()
        response = client.post(
            self.company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('gst is required', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0008', api_response_json['code'])

    def test_create_company_with_blank_cin_when_country_is_india(self):
        params = CompanyRequestParams.create_company_with_blank_cin_when_country_is_india()
        response = client.post(
            self.company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('cin is required', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0010', api_response_json['code'])

    def test_create_company_with_blank_iec_when_country_is_india_and_customer_type_is_importer_or_exporter(self):
        params = CompanyRequestParams.create_company_with_blank_iec_when_country_is_india()
        response = client.post(
            self.company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('iec is required', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0011', api_response_json['code'])

    def test_create_company_with_blank_pan_when_country_is_india(self):
        params = CompanyRequestParams.create_company_with_blank_pan_when_country_is_india()
        response = client.post(
            self.company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('pan is required', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0009', api_response_json['code'])

    def test_create_company_with_invalid_pan_when_country_is_india(self):
        params = CompanyRequestParams.create_company_with_invalid_pan_when_country_is_india()
        response = client.post(
            self.company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual(
            'pan - Enter a valid value.Ensure this field has at least 10 characters.', api_response_json['message'])
        self.assertEqual({'pan': [
                         'Enter a valid value.', 'Ensure this field has at least 10 characters.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])

    def test_create_company_with_invalid_cin_when_country_is_india(self):
        params = CompanyRequestParams.create_company_with_invalid_cin_when_country_is_india()
        response = client.post(
            self.company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual(
            'cin - Enter a valid value.Ensure this field has at least 21 characters.', api_response_json['message'])
        self.assertEqual({'cin': [
                         'Enter a valid value.', 'Ensure this field has at least 21 characters.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])

    def test_create_company_with_invalid_gst_when_country_is_india(self):
        params = CompanyRequestParams.create_company_with_invalid_gst_when_country_is_india()
        response = client.post(
            self.company_post_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual(
            'gst - Enter a valid value.Ensure this field has at least 15 characters.', api_response_json['message'])
        self.assertEqual({'gst': [
                         'Enter a valid value.', 'Ensure this field has at least 15 characters.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])

    def test_create_company_with_invalid_iec_when_country_is_india_and_customer_type_is_importer_or_exporter(self):
        params = CompanyRequestParams.create_company_with_invalid_iec_when_country_is_india()
        response = client.post(
            self.company_post_api_url, data=params, format='json')

        api_response_json = json.loads(response.content)
        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual(
            'iec - Ensure this field has at least 10 characters.', api_response_json['message'])
        self.assertEqual(
            {'iec': ['Ensure this field has at least 10 characters.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])

    def test_create_company_when_country_is_other_than_india(self):
        params = CompanyRequestParams.create_company_valid_response_other_than_country_india()
        response = client.post(
            self.company_post_api_url, data=params, format='json')

        api_response_json = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Company added successfully',
                         api_response_json['message'])
        self.assertEqual(4, api_response_json['data'])
