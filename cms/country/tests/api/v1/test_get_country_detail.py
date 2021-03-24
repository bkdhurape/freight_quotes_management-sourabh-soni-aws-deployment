from country.tests.api.v1.country_params import CountryParams
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import json

# initialize the APIClient app
client = APIClient()


class TestGetCountryDetail(TestCase):

    fixtures = CountryParams.get_seed_data_list()

    @classmethod
    def setUpTestData(cls):
        cls.api_url_host = CountryParams.api_url()
        cls.get_country_list_url = cls.api_url_host + '/api/v1/country/'


    def tearDownTestCase(self):
        self._cleanup_record()


    # Get a Country Detail with valid URL
    def test_country_detail_by_url(self):
        response = client.get(self.get_country_list_url + '3/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(200, response.data['code'])
        self.assertEqual('success', response.data['status'])
        self.assertEqual('Country Data retrieved successfully.', response.data['message'])
        self.assertEqual(json.dumps(CountryParams.get_country_detail_response_set()), json.dumps(response.data['data']))


    # Get a Country Detail with invalid URL
    def test_country_detail_by_invalid_url(self):
        response = client.get(self.get_country_list_url + '99/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0705', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('country not found.', response.data['message'])
        self.assertEqual({}, response.data['data'])
