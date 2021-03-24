from customer.models.customer import Customer
from django.test import TestCase
from quote.tests.api.v1.quote_request_params import QuoteRequestParams
from rest_framework import status
from rest_framework.test import APIClient
from transport.models.transport import Transport
from transport.tests.api.v1.transport_params import TransportParams
import json

# initialize the APIClient app
client = APIClient()


class TestGetTransport(TestCase):

    fixtures = TransportParams.get_seed_data_list()

    @classmethod
    def api_authentication(cls):
        client.credentials(HTTP_AUTHORIZATION=cls.jwt_token)

    @classmethod
    def setUpTestData(cls):
        cls.api_url_host = TransportParams.api_url()
        
        cls.customer_post_api_url = TransportParams.api_url() + \
            '/api/v1/customer/'
        cls.customer_register_params = QuoteRequestParams.post_customer_registration_personal_details_request_set(
            cls)
        response = client.post(cls.customer_post_api_url, data=json.dumps(
            cls.customer_register_params), content_type='application/json')
        api_response_json = json.loads(response.content)

        customer_name = cls.customer_register_params['customer_details']['name']
        cls.company_id = list(Customer.find_by(
            multi=True, name=customer_name).values_list('home_company', flat=True))[0]

        response = client.get(
            api_response_json['data'], content_type='application/json')

        response = client.post(QuoteRequestParams.api_url() + '/user/login/', data=json.dumps(
            QuoteRequestParams.login_valid_request_params(cls)), content_type='application/json')
        api_response_json = json.loads(response.content)

        cls.jwt_token = api_response_json['data'][0]['token']

        cls.api_authentication()

        cls.get_transport_list_url = cls.api_url_host + '/api/v1/transport/'
        cls.transport_id =  1

    def tearDownTestCase(self):
        self._cleanup_record()


    # Get a Transport List with valid URL
    def test_transport_list_by_url(self):
        response = client.get(self.get_transport_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(200, response.data['code'])
        self.assertEqual('success', response.data['status'])
        self.assertEqual('Transport Data retrieved successfully.', response.data['message'])

        data = response.data['data']

        for transport in data:
            self.assertIn('id', transport)
            self.assertIn('name', transport)
            self.assertIn('type', transport)
            self.assertIn('code', transport)
    
    def test_get_transport_based_on_id(self):
        transport = Transport.objects.latest('id')

        response = client.get(self.get_transport_list_url + str(transport.id) + '/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(200, response.data['code'])
        self.assertEqual('success', response.data['status'])
        self.assertEqual('Transport Data retrieved successfully.', response.data['message'])

        data = response.data['data']

        for transport in data:
            self.assertIn('id', transport)
            self.assertIn('name', transport)
            self.assertIn('type', transport)
            self.assertIn('code', transport)
    


