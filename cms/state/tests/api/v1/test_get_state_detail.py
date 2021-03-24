from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from state.tests.api.v1.state_params import StateParams
import json

# initialize the APIClient app
client = APIClient()


class TestGetStateDetail(TestCase):

    fixtures = StateParams.get_seed_data_list()

    @classmethod
    def setUpTestData(cls):
        cls.api_url_host = StateParams.api_url()
        cls.get_country_list_url = cls.api_url_host + '/api/v1/country/'


    def tearDownTestCase(self):
        self._cleanup_record()


    # Get a State Detail with valid URL
    def test_state_detail_by_url(self):
        response = client.get(self.get_country_list_url + '1/state/3/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(200, response.data['code'])
        self.assertEqual('success', response.data['status'])
        self.assertEqual('State Data retrieved successfully.', response.data['message'])
        self.assertEqual(json.dumps(StateParams.get_state_detail_response_set()), json.dumps(response.data['data']))


    # Get a State Detail with invalid URL
    def test_state_detail_by_invalid_url(self):
        response = client.get(self.get_country_list_url + '1/state/99/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0706', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('state not found.', response.data['message'])
        self.assertEqual({}, response.data['data'])
