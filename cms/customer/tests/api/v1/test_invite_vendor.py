from customer.models.customer import Customer
from customer.models.invited_vendor import InvitedVendor
from customer.tests.api.v1.customer_params import CustomerParams
from rest_framework.test import APITestCase
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
import json


class TestPostInviteVendor(APITestCase):

    fixtures = CustomerParams.get_seed_data_list()

    def setUp(self):

        # Customer Registration Start

        customer_registration_api_url = CustomerParams.api_url() + '/api/v1/customer/'
        customer_registration_params = CustomerParams.post_register_required_request_params()

        response = self.client.post(customer_registration_api_url, data=customer_registration_params, format='json')
        api_response_json = json.loads(response.content)

        # Customer Registration End

        # Get customer id and company id by customer name
        customer_name = customer_registration_params['customer_details']['name']
        customer = list(Customer.find_by(multi=True, name=customer_name).values_list('id','home_company'))[0]
        self.customer_id, self.customer_company_id = customer

        # Actvate customer
        response = self.client.get(api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        # Login activated customer
        response = self.client.post(CustomerParams.api_url() + '/user/login/', data=CustomerParams.post_login_customer_request_params(), format='json')
        jwt_token = response.data['data'][0]['jwt_token']
        self.client.credentials(HTTP_AUTHORIZATION=jwt_token)


        # Register new vendor
        vendor_post_api_url = CustomerParams.api_url() + '/api/v1/vendor/'
        vendor_register_params = CustomerParams.post_vendor_registration_personal_details_request_set()

        response = self.client.post(vendor_post_api_url, data=vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        # Get company and vendor id by vendor name
        vendor_name = vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(multi=True, name=vendor_name).values_list('id','home_company'))[0]
        vendor_id, company_id = vendor

        # Create send activation link
        encoded_email = encode_data(vendor_register_params['vendor_details']['email'])
        test_vendor_send_activation_link_api_url = CustomerParams.api_url() + '/api/v1/company/'+ str(company_id) +'/vendor/send_activation_link/' + encoded_email

        response = self.client.get(test_vendor_send_activation_link_api_url, format='json')
        final_api_response_json = json.loads(response.content)

        # Activate vendor
        response = self.client.get(final_api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)


    def test_invite_vendor_with_company_and_email_exists(self):
        invite_vendor_params = CustomerParams.post_invite_vendor_request_set()
        invite_vendor_post_api_url = CustomerParams.api_url() + '/api/v1/company/' + str(self.customer_company_id) + '/customer/' + str(self.customer_id) + '/clients'

        response = self.client.post(invite_vendor_post_api_url, data=invite_vendor_params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor invited successfully.', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])
        self.assertEqual(200, api_response_json['code'])


    def test_invite_vendor_with_company_exits_and_email_not_exists(self):
        invite_vendor_params = CustomerParams.post_invite_vendor_request_set()
        invite_vendor_params['email'] = 'abc@gmail.com'
        invite_vendor_post_api_url = CustomerParams.api_url() + '/api/v1/company/' + str(self.customer_company_id) + '/customer/' + str(self.customer_id) + '/clients'

        response = self.client.post(invite_vendor_post_api_url, data=invite_vendor_params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor invited successfully.', api_response_json['message'])
        self.assertEqual(invite_vendor_params, api_response_json['data'])
        self.assertEqual(200, api_response_json['code'])


    def test_invite_vendor_with_company_and_email_both_not_exists(self):
        invite_vendor_params = CustomerParams.post_invite_vendor_request_set()
        invite_vendor_params['email'] = 'abc@gmail.com'
        invite_vendor_params['company_name'] = 'abcd'
        invite_vendor_post_api_url = CustomerParams.api_url() + '/api/v1/company/' + str(self.customer_company_id) + '/customer/' + str(self.customer_id) + '/clients'

        response = self.client.post(invite_vendor_post_api_url, data=invite_vendor_params, format='json')
        api_response_json = json.loads(response.content)

        invited_vendor = InvitedVendor.find_by(multi = True, email = invite_vendor_params['email'], customer_company = self.customer_company_id, customer = self.customer_id, company_name = invite_vendor_params['company_name'])
        invited_vendor_id = list(invited_vendor.values_list('id', flat=True))[0]

        data = str(invited_vendor_id) + '__' + invite_vendor_params['company_name'] + '__' + invite_vendor_params['email']
        token = encode_data(data)
        invited_vendor_register_url = CustomerParams.api_url() + '/api/v1/vendor/' + token

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor invited successfully.', api_response_json['message'])
        self.assertEqual(invited_vendor_register_url, api_response_json['data'])
        self.assertEqual(200, api_response_json['code'])


    def test_invite_same_vendor_from_same_company(self):
        invite_vendor_params = CustomerParams.post_invite_vendor_request_set()
        invite_vendor_post_api_url = CustomerParams.api_url() + '/api/v1/company/' + str(self.customer_company_id) + '/customer/' + str(self.customer_id) + '/clients'

        response = self.client.post(invite_vendor_post_api_url, data=invite_vendor_params, format='json')
        api_response_json = json.loads(response.content)

        response = self.client.post(invite_vendor_post_api_url, data=invite_vendor_params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('non_field_errors - The fields customer_company, email must make a unique set.', api_response_json['message'])
        self.assertEqual({'non_field_errors': ['The fields customer_company, email must make a unique set.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])
