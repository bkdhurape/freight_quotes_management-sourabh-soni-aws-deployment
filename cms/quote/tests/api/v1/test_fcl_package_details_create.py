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


    def test_package_details_create_fcl(self):

        params = PackageDetailsRequestParams.package_details_valid_set_fcl()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Package details added successfully',
                         api_response['message'])
        self.assertEqual(None, api_response['data'])

    def test_package_details_fcl_with_type_and_container_type(self):

        params = PackageDetailsRequestParams.package_details_fcl_type_and_container_type_set()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Package details added successfully',
                         api_response['message'])
        self.assertEqual(None, api_response['data'])


    def test_package_details_fcl_type_or_container_type_required(self):

        params = PackageDetailsRequestParams.package_details_check_for_fcl_type_or_container_type_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4017', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('For FCL, either type or container_type is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_package_details_fcl_container_subtype_required(self):

        params = PackageDetailsRequestParams.package_details_check_fcl_container_subtype_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4030', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Container subtype is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_package_details_fcl_no_of_containers_required(self):

        params = PackageDetailsRequestParams.package_details_fcl_no_of_containers_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4006', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('For FCL, no_of_containers is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_package_details_fcl_stuffing_required(self):

        params = PackageDetailsRequestParams.package_details_fcl_stuffing_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')


        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4007', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('For FCL, stuffing is required',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_package_details_fcl_destuffing_required(self):

        params = PackageDetailsRequestParams.package_details_fcl_destuffing_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4008', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('For FCL, destuffing is required',
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



    def test_package_details_create_fcl_with_dock_stuffing(self):

        params = PackageDetailsRequestParams.package_details_fcl_with_dock_stuffing_and_without_packages_set()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)


        self.assertEqual('F4028', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Please add package to this container',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_package_details_create_fcl_with_dock_stuffing_and_invalid_packages_id(self):

        params = PackageDetailsRequestParams.package_details_fcl_with_dock_stuffing_and_invalid_packages_id_set()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4029', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Selected package(s) does not belong to this quote or transport mode',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_package_details_create_fcl_with_dock_stuffing_and_packages(self):

        params = PackageDetailsRequestParams.quote_valid_set_with_single_pickup_and_multi_drop()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        quote = Quote.objects.latest('id')
        quote_id = quote.id

        package_details_url = PackageDetailsRequestParams.api_url(
        ) + '/api/v1/company/'+str(self.company_id)+'/quote/'+str(quote_id)+'/package_details/'


        params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_loose_cargo_set()
        params['transport_mode'] = [7]
        params['pickup_location'] = 16
        params['loose_cargo']['packages'][0]['drop_location'] = 17
        response = client.post(package_details_url, data=json.dumps(
            params), content_type='application/json')

        package_details = PackageDetails.objects.latest('id')
        package_id1 = package_details.id

        params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_loose_cargo_set()
        params['transport_mode'] = [7]
        params['pickup_location'] = 16
        params['loose_cargo']['packages'][0]['drop_location'] = 18
        response = client.post(package_details_url, data=json.dumps(
            params), content_type='application/json')

        package_id2 = PackageDetails.objects.latest('id').id

        params = PackageDetailsRequestParams.package_details_fcl_with_dock_stuffing_set()
        params['transport_mode'] = [7]
        params['packages'] = [package_id1, package_id2]

        response = client.post(package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Package details added successfully',
                         api_response['message'])
        self.assertEqual(None, api_response['data'])


    def test_package_details_create_fcl_with_dock_stuffing_package_stackable_required(self):

        params = PackageDetailsRequestParams.package_details_create_fcl_with_dock_stuffing_package_stackable_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)


        self.assertEqual('F4035', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Please select if package is stackable or not.',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_package_details_create_fcl_with_dock_stuffing_package_hazardous_required(self):

        params = PackageDetailsRequestParams.package_details_create_fcl_with_dock_stuffing_package_hazardous_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)


        self.assertEqual('F4036', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Please select if package is hazardous or not.',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_package_details_create_fcl_with_dock_stuffing_package_commodity_required(self):

        params = PackageDetailsRequestParams.package_details_create_fcl_with_dock_stuffing_package_commodity_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)


        self.assertEqual('F4037', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Commodity is required.',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_package_details_create_fcl_with_factory_stuffing_container_stackable_required(self):

        params = PackageDetailsRequestParams.package_details_create_fcl_with_factory_stuffing_container_stackable_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)


        self.assertEqual('F4035', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Please select if package is stackable or not.',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_package_details_create_fcl_with_factory_stuffing_container_hazardous_required(self):

        params = PackageDetailsRequestParams.package_details_create_fcl_with_factory_stuffing_container_hazardous_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)


        self.assertEqual('F4036', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Please select if package is hazardous or not.',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_package_details_create_fcl_with_factory_stuffing_container_commodity_required(self):

        params = PackageDetailsRequestParams.package_details_create_fcl_with_factory_stuffing_container_commodity_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)


        self.assertEqual('F4037', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Commodity is required.',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_package_details_create_fcl_flactrack_container_with_package_details_required(self):

        params = PackageDetailsRequestParams.package_details_create_fcl_flactrack_container_with_package_details_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4028', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Please add package to this container',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_package_details_create_fcl_flactrack_container_only_package_details_required(self):

        params = PackageDetailsRequestParams.package_details_create_fcl_flactrack_container_only_package_details_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4028', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Please add package to this container',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_package_details_create_fcl_reefer_container_temperature_required(self):

        params = PackageDetailsRequestParams.package_details_create_fcl_reefer_container_with_temperature_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4038', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Temperature is required.',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_package_details_create_fcl_reefer_container_temperature_unit_required(self):

        params = PackageDetailsRequestParams.package_details_create_fcl_reefer_container_with_temperature_unit_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4039', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Temperature unit is required.',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_package_details_create_fcl_reefer_container_with_invalid_temperature_unit(self):

        params = PackageDetailsRequestParams.package_details_create_fcl_reefer_container_with_invalid_temperature_unit()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('BEF0001', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('temperature_unit - "DD" is not a valid choice.',
                         api_response['message'])
        self.assertEqual({'temperature_unit': ['"DD" is not a valid choice.']}, api_response['data'])


    def test_package_details_create_fcl_reefer_container_shipper_required(self):

        params = PackageDetailsRequestParams.package_details_create_fcl_reefer_container_with_shipper_required()

        response = client.post(self.package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4040', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Shipper details is required.',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_package_details_create_fcl_container_multi_drop_with_package_details(self):

        params = PackageDetailsRequestParams.quote_valid_set_with_single_pickup_and_multi_drop()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        quote = Quote.objects.latest('id')
        quote_id = quote.id

        package_details_url = PackageDetailsRequestParams.api_url(
        ) + '/api/v1/company/'+str(self.company_id)+'/quote/'+str(quote_id)+'/package_details/'


        params = PackageDetailsRequestParams.package_details_create_fcl_container_multi_drop_with_package_details_required()

        response = client.post(package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4028', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Please add package to this container',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_package_details_create_fcl_multi_drop_only_dock_destuffing_required(self):

        params = PackageDetailsRequestParams.quote_valid_set_with_single_pickup_and_multi_drop()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        quote = Quote.objects.latest('id')
        quote_id = quote.id

        package_details_url = PackageDetailsRequestParams.api_url(
        ) + '/api/v1/company/'+str(self.company_id)+'/quote/'+str(quote_id)+'/package_details/'


        params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_loose_cargo_set2()
        params['transport_mode'] = [6]
        params['pickup_location'] = 13
        params['loose_cargo']['packages'][0]['drop_location'] = 14
        response = client.post(package_details_url, data=json.dumps(
            params), content_type='application/json')

        package_id1 = PackageDetails.objects.latest('id').id

        params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_loose_cargo_set3()
        params['transport_mode'] = [6]
        params['pickup_location'] = 13
        params['loose_cargo']['packages'][0]['drop_location'] = 15
        response = client.post(package_details_url, data=json.dumps(
            params), content_type='application/json')

        package_id2 = PackageDetails.objects.latest('id').id


        params = PackageDetailsRequestParams.package_details_fcl_with_factory_destuffing_set()
        params['transport_mode'] = [6]
        params['packages'] = [package_id1, package_id2]

        response = client.post(package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4032', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('For multiple drop location, only dock stuffing is required.',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_package_details_create_fcl_for_reefer_container_temperature_packages_required(self):

        params = PackageDetailsRequestParams.quote_valid_set_with_single_pickup_and_multi_drop()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        quote = Quote.objects.latest('id')
        quote_id = quote.id

        package_details_url = PackageDetailsRequestParams.api_url(
        ) + '/api/v1/company/'+str(self.company_id)+'/quote/'+str(quote_id)+'/package_details/'

        params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_loose_cargo_set2()
        params['transport_mode'] = [5]
        params['pickup_location'] = 10
        params['loose_cargo']['packages'][0]['temperature'] = 23.45
        params['loose_cargo']['packages'][0]['temperature_unit'] = "C"
        params['loose_cargo']['packages'][0]['shipper_details'] = "Shipper1"
        params['loose_cargo']['packages'][0]['drop_location'] = 11

        response = client.post(package_details_url, data=json.dumps(
            params), content_type='application/json')

        package_id1 = PackageDetails.objects.latest('id').id


        params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_loose_cargo_set3()
        params['transport_mode'] = [5]
        params['pickup_location'] = 10
        params['loose_cargo']['packages'][0]['temperature'] = 33.45
        params['loose_cargo']['packages'][0]['temperature_unit'] = "C"
        params['loose_cargo']['packages'][0]['shipper_details'] = "Shipper2"
        params['loose_cargo']['packages'][0]['drop_location'] = 12

        response = client.post(package_details_url, data=json.dumps(
            params), content_type='application/json')

        package_id2 = PackageDetails.objects.latest('id').id


        params = PackageDetailsRequestParams.package_details_fcl_with_dock_stuffing_set()
        params['packages'] = [package_id1, package_id2]
        params['transport_mode'] = [5]

        response = client.post(package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4042', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Cannot add temperature controlled packages in this type of container',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])


    def test_package_details_create_fcl_for_reefer_container_same_temperature_packages_required_in_same_container(self):

        params = PackageDetailsRequestParams.quote_valid_set_with_single_pickup_and_multi_drop()

        response = client.post(self.quote_api_url, data=json.dumps(
            params), content_type='application/json')

        quote = Quote.objects.latest('id')
        quote_id = quote.id

        package_details_url = PackageDetailsRequestParams.api_url(
        ) + '/api/v1/company/'+str(self.company_id)+'/quote/'+str(quote_id)+'/package_details/'


        params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_loose_cargo_set2()
        params['loose_cargo']['packages'][0]['temperature'] = 23.45
        params['loose_cargo']['packages'][0]['temperature_unit'] = "C"
        params['loose_cargo']['packages'][0]['shipper_details'] = "Shipper1"

        response = client.post(package_details_url, data=json.dumps(
            params), content_type='application/json')

        package_id1 = PackageDetails.objects.latest('id').id


        params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_loose_cargo_set3()
        params['loose_cargo']['packages'][0]['temperature'] = 33.45
        params['loose_cargo']['packages'][0]['temperature_unit'] = "C"
        params['loose_cargo']['packages'][0]['shipper_details'] = "Shipper2"

        response = client.post(package_details_url, data=json.dumps(
            params), content_type='application/json')

        package_id2 = PackageDetails.objects.latest('id').id


        params = PackageDetailsRequestParams.package_details_fcl_with_dock_stuffing_set()
        params['packages'] = [package_id1, package_id2]
        params['transport_mode'] = [4]
        params['container_type'] = "20Reefer"
        params['container_subtype'] = "RF"

        response = client.post(package_details_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F4043', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Same container cannot be used for different temperature packages.',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])
