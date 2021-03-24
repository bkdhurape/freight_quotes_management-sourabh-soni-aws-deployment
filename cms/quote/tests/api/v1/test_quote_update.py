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


class TestQuoteUpdate(TestCase):

    fixtures = QuoteRequestParams.get_seed_data_list()

    @classmethod
    def api_authentication(cls):
        client.credentials(HTTP_AUTHORIZATION=cls.jwt_token)

    @classmethod
    def setUpTestData(cls):
        cls.customer_post_api_url = QuoteRequestParams.api_url() + \
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

        cls.quote_api_url = QuoteRequestParams.api_url() + '/api/v1/company/' + \
            str(cls.company_id) + '/quote/'

        params = QuoteRequestParams.quote_valid_set()

        response = client.post(cls.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        cls.quote = Quote.objects.latest('id')

        cls.quote_id_url = QuoteRequestParams.api_url() + '/api/v1/company/' + \
            str(cls.company_id) + '/quote/'+str(cls.quote.id)+'/'

    def test_update_quote_with_air_courier(self):

        params = QuoteRequestParams.quote_update_air_courier_validation()
        response = client.put(self.quote_id_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3008', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('For Air_courier, personal_courier or commercial_courier is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_update_quote(self):

        params = QuoteRequestParams.quote_update_valid_set()
        response = client.put(self.quote_id_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Quote data updated successfully',
                         api_response['message'])
        self.assertEqual(None, api_response['data'])

    def test_update_quote_data_not_found(self):

        quote_id_url = QuoteRequestParams.api_url() + '/api/v1/company/' + \
            str(self.company_id) + '/quote/999999/'

        params = QuoteRequestParams.quote_update_valid_set()
        response = client.put(quote_id_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3001', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Quote not found',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_update_quote_access_denied(self):

        quote_id_url = QuoteRequestParams.api_url() + '/api/v1/company/9999/quote/' + \
            str(self.quote.id)+'/'

        params = QuoteRequestParams.quote_update_valid_set()
        response = client.put(quote_id_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Access denied.',
                         api_response['message'])
        self.assertEqual(None, api_response['data'])

    def test_update_quote_sea_port_validation(self):

        params = QuoteRequestParams.quote_update_sea_port_validation()
        response = client.put(self.quote_id_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3004', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('pickup_sea_port is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_update_quote_location_required(self):

        params = QuoteRequestParams.quote_update_door_to_door_validation()
        response = client.put(self.quote_id_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3002', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('pickup_location is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_update_quote_expected_delivery_date_required_for_door(self):

        params = QuoteRequestParams.quote_update_quote_expected_deliver_date_reuired_for_door()
        response = client.put(self.quote_id_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3010', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Expected delivery date is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_quote_update_transport_mode_should_not_blank(self):

        params = QuoteRequestParams.quote_create_transport_mode_should_not_blank()

        response = client.put(self.quote_id_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3011', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Transport mode required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])
