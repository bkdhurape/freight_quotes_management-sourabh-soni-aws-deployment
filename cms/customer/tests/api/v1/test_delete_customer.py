from customer.tests.api.v1.customer_params import CustomerParams
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

# initialize the APIClient app
client = APIClient()


class TestDeleteCustomer(TestCase):

    fixtures = CustomerParams.get_seed_data_list()

    @classmethod
    def setUpTestData(cls):
        cls.api_url_host = CustomerParams.api_url()
        cls.register_url = cls.api_url_host + '/api/v1/customer/'
        cls.login_url = cls.api_url_host + '/user/login/'
        cls.add_customer_url = cls.api_url_host + '/api/v1/company/1/customer/'
        cls.create_company_url = cls.api_url_host + '/api/v1/company/'
        cls.delete_customer_url = cls.api_url_host + '/api/v1/company/1/customer/2/'
        
        # Register Customer
        response = client.post(cls.register_url, data=CustomerParams.post_register_required_request_params(), format='json')
        activation_link = response.data['data']
        client.get(activation_link)

        # Customer Login
        response = client.post(cls.login_url, data=CustomerParams.post_login_customer_request_params(), format='json')
        jwt_token = response.data['data'][0]['token']
        client.credentials(HTTP_AUTHORIZATION=jwt_token)

        # Add Customer Company
        request_params = CustomerParams.post_add_customer_company_request_params()
        client.post(cls.create_company_url, data=request_params, format='json')
        request_params['name'] = 'canon_o3cC'
        client.post(cls.create_company_url, data=request_params, format='json')

        # Add a Customer
        request_params = CustomerParams.post_add_customer_request_params()
        response = client.post(cls.add_customer_url, data=request_params, format='json')
        activation_link = response.data['data']
        client.get(activation_link)
        request_params['customer_details']['email'] = 'calvino1u3@g.com'
        response = client.post(cls.add_customer_url, data=request_params, format='json')
        activation_link = response.data['data']
        client.get(activation_link)


    def tearDownTestCase(self):
        self._cleanup_record()


    # Delete a Customer with valid URL
    def test_delete_customer_by_url(self):
        response = client.delete(self.delete_customer_url)
        # print('---test_delete_customer_by_url_api_response---', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(200, response.data['code'])
        self.assertEqual('success', response.data['status'])
        self.assertEqual('Customer removed successfully.', response.data['message'])
        self.assertEqual(None, response.data['data'])


    # Delete a Customer with invalid Company ID
    def test_delete_customer_with_invalid_company_id(self):
        response = client.delete(self.api_url_host + '/api/v1/company/991/customer/3/')
        # print('---test_delete_customer_with_invalid_company_id_api_response---', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(200, response.data['code'])
        self.assertEqual('success', response.data['status'])
        self.assertEqual('Access denied.', response.data['message'])
        self.assertEqual(None, response.data['data'])


    # Delete a Customer with invalid Customer ID
    def test_delete_customer_with_invalid_customer_id(self):
        response = client.delete(self.api_url_host + '/api/v1/company/1/customer/993/')
        # print('---test_delete_customer_with_invalid_customer_id_api_response---', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0101', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('Customer data not found.', response.data['message'])
        self.assertEqual({}, response.data['data'])
