from customer.tests.api.v1.customer_params import CustomerParams
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

# initialize the APIClient app
client = APIClient()


class TestPostAddCustomer(TestCase):

    fixtures = CustomerParams.get_seed_data_list()

    @classmethod
    def setUpTestData(cls):
        cls.api_url_host = CustomerParams.api_url()
        cls.register_url = cls.api_url_host + '/api/v1/customer/'
        cls.login_url = cls.api_url_host + '/user/login/'
        cls.add_customer_url = cls.api_url_host + '/api/v1/company/1/customer/'
        cls.create_company_url = cls.api_url_host + '/api/v1/company/'
        
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


    def tearDownTestCase(self):
        self._cleanup_record()


    # Add a Customer with valid params set
    def test_add_customer_required_params(self):
        response = client.post(self.add_customer_url, data=CustomerParams.post_add_customer_request_params(), format='json')
        # print('---test_add_customer_required_params_api_response---', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(200, response.data['code'])
        self.assertEqual('success', response.data['status'])
        self.assertEqual('Customer added successfully.', response.data['message'])


    # Add a Customer with invalid email params set
    def test_add_customer_invalid_email_params(self):
        request_params = CustomerParams.post_add_customer_request_params()
        request_params['customer_details']['email'] = 'calvino1u3@com'
        response = client.post(self.add_customer_url, data=request_params, format='json')
        # print('---test_add_customer_invalid_email_params_api_response---', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('BEF0001', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('email - Enter a valid email address.', response.data['message'])
        self.assertEqual({'email': ['Enter a valid email address.']}, response.data['data'])


    # Add a Customer with invalid home company params set
    def test_add_customer_invalid_home_company_params(self):
        request_params = CustomerParams.post_add_customer_request_params()
        request_params['customer_details']['home_company'] = 99
        response = client.post(self.add_customer_url, data=request_params, format='json')
        # print('---test_add_customer_invalid_home_company_params_api_response---', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0117', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('For this customer company does not exist.', response.data['message'])
        self.assertEqual({}, response.data['data'])


    # Add a Customer with invalid companies currency params set
    def test_add_customer_invalid_companies_currency_params(self):
        request_params = CustomerParams.post_add_customer_request_params()
        request_params['user_companies_currency'][2]['3']['lcl_currency'] = None
        response = client.post(self.add_customer_url, data=request_params, format='json')
        # print('---test_add_customer_invalid_companies_currency_params_api_response---', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0145', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('Companies currency is required.', response.data['message'])
        self.assertEqual({}, response.data['data'])


    # Add a Customer with empty departments params set
    def test_add_customer_empty_department_params(self):
        request_params = CustomerParams.post_add_customer_request_params()
        request_params['customer_details']['department'] = []
        response = client.post(self.add_customer_url, data=request_params, format='json')
        # print('---test_add_customer_empty_department_params_api_response---', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('BEF0001', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('department - This list may not be empty.', response.data['message'])
        self.assertEqual({'department': ['This list may not be empty.']}, response.data['data'])


    # Add a Customer with invalid departments params set
    def test_add_customer_invalid_department_params(self):
        request_params = CustomerParams.post_add_customer_request_params()
        request_params['customer_details']['department'] = [99]
        response = client.post(self.add_customer_url, data=request_params, format='json')
        # print('---test_add_customer_invalid_department_params_api_response---', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0106', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('For this company department does not exist.', response.data['message'])
        self.assertEqual({}, response.data['data'])