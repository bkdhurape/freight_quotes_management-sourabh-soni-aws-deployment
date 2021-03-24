from country.tests.api.v1.country_params import CountryParams
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import json

# initialize the APIClient app
client = APIClient()


class TestGetCountryList(TestCase):

    fixtures = CountryParams.get_seed_data_list()

    @classmethod
    def setUpTestData(cls):
        cls.api_url_host = CountryParams.api_url()
        cls.get_country_list_url = cls.api_url_host + '/api/v1/country/'


    def tearDownTestCase(self):
        self._cleanup_record()


    # Get a Country List with valid URL
    def test_country_list_by_url(self):
        response = client.get(self.get_country_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(200, response.data['code'])
        self.assertEqual('success', response.data['status'])
        self.assertEqual('Country Data retrieved successfully.', response.data['message'])
        self.assertEqual(json.dumps(CountryParams.get_country_list_response_set()), json.dumps(response.data['data']))
