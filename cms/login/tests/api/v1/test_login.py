from customer.tests.api.v1.customer_params import CustomerParams
from django.core.management import call_command
from django.test import TestCase
from login.tests.api.v1.request_response_params import RequestResponseParams
from rest_framework import status
from rest_framework.test import APIClient
import json


# initialize the APIClient app
client = APIClient()


class TestLogin(TestCase):

    def setUp(self):
        call_command('loaddata', 'country/fixtures/country.json')
        call_command('loaddata', 'state/fixtures/state.json')
        call_command('loaddata', 'city/fixtures/city.json')
        call_command('loaddata', 'commodity/fixtures/commodity.json')
        call_command('loaddata', 'region/fixtures/region.json')

        self.api_url_host = RequestResponseParams.api_url()

        # Customer Registration
        response = client.post(self.api_url_host + '/api/v1/customer/', 
            data=json.dumps(CustomerParams.post_register_required_request_params()), 
            content_type='application/json')
        api_response = json.loads(response.content)
        activation_link = api_response['data']
        self.client.get(activation_link)

    def api_authentication(self):
        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)

    def login_valid_request_params(self):
        response = client.post(self.api_url_host + '/user/login/', data=json.dumps(RequestResponseParams.login_valid_request_params()), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Login successfully.', api_response['message'])
        self.assertEqual(200, api_response['code'])
        self.jwt_token = api_response['data'][0]['token']
        self.api_authentication()

    def fetch_customer_list_with_missing_token(self):
        client.credentials()
        response = client.get(self.api_url_host + '/api/v1/company/1/customer/', headers={'Authorization':'qwe'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Token missing in header.', api_response['message'])
        self.assertEqual(200, api_response['code'])
        self.assertEqual(None, api_response['data'])

    def fetch_customer_list_with_invalid_token(self):
        client.credentials(HTTP_AUTHORIZATION='qwe.wer.ert')
        response = client.get(self.api_url_host + '/api/v1/company/1/customer/', headers={'Authorization':'qwe'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Invalid token.', api_response['message'])
        self.assertEqual(200, api_response['code'])
        self.assertEqual(None, api_response['data'])

    def after_login_get_customer_list(self):
        self.api_authentication()
        response = client.get(self.api_url_host + '/api/v1/company/1/customer/', headers={'Authorization':'qwe'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Customer Data retrieved successfully.', api_response['message'])
        self.assertEqual(200, api_response['code'])
        self.assertEqual(RequestResponseParams.after_login_get_customer_list_response_params(), api_response['data'])

    def after_login_get_vendor_list(self):
        self.api_authentication()
        response = client.get(self.api_url_host + '/api/v1/company/1/vendor/', headers={'Authorization':'qwe'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Access denied.', api_response['message'])
        self.assertEqual(200, api_response['code'])
        self.assertEqual(None, api_response['data'])

    def logout_user(self):
        response = client.get(self.api_url_host + '/user/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Logout successfully.', api_response['message'])
        self.assertEqual(200, api_response['code'])
        self.assertEqual(None, api_response['data'])

    def after_logout_get_customer_list(self):
        response = client.get(self.api_url_host + '/api/v1/company/1/customer/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Login again token expired.', api_response['message'])
        self.assertEqual(200, api_response['code'])
        self.assertEqual(None, api_response['data'])

    def test_login(self):
        self.login_valid_request_params()
        self.fetch_customer_list_with_missing_token()
        self.fetch_customer_list_with_invalid_token()
        self.after_login_get_customer_list()
        self.after_login_get_vendor_list()
        self.logout_user()
        self.after_logout_get_customer_list()
