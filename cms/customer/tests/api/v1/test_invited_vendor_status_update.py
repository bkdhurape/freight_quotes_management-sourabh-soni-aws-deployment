from customer.models.customer import Customer
from customer.models.invited_vendor import InvitedVendor
from customer.tests.api.v1.customer_params import CustomerParams
from rest_framework.test import APITestCase
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json


class TestInvitedVendorStatusUpdate(APITestCase):

    fixtures = CustomerParams.get_seed_data_list()

    def setUp(self):

        # Customer Registration Start

        customer_registration_api_url = CustomerParams.api_url() + '/api/v1/customer/'
        customer_registration_params = CustomerParams.post_register_required_request_params()
        invite_vendor_params = CustomerParams.post_invite_vendor_request_set()

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

        vendor_register_params['vendor_details']['email'] = invite_vendor_params['email']
        vendor_register_params['vendor_details']['company_name'] = invite_vendor_params['company_name']
        response = self.client.post(vendor_post_api_url, data=vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        # Get company and vendor id by vendor name
        vendor_name = vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(multi=True, name=vendor_name).values_list('id','home_company'))[0]
        self.vendor_id, self.company_id = vendor

        # Create send activation link
        encoded_email = encode_data(vendor_register_params['vendor_details']['email'])
        test_vendor_send_activation_link_api_url = CustomerParams.api_url() + '/api/v1/company/'+ str(self.company_id) +'/vendor/send_activation_link/' + encoded_email

        response = self.client.get(test_vendor_send_activation_link_api_url, format='json')
        final_api_response_json = json.loads(response.content)

        # Activate vendor
        response = self.client.get(final_api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)


        self.invite_vendor_post_api_url = CustomerParams.api_url() + '/api/v1/company/' + str(self.customer_company_id) + '/customer/' + str(self.customer_id) + '/clients'

        response = self.client.post(self.invite_vendor_post_api_url, data=invite_vendor_params, format='json')
        api_response_json = json.loads(response.content)

        email = invite_vendor_params['email']
        self.invited_vendor_id = list(InvitedVendor.find_by(multi=True, email=email).values_list('id', flat=True))[0]



    def test_invited_vendor_accept_status_update(self):
        invite_vendor_update_api_url = CustomerParams.api_url() + '/api/v1/company/' + str(self.company_id) + '/vendor/' + str(self.vendor_id) + '/clients/' + str(self.invited_vendor_id) + '/accept'
        response = self.client.put(invite_vendor_update_api_url, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor client  updated successfully.', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])
        self.assertEqual(200, api_response_json['code'])


    def test_invited_vendor_only_admin_status_update(self):
        vendor_add_api_url = VendorRequestParams.api_url() + '/api/v1/company/' + str(self.company_id) + '/vendor/'

        request_params = VendorRequestParams.post_add_vendor_valid_request_set()
        request_params['vendor_details']['company'] = [self.company_id]

        request_params['user_companies_currency'][0][self.company_id] =  request_params['user_companies_currency'][0]["1"]
        del request_params['user_companies_currency'][0]["1"]

        request_params['companies_mode'][0][self.company_id] =  request_params['companies_mode'][0]["1"]
        del request_params['companies_mode'][0]["1"]

        request_params['vendor_details']['home_company'] = self.company_id
        request_params['vendor_details']['branch'] = [3]
        request_params['vendor_details']['supervisor'] = [self.vendor_id]

        response = self.client.post(vendor_add_api_url,
            data=json.dumps(request_params), content_type='application/json')
        api_response_json = json.loads(response.content)

        vendor_name = request_params['vendor_details']['name']
        vendor = list(Vendor.find_by(multi=True, name=vendor_name).values_list('id','home_company'))[0]
        vendor_id, company_id = vendor

        invite_vendor_update_api_url = CustomerParams.api_url() + '/api/v1/company/' + str(self.company_id) + '/vendor/' + str(vendor_id) + '/clients/' + str(self.invited_vendor_id) + '/accept'
        response = self.client.put(invite_vendor_update_api_url, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('You cannot ACCEPT or REJECT this client.', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0188', api_response_json['code'])


    def test_invited_vendor_reject_status_update(self):
        invite_vendor_update_api_url = CustomerParams.api_url() + '/api/v1/company/' + str(self.company_id) + '/vendor/' + str(self.vendor_id) + '/clients/' + str(self.invited_vendor_id) + '/reject'
        response = self.client.put(invite_vendor_update_api_url, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor client  updated successfully.', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])
        self.assertEqual(200, api_response_json['code'])


    def test_invited_vendor_invalid_status_update(self):
        invite_vendor_update_api_url = CustomerParams.api_url() + '/api/v1/company/' + str(self.company_id) + '/vendor/' + str(self.vendor_id) + '/clients/' + str(self.invited_vendor_id) + '/invalid123'
        response = self.client.put(invite_vendor_update_api_url, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('You can either ACCEPT or REJECT client', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0186', api_response_json['code'])
