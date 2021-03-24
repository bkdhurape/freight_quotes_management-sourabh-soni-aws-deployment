from customer.models.customer import Customer
from customer.tests.api.v1.customer_params import CustomerParams
from rest_framework.test import APITestCase
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
import json


class TestCustomerVendorGetAll(APITestCase):

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

        # Add Invited Vendor
        invite_vendor_params = CustomerParams.post_invite_vendor_request_set()
        self.invite_vendor_get_api_url = CustomerParams.api_url() + '/api/v1/company/' + str(self.customer_company_id) + '/customer/' + str(self.customer_id) + '/clients'

        response = self.client.post(self.invite_vendor_get_api_url, data=invite_vendor_params, format='json')


    def test_invited_vendor_get_all(self):
        response = self.client.get(self.invite_vendor_get_api_url, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Invited Vendor Data retrieved successfully.', api_response_json['message'])
        self.assertEqual(CustomerParams.get_invite_vendor_list_request_set(), api_response_json['data'])
        self.assertEqual(200, api_response_json['code'])


    def test_invited_vendor_get_all_with_invalid_company_id(self):
        invite_vendor_get_invalid_api_url = CustomerParams.api_url() + '/api/v1/company/999999999999/customer/' + str(self.customer_id) + '/clients'
        response = self.client.get(invite_vendor_get_invalid_api_url, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Company not found', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0001', api_response_json['code'])


    def test_invited_vendor_get_all_with_invalid_customer_id(self):
        invite_vendor_get_invalid_api_url = CustomerParams.api_url() + '/api/v1/company/' + str(self.customer_company_id) + '/customer/9999999999999/clients'
        response = self.client.get(invite_vendor_get_invalid_api_url, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Customer data not found.', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0101', api_response_json['code'])
