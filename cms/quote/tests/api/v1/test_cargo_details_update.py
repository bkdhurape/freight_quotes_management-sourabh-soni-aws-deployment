from customer.models.customer import Customer
from django.test import TestCase, Client
from quote.models.package_details import PackageDetails
from quote.models.quote import Quote
from quote.tests.api.v1.package_details_request_params import PackageDetailsRequestParams
from quote.tests.api.v1.quote_request_params import QuoteRequestParams
from rest_framework import status
from rest_framework.test import APIClient
import json

# initialize the APIClient app
client = APIClient()

class TestCargoDetailsUpdate(TestCase):

    fixtures = PackageDetailsRequestParams.get_seed_data_list()

    @classmethod
    def api_authentication(cls):
        client.credentials(HTTP_AUTHORIZATION=cls.jwt_token)

    @classmethod
    def setUpTestData(cls):
        cls.customer_post_api_url = PackageDetailsRequestParams.api_url() + \
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

        cls.quote_api_url = PackageDetailsRequestParams.api_url() + '/api/v1/company/' + \
            str(cls.company_id) + '/quote/'

        params = PackageDetailsRequestParams.quote_valid_set()

        response = client.post(cls.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        quote = Quote.objects.latest('id')
        cls.quote_id = quote.id

        cls.package_details_url = PackageDetailsRequestParams.api_url(
        ) + '/api/v1/company/'+ str(cls.company_id) +'/quote/'+str(cls.quote_id)+'/package_details/'

        cls.cargo_details_url = PackageDetailsRequestParams.api_url(
        ) + '/api/v1/company/'+ str(cls.company_id) +'/quote/'+str(cls.quote_id)+'/cargo_details/'

        params = PackageDetailsRequestParams.cargo_details_set()

        response = client.post(cls.cargo_details_url, data=json.dumps(
            params), content_type='application/json')

        package_details = PackageDetails.objects.latest('id')
        cls.package_details_id = package_details.id


    def tearDownTestCase(self):
        self._cleanup_record()

    def test_cargo_details_update(self):

        params = PackageDetailsRequestParams.cargo_details_set()
        params['id'] = self.package_details_id

        response = client.put(self.cargo_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Cargo Details updated successfully',
                         api_response['message'])
        self.assertEqual(None, api_response['data'])


    def test_cargo_details_update_without_id(self):

        params = PackageDetailsRequestParams.cargo_details_set()

        response = client.put(self.cargo_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3165', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Cargo details id is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_cargo_details_update_with_invalid_id(self):

        params = PackageDetailsRequestParams.cargo_details_set()
        params['id'] = 999999999

        response = client.put(self.cargo_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3164', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Cannot update cargo details with invalid id',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])
