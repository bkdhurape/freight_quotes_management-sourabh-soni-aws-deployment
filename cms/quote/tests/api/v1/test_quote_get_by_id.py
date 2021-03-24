from customer.models.customer import Customer
from django.test import TestCase, Client
from quote.models.quote import Quote
from quote.models.quote_transport_mode import QuoteTransportMode
from quote.tests.api.v1.quote_request_params import QuoteRequestParams
from rest_framework import status
from rest_framework.test import APIClient
from utils.helpers import encode_data
import json

# initialize the APIClient app
client = APIClient()


class TestQuoteGetById(TestCase):

    fixtures = QuoteRequestParams.get_seed_data_list()

    def api_authentication(self):
        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)

    def setUp(self):
        self.customer_post_api_url = QuoteRequestParams.api_url() + \
            '/api/v1/customer/'
        self.customer_register_params = QuoteRequestParams.post_customer_registration_personal_details_request_set(
            self)

        response = client.post(self.customer_post_api_url, data=json.dumps(
            self.customer_register_params), content_type='application/json')
        api_response_json = json.loads(response.content)

        customer_name = self.customer_register_params['customer_details']['name']
        self.company_id = list(Customer.find_by(
            multi=True, name=customer_name).values_list('home_company', flat=True))[0]

        response = client.get(
            api_response_json['data'], content_type='application/json')
        response = client.post(QuoteRequestParams.api_url() + '/user/login/', data=json.dumps(
            QuoteRequestParams.login_valid_request_params(self)), content_type='application/json')
        api_response_json = json.loads(response.content)

        self.jwt_token = api_response_json['data'][0]['token']
        self.api_authentication()

        self.quote_api_url = QuoteRequestParams.api_url() + '/api/v1/company/' + \
            str(self.company_id) + '/quote/'

        params = QuoteRequestParams.quote_valid_set()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        self.quote = Quote.objects.latest('id')

    def test_quote_get_by_id(self):

        quote_id_url = QuoteRequestParams.api_url() + '/api/v1/company/' + \
            str(self.company_id) + '/quote/'+str(self.quote.id)+'/'

        response = client.get(quote_id_url)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Quote data retrived successfully',
                         api_response['message'])

        quote = api_response['data']
        quote_keys = QuoteRequestParams.quote_get_all_keys()

        for quote_key in quote_keys:
            self.assertIn(quote_key, quote)

    def test_quote_get_company_not_found(self):

        api_url = QuoteRequestParams.api_url() + '/api/v1/company/999999/quote/' + \
            str(self.quote.id)+'/'

        response = client.get(api_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Access denied.',
                         api_response['message'])
        self.assertEqual(None, api_response['data'])

    def test_quote_get_data_not_found(self):

        api_url = QuoteRequestParams.api_url() + '/api/v1/company/' + \
            str(self.company_id)+'/quote/999999/'

        response = client.get(api_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3001', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Quote not found',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])
