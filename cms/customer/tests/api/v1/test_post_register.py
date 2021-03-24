from customer.tests.api.v1.customer_params import CustomerParams
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

# initialize the APIClient app
client = APIClient()


class TestPostRegister(TestCase):

    fixtures = CustomerParams.get_seed_data_list()

    @classmethod
    def setUpTestData(cls):
        cls.api_url_host = CustomerParams.api_url()
        cls.register_url = cls.api_url_host + '/api/v1/customer/'

    def tearDownTestCase(self):
        self._cleanup_record()

    # Customer Register with Required valid params set

    def test_register_required_params(self):
        response = client.post(
            self.register_url, data=CustomerParams.post_register_required_request_params(), format='json')
        # print('---test_register_required_params_api_response---', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(200, response.data['code'])
        self.assertEqual('success', response.data['status'])
        self.assertEqual('Customer added successfully.',
                         response.data['message'])

    # Customer Register with valid params set

    def test_register_params(self):
        response = client.post(
            self.register_url, data=CustomerParams.post_register_required_request_params(), format='json')
        # print('---test_register_params---', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(200, response.data['code'])
        self.assertEqual('success', response.data['status'])
        self.assertEqual('Customer added successfully.',
                         response.data['message'])

    # Customer Register with Duplicate valid params set

    def test_register_duplicate_params(self):
        client.post(self.register_url,
                    data=CustomerParams.post_register_required_request_params(), format='json')
        response = client.post(
            self.register_url, data=CustomerParams.post_register_required_request_params(), format='json')
        # print('---test_register_duplicate_params_api_response---', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0105', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual(
            'Company already exists. Please contact your admin to register.', response.data['message'])
        self.assertEqual({}, response.data['data'])

    # Customer Register with Diffrent Customer Email but Same Company Name params set

    def test_register_diffrent_customer_email_same_company_params(self):
        request_params = CustomerParams.post_register_required_request_params()
        client.post(self.register_url, data=request_params, format='json')
        request_params['customer_details']['email'] = 'calvino2u1@g.com'
        response = client.post(
            self.register_url, data=request_params, format='json')
        # print('---test_register_diffrent_customer_email_same_company_params_api_response---', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0105', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual(
            'Company already exists. Please contact your admin to register.', response.data['message'])
        self.assertEqual({}, response.data['data'])

    # customer register with invalid customer type choice

    def test_register_invalid_customer_type_choice(self):
        request_params = CustomerParams.post_register_required_request_params()
        client.post(self.register_url, data=request_params, format='json')
        request_params['customer_details']['email'] = 'calvino2u11@g.com'
        request_params['customer_details']['company_name'] = 'fct_demo'
        request_params['customer_details']['customer_type'] = 'Importer_exprter'

        response = client.post(
            self.register_url, data=request_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('BEF0001', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual(
            'customer_type - "Importer_exprter" is not a valid choice.', response.data['message'])
        self.assertEqual({"customer_type": [
                         "\"Importer_exprter\" is not a valid choice."]}, response.data['data'])

    # Customer Register with null customer email & company name params set

    def test_register_with_null_email_company_name_params(self):
        request_params = CustomerParams.post_register_required_request_params()
        request_params['customer_details']['email'] = None
        request_params['customer_details']['company_name'] = None
        response = client.post(
            self.register_url, data=request_params, format='json')
        # print('---test_register_with_null_email_company_name_params_api_response---', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('BEF0001', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('name - This field may not be null.',
                         response.data['message'])
        self.assertEqual(
            {'name': ['This field may not be null.']}, response.data['data'])

    # customer_register_with_customer_type_is_other_then_customer_type_other_is_required

    def test_register_with_customer_type_is_other_then_customer_type_other_is_required(self):
        request_params = CustomerParams.post_register_required_request_params()
        request_params['customer_details']['email'] = 'calvino2u1q1@g.com'
        request_params['customer_details']['company_name'] = 'fct_demo1'
        request_params['customer_details']['customer_type'] = 'other'
        response = client.post(self.register_url, data=request_params, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0119', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('Customer Type other is required.',response.data['message'])
        self.assertEqual({}, response.data['data'])

    # customer_register_with_null_customer_type
    
    def test_register_with_null_customer_type(self):
        request_params = CustomerParams.post_register_required_request_params()
        request_params['customer_details']['email'] = 'calvino2u1q11@g.com'
        request_params['customer_details']['company_name'] = 'fct_demo2'
        request_params['customer_details']['customer_type'] = None
        response = client.post(self.register_url, data=request_params, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0120', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('Customer Type is required.',response.data['message'])
        self.assertEqual({}, response.data['data'])

