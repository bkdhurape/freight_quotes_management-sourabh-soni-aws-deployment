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


class TestPutChangePassword(TestCase):

    fixtures = CustomerParams.get_seed_data_list()

    @classmethod
    def setUpTestData(cls):
        cls.api_url_host = CustomerParams.api_url()
        cls.customer_register_url = cls.api_url_host + '/api/v1/customer/'
        cls.vendor_register_url = cls.api_url_host + '/api/v1/vendor/'
        cls.login_url = cls.api_url_host + '/user/login/'
        cls.change_password_url = cls.api_url_host + '/user/change-password/'
                
        # Register Customer
        response = client.post(cls.customer_register_url, data=CustomerParams.post_register_required_request_params(), format='json')
        activation_link = response.data['data']
        client.get(activation_link)

        # Customer Login
        response = client.post(cls.login_url, data=CustomerParams.post_login_customer_request_params(), format='json')
        jwt_token = response.data['data'][0]['token']
        client.credentials(HTTP_AUTHORIZATION=jwt_token)

        cls.request_params = RequestResponseParams.put_change_password_customer_request_params()


    def tearDownTestCase(self):
        self._cleanup_record()


    # Change password Customer with valid params set
    def test_change_password_required_params(self):
        response = client.put(self.change_password_url, data=self.request_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(200, response.data['code'])
        self.assertEqual('success', response.data['status'])
        self.assertEqual('Your password changed successfully.', response.data['message'])
        self.assertEqual(None, response.data['data'])


    # Change password Customer with invalid params set
    def test_change_password_invalid_params(self):
        request_params = copy.deepcopy(self.request_params)
        request_params['old_password'] = ''
        request_params['new_password'] = None
        response = client.put(self.change_password_url, data=request_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0507', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('Old or new password required.', response.data['message'])
        self.assertEqual({}, response.data['data'])


    # Change password Customer with invalid old_password params set
    def test_change_password_invalid_old_params(self):
        request_params = copy.deepcopy(self.request_params)
        request_params['old_password'] = 'apple'
        response = client.put(self.change_password_url, data=request_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0508', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('You entered old password is invalid.', response.data['message'])
        self.assertEqual({}, response.data['data'])


    # Change password Vendor with valid params set
    def test_change_password_vendor_required_params(self):
        # Register Vendor
        vendor_register_params = VendorRequestParams.post_vendor_registration_personal_details_request_set()
        response = client.post(self.vendor_register_url, data=vendor_register_params, format='json')

        # Get Activation link
        vendor_name = vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(multi=True, name=vendor_name).values_list('id','home_company'))[0]
        self.vendor_id, self.company_id = vendor
        self.vendor_register_params = vendor_register_params
        encoded_email = encode_data(vendor_register_params['vendor_details']['email'])
        self.test_vendor_send_activation_link_api_url = VendorRequestParams.api_url() + '/api/v1/company/'+ str(self.company_id) +'/vendor/send_activation_link/' + encoded_email
        response = client.get(self.test_vendor_send_activation_link_api_url, format='json')
        activation_link = response.data['data']
        
        # Activate Vendor
        client.get(activation_link)

        # Vendor Login
        response = client.post(self.login_url, data=VendorRequestParams.login_valid_request_params(), format='json')
        jwt_token = response.data['data'][0]['token']
        client.credentials(HTTP_AUTHORIZATION=jwt_token)

        # Test Change Password feature
        self.vendor_request_params = RequestResponseParams.put_change_password_vendor_request_params()
        response = client.put(self.change_password_url, data=self.vendor_request_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(200, response.data['code'])
        self.assertEqual('success', response.data['status'])
        self.assertEqual('Your password changed successfully.', response.data['message'])
        self.assertEqual(None, response.data['data'])

        # Change password Vendor with invalid params set
        request_params = copy.deepcopy(self.vendor_request_params)
        request_params['old_password'] = ''
        request_params['new_password'] = None
        response = client.put(self.change_password_url, data=request_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0507', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('Old or new password required.', response.data['message'])
        self.assertEqual({}, response.data['data'])

        # Change password Vendor with invalid old_password params set
        request_params = copy.deepcopy(self.vendor_request_params)
        request_params['old_password'] = 'applefruit'
        response = client.put(self.change_password_url, data=request_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('F0508', response.data['code'])
        self.assertEqual('failure', response.data['status'])
        self.assertEqual('You entered old password is invalid.', response.data['message'])
        self.assertEqual({}, response.data['data'])
