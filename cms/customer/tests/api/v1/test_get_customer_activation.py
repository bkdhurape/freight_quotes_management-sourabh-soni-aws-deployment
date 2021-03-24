from customer.models.customer import Customer
from customer.tests.api.v1.customer_params import CustomerParams
from rest_framework.test import APITestCase
import json


class TestGetCustomerActivation(APITestCase):

    fixtures = CustomerParams.get_seed_data_list()

    def setUp(self):
        # Customer Registration Start

        customer_registration_api_url = CustomerParams.api_url() + '/api/v1/customer/'
        customer_registration_params = CustomerParams.post_register_required_request_params()

        response = self.client.post(customer_registration_api_url, data=customer_registration_params, format='json')
        self.api_response_json = json.loads(response.content)

        # Customer Registration End

        # Get customer id and company id by customer name
        customer_name = customer_registration_params['customer_details']['name']
        customer = list(Customer.find_by(multi=True, name=customer_name).values_list('id','home_company'))[0]
        self.customer_id, self.customer_company_id = customer


    def test_customer_activaion(self):

        # Actvate customer
        response = self.client.get(self.api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Customer activated successfully.', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])
        self.assertEqual(200, api_response_json['code'])


    def test_customer_already_activated(self):

        # Actvate customer
        response = self.client.get(self.api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        # Activate customer again
        response = self.client.get(self.api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('You are already acivated. Please login to continue', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0107', api_response_json['code'])


    def test_customer_activation_with_invalid_token(self):

        api_url = CustomerParams.api_url() + '/api/v1/company/'+ str(self.customer_company_id) +'/customer/activate/11223'

        # Actvate customer with invalid token url
        response = self.client.get(api_url, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Invalid Token. Please contact admin for your account activation and other queries.', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0108', api_response_json['code'])
