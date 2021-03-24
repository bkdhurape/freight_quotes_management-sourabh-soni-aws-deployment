from customer.models.customer import Customer
from customer.tests.api.v1.customer_request_params import CustomerRequestParams
from entity.tests.api.v1.entity_request_params import EntityRequestParams
from product.tests.api.v1.product_request_params import ProductRequestParams
from rest_framework.test import APITestCase
import json


class TestProductGetAll(APITestCase):

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
        entity_id = entity_data['id']

        self.api_url = ProductRequestParams.api_url() + '/api/v1/entity/'+ str(entity_id) +'/product/'
        self.invalid_api_url = ProductRequestParams.api_url() + '/api/v1/entity/999999999999/product/'


        # Add Product
        params = ProductRequestParams.post_product_request_set()
        self.client.post(self.api_url, data=params, format='json')

        # Add Other Product
        params = ProductRequestParams.post_product_request_set2()
        self.client.post(self.api_url, data=params, format='json')


    def test_product_get_all(self):
        response = self.client.get(self.api_url, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Product data retrieved successfully.', api_response_json['message'])
        self.maxDiff = None
        self.assertEqual(ProductRequestParams.get_list_of_product_params_set(), api_response_json['data'])


    def test_product_get_all_with_invalid_entity_id(self):
        # Add product
        response = self.client.get(self.invalid_api_url, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Entity data not found.', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F02001', api_response_json['code'])
