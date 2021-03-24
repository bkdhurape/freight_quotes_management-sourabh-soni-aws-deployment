from address.models.address import Address
from customer.models.customer import Customer
from django.test import TestCase, Client
from quote.models.quote import Quote
from quote.models.quote_transport_mode import QuoteTransportMode
from quote.tests.api.v1.additional_details_request_params import AdditionalDetailsRequestParams
from quote.tests.api.v1.quote_request_params import QuoteRequestParams
from rest_framework import status
from rest_framework.test import APIClient
from utils.helpers import encode_data
import json

# initialize the APIClient app
client = APIClient()

class TestAdditionalDetailsCreate(TestCase):

    fixtures = AdditionalDetailsRequestParams.get_seed_data_list()

    @classmethod
    def api_authentication(cls):
        client.credentials(HTTP_AUTHORIZATION=cls.jwt_token)

    @classmethod
    def setUpTestData(cls):
        cls.customer_post_api_url = AdditionalDetailsRequestParams.api_url() + \
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

        cls.quote_api_url = AdditionalDetailsRequestParams.api_url() + '/api/v1/company/' + \
            str(cls.company_id) + '/quote/'

        params = AdditionalDetailsRequestParams.quote_valid_set()

        response = client.post(cls.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        quote = Quote.objects.latest('id')
        cls.quote_id = quote.id

        cls.additional_details_url = AdditionalDetailsRequestParams.api_url(
        ) + '/api/v1/company/'+str(cls.company_id)+'/quote/'+str(cls.quote_id)+'/additional_details/'

    def tearDownTestCase(self):
        self._cleanup_record()

    def test_additional_details_create(self):

        params = AdditionalDetailsRequestParams.additional_details_valid_set()

        response = client.post(self.additional_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Additional details added successfully',
                         api_response['message'])
        self.assertEqual(None, api_response['data'])

    def test_additional_details_quote_not_found(self):

        additional_details_api_url = AdditionalDetailsRequestParams.api_url(
        ) + '/api/v1/company/'+str(self.company_id)+'/quote/999999999999/additional_details/'

        params = AdditionalDetailsRequestParams.additional_details_valid_set()

        response = client.post(additional_details_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3001', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Quote not found',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_additional_details_required_field(self):

        params = AdditionalDetailsRequestParams.additional_details_invalid_set()

        response = client.post(self.additional_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3101', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('No of suppliers required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_additional_details_can_not_select_both(self):

        params = AdditionalDetailsRequestParams.additional_details_can_not_select_both()

        response = client.post(self.additional_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3104', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('You can select either preference or depreference not both at the same time',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_addional_details_maximum_five_preference(self):

        params = AdditionalDetailsRequestParams.additional_details_maximum_five_preference_can_be_selected()

        response = client.post(self.additional_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3102', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('You can select only five airlines',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])
        
    def test_addional_details_maximum_five_depreference(self):

        params = AdditionalDetailsRequestParams.additional_details_maximum_five_depreference_can_be_selected()

        response = client.post(self.additional_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3103', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('You can depreference only five airlines',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])
        

    