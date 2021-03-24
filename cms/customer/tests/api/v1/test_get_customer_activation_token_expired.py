from customer.tests.api.v1.customer_params import CustomerParams
from customer.models.customer import Customer
from rest_framework.test import APITestCase
import json


class TestGetCustomerActivationTokenExpired(APITestCase):

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


    def test_customer_activaion_with_expired_token(self):

        # Actvate customer
        response = self.client.get(self.api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Your activation link has been expired. Please click here to resend the activation link or Contact admin for any other queries.', api_response_json['message'])
        self.assertEqual(200, api_response_json['code'])


    def test_customer_activaion_with_resend_valid_activation_link(self):
        response = self.client.get(self.api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        response = self.client.get(api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Resend mail sent successfully.', api_response_json['message'])
        self.assertEqual(200, api_response_json['code'])


    def test_customer_activaion_with_valid_activation_link(self):

        response = self.client.get(self.api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        response = self.client.get(api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        response = self.client.get(api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Customer activated successfully.', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])
        self.assertEqual(200, api_response_json['code'])
