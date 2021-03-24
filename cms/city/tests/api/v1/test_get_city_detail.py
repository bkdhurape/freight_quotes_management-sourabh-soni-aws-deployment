from city.tests.api.v1.city_params import CityParams
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import json

# initialize the APIClient app
client = APIClient()


class TestGetCityDetail(TestCase):

    fixtures = CityParams.get_seed_data_list()

    @classmethod
    def setUpTestData(cls):
        cls.api_url_host = CityParams.api_url()
        cls.get_state_list_url = cls.api_url_host + '/api/v1/country/1/state/'


    def tearDownTestCase(self):
        self._cleanup_record()


    # Get a City Detail with valid URL
    def test_city_detail_by_url(self):
        response = client.get(self.get_state_list_url + '3/city/5/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(200, response.data['code'])
        self.assertEqual('success', response.data['status'])
        self.assertEqual('City Data retrieved successfully.', response.data['message'])
        self.assertEqual(json.dumps(CityParams.get_city_detail_response_set()), json.dumps(response.data['data']))


    # Get a City Detail with invalid URL
    def test_city_detail_by_invalid_url(self):
        response = client.get(self.get_state_list_url + '3/city/99/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0707', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('city not found.', response.data['message'])
        self.assertEqual({}, response.data['data'])
