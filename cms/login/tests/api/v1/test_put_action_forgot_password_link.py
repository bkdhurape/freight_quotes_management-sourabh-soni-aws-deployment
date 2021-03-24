from customer.tests.api.v1.customer_params import CustomerParams
from django.test import TestCase
from login.tests.api.v1.request_response_params import RequestResponseParams
from rest_framework import status
from rest_framework.test import APIClient
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import copy, json

# initialize the APIClient app
client = APIClient()


class TestPutActionForgotPasswordLink(TestCase):

    fixtures = CustomerParams.get_seed_data_list()

    @classmethod
    def setUpTestData(cls):
        cls.api_url_host = CustomerParams.api_url()
        cls.customer_register_url = cls.api_url_host + '/api/v1/customer/'
        cls.vendor_register_url = cls.api_url_host + '/api/v1/vendor/'
        cls.login_url = cls.api_url_host + '/user/login/'
        cls.forgot_password_url = cls.api_url_host + '/user/forgot-password/'
                
        # Register Customer
        response = client.post(cls.customer_register_url, data=CustomerParams.post_register_required_request_params(), format='json')
        activation_link = response.data['data']
        client.get(activation_link)

        # Get Customer Forgot Password Token
        customer_request_params = RequestResponseParams.put_create_forgot_password_customer_request_params()
        response = client.put(cls.forgot_password_url, data=customer_request_params, format='json')
        cls.customer_forgot_password_link = json.loads(response.content)['data']['forgot_password_link']

        cls.request_params = RequestResponseParams.put_action_forgot_password_request_params()


        # Register Vendor
        vendor_register_params = VendorRequestParams.post_vendor_registration_personal_details_request_set()
        response = client.post(cls.vendor_register_url, data=vendor_register_params, format='json')

        # Get Activation link
        vendor_name = vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(multi=True, name=vendor_name).values_list('id','home_company'))[0]
        cls.vendor_id, cls.company_id = vendor
        cls.vendor_register_params = vendor_register_params
        encoded_email = encode_data(vendor_register_params['vendor_details']['email'])
        cls.test_vendor_send_activation_link_api_url = VendorRequestParams.api_url() + '/api/v1/company/'+ str(cls.company_id) +'/vendor/send_activation_link/' + encoded_email
        response = client.get(cls.test_vendor_send_activation_link_api_url, format='json')
        activation_link = response.data['data']
        
        # Activate Vendor
        client.get(activation_link)

        # Get Vendor Forgot Password Token
        vendor_request_params = RequestResponseParams.put_create_forgot_password_vendor_request_params()
        response = client.put(cls.forgot_password_url, data=vendor_request_params, format='json')
        cls.vendor_forgot_password_link = json.loads(response.content)['data']['forgot_password_link']


    def tearDownTestCase(self):
        self._cleanup_record()


    # Action on forgot password link for Customer with valid params set
    def test_action_forgot_password_link_customer_required_params(self):
        response = client.put(self.customer_forgot_password_link , data=self.request_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(200, response.data['code'])
        self.assertEqual('success', response.data['status'])
        self.assertEqual('Your password updated successfully.', response.data['message'])
        self.assertEqual(None, response.data['data'])


    # Action on forgot password link with invalid token params
    def test_action_forgot_password_link_invalid_token_params(self):
        request_params = copy.deepcopy(self.request_params)
        response = client.put(self.forgot_password_url + 'Y2FsdmlubzIzdTE1QGcuY29tX19jdXN0b21lcl9fYjBlZjg5MTAtYmJhOS00NjMzLTlhMWQtNjY1MWM5ZjY3YzE4_2b', data=request_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0108', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('Invalid Token. Please contact admin for your account activation and other queries.', response.data['message'])
        self.assertEqual({}, response.data['data'])


    # Action on forgot password link with invalid params
    def test_action_forgot_password_link_invalid_params(self):
        request_params = copy.deepcopy(self.request_params)
        request_params['new_password'] = ""
        response = client.put(self.customer_forgot_password_link, data=request_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0514', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('Entered password can\'t be null or empty.', response.data['message'])
        self.assertEqual({}, response.data['data'])
    

    # Action on forgot password link for Vendor with valid params set
    def test_action_forgot_password_link_vendor_required_params(self):
        response = client.put(self.vendor_forgot_password_link, data=self.request_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(200, response.data['code'])
        self.assertEqual('success', response.data['status'])
        self.assertEqual('Your password updated successfully.', response.data['message'])

        response = client.put(self.vendor_forgot_password_link, data=self.request_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0513', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('Invalid forgot password link.', response.data['message'])
        self.assertEqual({}, response.data['data'])
