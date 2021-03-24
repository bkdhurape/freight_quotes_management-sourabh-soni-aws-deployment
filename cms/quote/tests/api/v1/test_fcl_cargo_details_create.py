from customer.models.customer import Customer
from django.test import TestCase
from quote.tests.api.v1.package_details_request_params import PackageDetailsRequestParams
from quote.tests.api.v1.quote_request_params import QuoteRequestParams
from rest_framework import status
from rest_framework.test import APIClient
import json

# initialize the APIClient app
client = APIClient()


class TestFCLCargoDetailsCreate(TestCase):
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

        response = client.get(api_response_json['data'], content_type='application/json')

        response = client.post(QuoteRequestParams.api_url() + '/user/login/', data=json.dumps(
            QuoteRequestParams.login_valid_request_params(cls)), content_type='application/json')
        api_response_json = json.loads(response.content)

        cls.jwt_token = api_response_json['data']['token']
        cls.api_authentication()

        cls.quote_api_url = PackageDetailsRequestParams.api_url() + '/api/v1/company/' + str(cls.company_id) + '/quote/'

    def tearDownTestCase(self):
        self._cleanup_record()

    def test_fcl_cargo_details_create(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Quote created successfully.', api_response['message'])
        self.assertEqual(None, api_response['data'])

    def test_without_transport_mode(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_wo_transport_mode()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.assertEqual({"basic_details": {"transport_mode": ["This field is required."]}}, api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_blank_transport_mode(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_blank_transport_mode()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.assertEqual({"basic_details": {"transport_mode": ["This selection may not be empty."]}},
                         api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_invalid_transport_mode(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_invalid_transport_mode()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.assertEqual({"basic_details": {"transport_mode": ["\"FCL1\" is not a valid choice."]}},
                         api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_without_pickup_location(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_wo_pickup_location()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.assertEqual({"basic_details": {"pickup_location": ["This field is required."]}}, api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_without_pickup_location_street(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_wo_pickup_location_street()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.assertEqual({"basic_details": {"pickup_location": [{"street": ["This field is required."]}]}},
                         api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_without_pickup_location_country(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_wo_pickup_location_country()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.assertEqual({"basic_details": {"pickup_location": [{"country": ["This field is required."]}]}},
                         api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_null_pickup_location_country(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_null_pickup_location_country()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.assertEqual({"basic_details": {"pickup_location": [{"country": ["This field may not be null."]}]}},
                         api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_invalid_pickup_location_country(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_invalid_pickup_location_country()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.assertEqual({"basic_details": {"pickup_location": [{"country": ["Invalid country."]}]}},
                         api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_without_seaports(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_without_seaports()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.assertEqual({"basic_details": {"pickup_location": [{"seaport_ids": ["Seaport is required."]}]}},
                         api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_null_seaports(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_null_seaports()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.assertEqual({"basic_details": {"pickup_location": [{"seaport_ids": ["This field may not be null."]}]}},
                         api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_invalid_seaports(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_invalid_seaports()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        print("API RESPONSE =================================")
        print(api_response)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.maxDiff = None
        self.assertEqual({"basic_details": {"pickup_location": [{"seaport_ids": {"0": ["Invalid seaport id"]}}]}},
                         api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_without_shipment_terms(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_wo_shipment_terms()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.assertEqual({"basic_details": {"shipment_terms": ["This field is required."]}},
                         api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_blank_shipment_terms(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_blank_shipment_terms()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.assertEqual({"basic_details": {"shipment_terms": ["\"\" is not a valid choice."]}},
                         api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_null_shipment_terms(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_null_shipment_terms()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.assertEqual({"basic_details": {"shipment_terms": ["This field may not be null."]}},
                         api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_without_expected_delivery_date(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_wo_expected_delivery_date()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.assertEqual({"basic_details": {"expected_delivery_date": ["Expected delivery date is required."]}},
                         api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_blank_expected_delivery_date(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_blank_expected_delivery_date()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.maxDiff = None
        self.assertEqual({"basic_details": {
            "expected_delivery_date": ["Date has wrong format. Use one of these formats instead: YYYY-MM-DD."]}},
            api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_dock_stuffing_destuffing(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_dock_stuffing_destuffing()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.maxDiff = None
        self.assertEqual({"cargo_details": [{"containers": [{"packages": ["Package(s) is required."]}]}, {}]},
                         api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_container_stuffing_dock_wo_commodity(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_container_stuffing_dock_wo_commodity()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.maxDiff = None
        self.assertEqual(
            {"cargo_details": [{"containers": [{"packages": [{"commodity": ["Commodity is required."]}]}]}, {}]},
            api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_container_stuffing_dock_wo_hazardous(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_container_stuffing_dock_wo_hazardous()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.maxDiff = None
        self.assertEqual(
            {"cargo_details": [{"containers": [{"packages": [{"is_hazardous": ["Hazardous is required."]}]}]}, {}]},
            api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_container_stuffing_dock_wo_stackable(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_container_stuffing_dock_wo_stackable()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.maxDiff = None
        self.assertEqual(
            {"cargo_details": [{"containers": [{"packages": [{"is_stackable": ["Stackable is required."]}]}]}, {}]},
            api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_container_stuffing_factory_wo_commodity(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_container_stuffing_factory_wo_commodity()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.assertEqual(
            {"cargo_details": [{"containers": [{"commodity": ["Commodity is required."]}]}, {}]},
            api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_container_stuffing_factory_wo_hazardous(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_container_stuffing_factory_wo_hazardous()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.assertEqual(
            {"cargo_details": [{"containers": [{"is_hazardous": ["Hazardous is required."]}]}, {}]},
            api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_container_stuffing_factory_wo_stackable(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_container_stuffing_factory_wo_stackable()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.assertEqual(
            {"cargo_details": [{"containers": [{"is_stackable": ["Stackable is required."]}]}, {}]},
            api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_container_type_fr_wo_dimen(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_container_type_fr_wo_dimen()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.maxDiff = None
        self.assertEqual(
            {"cargo_details": [{"containers": [
                {"packages": [{"non_field_errors": ["For Flatrack container type, only dimensions are required"]}]}]},
                {}]},
            api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_container_type_rf_wo_shipper_details(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_container_type_rf_wo_shipper_details()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.maxDiff = None
        self.assertEqual(
            {"cargo_details": [{"containers": [{"shipper_details": ["Shipper details is required."]}]}, {}]},
            api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_container_type_rf_wo_temp(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_container_type_rf_wo_temp()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.maxDiff = None
        self.assertEqual(
            {"cargo_details": [{"containers": [{"temperature": ["Temperature is required."]}]}, {}]},
            api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_container_type_rf_wo_temp_unit(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_container_type_rf_wo_temp_unit()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.maxDiff = None
        self.assertEqual(
            {"cargo_details": [{"containers": [{"temperature_unit": ["Temperature unit is required."]}]}, {}]},
            api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_container_type_ot_wo_package(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_container_type_ot_wo_package()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.maxDiff = None
        self.assertEqual(
            {"cargo_details": [{"containers": [{"packages": ["Package(s) is required."]}]}, {}]},
            api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_multi_drop_dock_destuffing(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_multi_drop_dock_destuffing()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.maxDiff = None
        self.assertEqual(
            {"cargo_details": [
                {"containers": [{"destuffing": ["For multiple drop location, only dock destuffing is required"]}]},
                {}]},
            api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_container_type_tank_wo_consignee(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_container_type_tank_wo_consignee()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.maxDiff = None
        self.assertEqual(
            {"cargo_details": [{"containers": [{"consignee_details": ["Consignee details is required."]}]}, {}]},
            api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_stuffing_factory_diff_loc(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_container_type_factory_diff_loc()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.maxDiff = None
        self.assertEqual(
            {"cargo_details": [{}, {"containers": [
                {"non_field_errors": ["For factory stuffing, package needs to be from same location."]}]}]},
            api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_non_rf_with_temp_cont_package(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_non_rf_with_temp_cont_package()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.maxDiff = None
        self.assertEqual(
            {"cargo_details": [{}, {"containers": [
                {"non_field_errors": ["Cannot add temperature controlled packages in this type of container"]}]}]},
            api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])

    def test_same_loc_diff_temp(self):
        params = PackageDetailsRequestParams.quote_fcl_valid_set_same_loc_diff_temp()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        api_response = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('error', api_response['status'])
        self.assertEqual(None, api_response['message'])
        self.maxDiff = None
        self.assertEqual(
            {"cargo_details": [{}, {"containers": [
                {"non_field_errors": ["Same container cannot be used for different temperature packages."]}]}]},
            api_response['errors'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, api_response['code'])
