from customer.tests.api.v1.customer_request_params import CustomerRequestParams
from rest_framework import status
from rest_framework.test import APITestCase
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json


class TestVendorAddUser(APITestCase):

    fixtures = VendorRequestParams.get_seed_data_list()

    def setUp(self):
        self.vendor_post_api_url = VendorRequestParams.api_url() + '/api/v1/vendor/'
        self.vendor_register_params = VendorRequestParams.post_vendor_registration_personal_details_request_set()
        self.params = VendorRequestParams.post_add_vendor_valid_request_set()

        response = self.client.post(self.vendor_post_api_url, data=self.vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        vendor_name = self.vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(multi=True, name=vendor_name).values_list('id','home_company'))[0]
        self.vendor_id, self.company_id = vendor

        encoded_email = encode_data(self.vendor_register_params['vendor_details']['email'])
        test_vendor_send_activation_link_api_url = VendorRequestParams.api_url() + '/api/v1/company/'+ str(self.company_id) +'/vendor/send_activation_link/' + encoded_email

        response = self.client.get(test_vendor_send_activation_link_api_url, format='json')
        self.final_api_response_json = json.loads(response.content)
        self.vendor_add_post_api_url = VendorRequestParams.api_url() + '/api/v1/company/'+ str(self.company_id) +'/vendor/'

        response = self.client.get(self.final_api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        response = self.client.post(VendorRequestParams.api_url() + '/user/login/', data=VendorRequestParams.login_valid_request_params(), format='json')
        api_response_json = json.loads(response.content)

        # Add Company 2nd in Organization
        response = self.client.post(VendorRequestParams.api_url()+ '/api/v1/company/',
            data=json.dumps(CustomerRequestParams.add_company_valid_request_params()), content_type='application/json')
        api_response = json.loads(response.content)

        # Add Company 3rd in Organization
        request_params = CustomerRequestParams.add_company_valid_request_params()
        request_params['name'] = 'company_o1cC'
        response = self.client.post(VendorRequestParams.api_url() + '/api/v1/company/',
            data=json.dumps(request_params), content_type='application/json')
        api_response = json.loads(response.content)


    # Test vendor contact no. feature
    def check_invalid_contact_no(self):
        request_params = VendorRequestParams.post_add_vendor_valid_request_set()
        request_params['vendor_details']['contact_no'][1]['dial_code'] = '1243'
        response = self.client.post(self.vendor_add_post_api_url,
            data=json.dumps(request_params), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Invalid contact no.', api_response['message'])
        self.assertEqual('BF0003', api_response['code'])


    # Test vendor branch feature
    def check_invalid_branch(self):
        request_params = VendorRequestParams.post_add_vendor_valid_request_set()
        request_params['vendor_details']['branch'] = [99]
        response = self.client.post(self.vendor_add_post_api_url,
            data=json.dumps(request_params), content_type='application/json')
        api_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('The selected branch does not belong to this company.', api_response['message'])
        self.assertEqual('F0910', api_response['code'])
        self.assertEqual({}, api_response['data'])

    # Test vendor home company feature
    def check_invalid_home_company(self):
        request_params = VendorRequestParams.post_add_vendor_valid_request_set()
        request_params['vendor_details']['home_company'] = [99]
        response = self.client.post(self.vendor_add_post_api_url,
            data=json.dumps(request_params), content_type='application/json')
        api_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Company not found', api_response['message'])
        self.assertEqual('F0001', api_response['code'])
        self.assertEqual({}, api_response['data'])

    # Test vendor companies currency & mode feature
    def check_invalid_compnies_currency_and_mode(self):
        # Test Vendor Companies Currency with Valid Request Params
        response = self.client.post(self.vendor_add_post_api_url,
            data=json.dumps(VendorRequestParams.post_add_vendor_valid_request_set()), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual('success', api_response['status'])
        self.assertEqual('Vendor added successfully.', api_response['message'])
        self.assertEqual(200, api_response['code'])
        self.assertEqual(None, api_response['data'])

        # Test Vendor Companies Currency with Invalid Company ID
        request_params = VendorRequestParams.post_add_vendor_valid_request_set()
        request_params['user_companies_currency'].append({"99": {"air_currency": "JPY","lcl_currency": "EUR","fcl_currency": "EUR"}})
        response = self.client.post(self.vendor_add_post_api_url,
            data=json.dumps(request_params), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Company not found', api_response['message'])
        self.assertEqual('F0001', api_response['code'])

        # Test Vendor Companies Currency with Blank Currency details
        request_params = VendorRequestParams.post_add_vendor_valid_request_set()
        request_params['user_companies_currency'][2]['3']['lcl_currency'] = None
        response = self.client.post(self.vendor_add_post_api_url,
            data=json.dumps(request_params), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Companies currency is required.', api_response['message'])
        self.assertEqual('F0145', api_response['code'])

        # Test Vendor Mode with invalid mode value
        request_params = VendorRequestParams.post_add_vendor_valid_request_set()
        request_params['companies_mode'][1]['2'] = ['ATC', 'FCLE_XYZ', 'LCLE', 'LCLI']
        response = self.client.post(self.vendor_add_post_api_url,
            data=json.dumps(request_params), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Vendor expertise transport mode is invalid.', api_response['message'])
        self.assertEqual('F0914', api_response['code'])


    def test_add_a_vendor(self):
        self.check_invalid_contact_no()
        self.check_invalid_branch()
        self.check_invalid_home_company()
        self.check_invalid_compnies_currency_and_mode()
