from customer.models.customer import Customer
from django.test import TestCase, Client
from quote.models.quote import Quote
from quote.tests.api.v1.quote_request_params import QuoteRequestParams
from rest_framework import status
from rest_framework.test import APIClient
from utils.helpers import encode_data
import datetime
import json

# initialize the APIClient app
client = APIClient()


class TestQuoteCreate(TestCase):

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

    def test_quote_post(self):

        params = QuoteRequestParams.quote_valid_set()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Quote created successfully',
                         api_response['message'])
        self.assertEqual(None, api_response['data'])

    def test_quote_post_company_not_found(self):

        api_url = QuoteRequestParams.api_url() + '/api/v1/company/999999/quote/'

        params = QuoteRequestParams.quote_valid_set()

        response = client.post(api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Access denied.',
                         api_response['message'])
        self.assertEqual(None, api_response['data'])

    def test_quote_door_to_door_pickup_location_required(self):

        params = QuoteRequestParams.quote_invalid_params_for_door_to_door_pickup()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3002', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('pickup_location is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_quote_door_to_door_drop_location_required(self):

        params = QuoteRequestParams.quote_invalid_params_for_door_to_door_drop()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3005', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('drop_location is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_quote_port_to_port_air_port_required(self):

        params = QuoteRequestParams.quote_invalid_params_for_port_to_port_air()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3003', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('pickup_air_port is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_quote_port_to_port_sea_port_required(self):

        params = QuoteRequestParams.quote_invalid_params_for_port_to_port_FCL_and_LCL()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3004', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('pickup_sea_port is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_quote_arrival_date_is_backdated(self):

        params = QuoteRequestParams.date_validation()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('BEF0001', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('expected_arrival_date - Ensure this value is greater than or equal to '+str(datetime.date.today())+'.',
                         api_response['message'])
        self.assertEqual(['Ensure this value is greater than or equal to '+str(
            datetime.date.today())+'.'], api_response['data']['expected_arrival_date'])

    def test_quote_door_to_port_pickup_location_required(self):

        params = QuoteRequestParams.quote_invalid_params_for_door_to_port_air()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3002', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('pickup_location is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_quote_door_to_port_sea_port_required(self):

        params = QuoteRequestParams.quote_invalid_params_for_door_to_port_FCL_and_LCL()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3007', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('drop_sea_port is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_quote_port_to_door_drop_location_required(self):

        params = QuoteRequestParams.quote_invalid_params_for_port_to_door_air()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3005', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('drop_location is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_quote_port_to_door_pickup_sea_port_required(self):

        params = QuoteRequestParams.quote_invalid_params_for_port_to_door_LCL_and_FCL()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3004', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('pickup_sea_port is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_quote_air_courier_validation(self):

        params = QuoteRequestParams.quote_air_courier_validation()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3008', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('For Air_courier, personal_courier or commercial_courier is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_quote_transport_mode_should_not_blank(self):

        params = QuoteRequestParams.quote_create_transport_mode_should_not_blank()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3011', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Transport mode required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])
