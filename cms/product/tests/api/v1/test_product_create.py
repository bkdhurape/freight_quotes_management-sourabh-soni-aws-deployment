from customer.models.customer import Customer
from customer.tests.api.v1.customer_request_params import CustomerRequestParams
from entity.tests.api.v1.entity_request_params import EntityRequestParams
from product.tests.api.v1.product_request_params import ProductRequestParams
from rest_framework.test import APITestCase
import json


class TestProductCreate(APITestCase):

    fixtures = ProductRequestParams.get_seed_data_list()

    def setUp(self):
        self.customer_post_api_url = CustomerRequestParams.api_url() + '/api/v1/customer/'
        self.customer_register_params = CustomerRequestParams.post_customer_registration_personal_details_request_set()
        self.params = CustomerRequestParams.post_add_customer_valid_request_set()

        response = self.client.post(self.customer_post_api_url, data=self.customer_register_params, format='json')
        api_response_json = json.loads(response.content)

        customer_name = self.customer_register_params['customer_details']['name']
        customer = list(Customer.find_by(multi=True, name=customer_name).values_list('id','home_company'))[0]
        self.customer_id, self.company_id = customer

        self.customer_add_post_api_url = CustomerRequestParams.api_url() + '/api/v1/company/'+ str(self.company_id) +'/customer/'
        response = self.client.get(api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        response = self.client.post(CustomerRequestParams.api_url() + '/user/login/', data=ProductRequestParams.login_valid_request_params(), format='json')
        api_response_json = json.loads(response.content)

        entity_api_url = CustomerRequestParams.api_url() + '/api/v1/company/'+ str(self.company_id) +'/entity/'

        params = EntityRequestParams.post_entity_request_set()
        response = self.client.post(entity_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        response = self.client.get(entity_api_url, format='json')
        api_response_json = json.loads(response.content)
        entity_data = api_response_json['data'][0]

        self.api_url = ProductRequestParams.api_url() + '/api/v1/entity/'+ str(entity_data['id']) +'/product/'
        self.invalid_api_url = ProductRequestParams.api_url() + '/api/v1/entity/999999999999/product/'


    def test_product_create(self):
        # Add product
        params = ProductRequestParams.post_product_request_set()
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Product added successfully.', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])


    def test_product_create_with_same_product_name(self):
        # Add same product name in same entity
        params = ProductRequestParams.post_product_request_set()
        response = self.client.post(self.api_url, data=params, format='json')

        params = ProductRequestParams.post_product_request_set()
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('non_field_errors - The fields entity, name must make a unique set.', api_response_json['message'])
        self.assertEqual({'non_field_errors': ['The fields entity, name must make a unique set.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])


    def test_product_create_product_with_invalid_entity_id(self):
        # Add product
        params = ProductRequestParams.post_product_request_set()
        response = self.client.post(self.invalid_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Entity data not found.', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F02001', api_response_json['code'])


    def test_product_create_blank_name(self):

        # Add product
        params = ProductRequestParams.post_product_request_set()
        params['name'] = ""
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('name - This field may not be blank.', api_response_json['message'])
        self.assertEqual({'name': ['This field may not be blank.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])


    def test_product_create_product_transport_mode_air_without_airports(self):
        # Add product
        params = ProductRequestParams.post_product_request_set()
        params['transport_modes'] = ['Air']
        params['airports'] = []
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Product airport required.', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F02016', api_response_json['code'])

    def test_product_create_product_transport_mode_fcl_lcl_without_seaports(self):
        # Add product
        params = ProductRequestParams.post_product_request_set()
        params['transport_modes'] = ['LCL']
        params['seaports'] = []
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Product seaport required.', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F02017', api_response_json['code'])


    def test_product_create_product_invalid_seaport_id(self):
        # Add product
        params = ProductRequestParams.post_product_request_set()
        params['transport_modes'] = ['LCL']
        params['seaports'] = [99999999999]
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Invalid seaport id', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F02018', api_response_json['code'])

    def test_product_create_product_invalid_airport_id(self):
        # Add product
        params = ProductRequestParams.post_product_request_set()
        params['transport_modes'] = ['Air']
        params['airports'] = [99999999999]
        response = self.client.post(self.api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Invalid airport id', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F02019', api_response_json['code'])
