from customer.models.customer import Customer
from django.test import TestCase
from quote.models.package_details import PackageDetails
from quote.models.quote import Quote
from quote.tests.api.v1.package_details_request_params import PackageDetailsRequestParams
from quote.tests.api.v1.quote_request_params import QuoteRequestParams
from rest_framework import status
from rest_framework.test import APIClient
import json

# initialize the APIClient app
client = APIClient()


class TestPackageDetailsCreate(TestCase):

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
        ) + '/api/v1/company/'+str(cls.company_id)+'/quote/'+str(cls.quote_id)+'/package_details/'

    def tearDownTestCase(self):
        self._cleanup_record()

    def test_package_details_create_air(self):

        params = PackageDetailsRequestParams.package_details_valid_set_air()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Package details added successfully',
                         api_response['message'])
        self.assertEqual(None, api_response['data'])


    def test_package_details_pickup_location_invalid(self):

        params = PackageDetailsRequestParams.package_details_invalid_pickup_location()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4002', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('For the selected quote this pickup location is not found',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_package_details_drop_location_invalid(self):

        params = PackageDetailsRequestParams.package_details_invalid_drop_location()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4003', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('For the selected quote this drop location is not found',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_package_details_invalid_transport_mode(self):

        params = PackageDetailsRequestParams.package_details_invalid_transport_mode()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4004', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('For the selected quote this transport mode is not found',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_package_details_air_type_required(self):

        params = PackageDetailsRequestParams.package_details_air_type_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4009', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('type is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_package_details_air_length_required(self):

        params = PackageDetailsRequestParams.package_details_air_length_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4011', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('length is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_package_details_air_width_required(self):

        params = PackageDetailsRequestParams.package_details_air_width_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4012', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('width is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_package_details_air_height_required(self):

        params = PackageDetailsRequestParams.package_details_air_height_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4013', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('height is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_package_details_air_dimension_unit_required(self):

        params = PackageDetailsRequestParams.package_details_air_dimension_unit_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4014', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('dimension_unit is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_package_details_air_weight_required(self):

        params = PackageDetailsRequestParams.package_details_air_weight_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4015', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('weight is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_package_details_air_weight_unit_required(self):

        params = PackageDetailsRequestParams.package_details_air_weight_unit_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4016', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('weight_unit is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_package_details_quote_not_found(self):

        package_details_api_url = PackageDetailsRequestParams.api_url(
        ) + '/api/v1/company/'+str(self.company_id)+'/quote/9999/package_details/'

        params = PackageDetailsRequestParams.package_details_valid_set_air()

        response = client.post(package_details_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F3001', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Quote not found',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_package_details_check_for_negative_value(self):

        params = PackageDetailsRequestParams.package_details_check_for_negative_value()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('BEF0001', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('quantity - Ensure this value is greater than or equal to 0.',
                         api_response['message'])
        self.assertEqual(
            ['Ensure this value is greater than or equal to 0.'], api_response['data']['quantity'])

    def test_package_details_access_denied(self):

        package_details_api_url = PackageDetailsRequestParams.api_url(
        ) + '/api/v1/company/99999/quote/'+str(self.quote_id)+'/package_details/'

        params = PackageDetailsRequestParams.package_details_valid_set_air()

        response = client.post(package_details_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Access denied.',
                         api_response['message'])
        self.assertEqual(None, api_response['data'])

    def test_package_details_invalid_port_id(self):

        self.quote_api_url = PackageDetailsRequestParams.api_url() + '/api/v1/company/' + \
            str(self.company_id) + '/quote/'

        params = PackageDetailsRequestParams.quote_valid_set_for_port_to_port()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        quote_id = Quote.objects.latest('id')

        package_details_url = PackageDetailsRequestParams.api_url() + '/api/v1/company/' + \
            str(self.company_id) + '/quote/' + \
            str(quote_id.id) + '/package_details/'

        package_details_params = PackageDetailsRequestParams.package_details_invalid_set_port_to_port()

        response = client.post(package_details_url, data=json.dumps(
            package_details_params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4019', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Entered pickup_sea_port does not belong to selected quote',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_package_details_temperature_validation_for_air(self):

        params = PackageDetailsRequestParams.package_details_temperature_validation_for_air()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4038', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Temperature is required for Air',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_package_details_temperature_unit_validation_for_air(self):

        params = PackageDetailsRequestParams.package_details_temperature_unit_validation_for_air()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4039', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Temperature unit is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])
