from customer.tests.api.v1.customer_request_params import CustomerRequestParams
from company.models.company import Company
from rest_framework import status
from rest_framework.test import APITestCase
from vendor.models.vendor import Vendor
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json


class TestVendorUpdateByCompanyAndVendorId(APITestCase):

    fixtures = VendorRequestParams.get_seed_data_list()

    def setUp(self):
        vendor_post_api_url = VendorRequestParams.api_url() + '/api/v1/vendor/'

        # Vendor register
        vendor_register_params = VendorRequestParams.post_vendor_registration_personal_details_request_set()
        vendor_register_params['vendor_details']['status'] = 1
        response = self.client.post(vendor_post_api_url, data=vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        vendor_name = vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(multi=True, name=vendor_name).values_list('id','home_company'))[0]
        self.vendor_id, self.company_id = vendor
        self.vendor_register_params = vendor_register_params
        self.vendor_update_api_url = VendorRequestParams.api_url() + '/api/v1/company/' + str(self.company_id) + '/vendor/' + str(self.vendor_id) + '/'

        response = self.client.post(VendorRequestParams.api_url() + '/user/login/', data=VendorRequestParams.login_valid_request_params(), format='json')

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

    def test_vendor_update(self):
        self.vendor_update_by_company_and_vendor_id()
        self.vendor_update_with_invalid_details()
        self.vendor_update_with_invalid_contact_no()
        self.vendor_update_with_companies_currency_and_mode()

    def vendor_update_by_company_and_vendor_id(self):
        params = VendorRequestParams.put_update_vendor_valid_request_set()
        response = self.client.put(self.vendor_update_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Vendor updated successfully.', api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])


    def vendor_update_with_invalid_details(self):
        params = VendorRequestParams.put_update_vendor_valid_request_set()
        params['vendor_details']['email'] = 'shiv1bgcom'
        response = self.client.put(self.vendor_update_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('email - Enter a valid email address.', api_response_json['message'])
        self.assertEqual({'email': ['Enter a valid email address.']}, api_response_json['data'])
        self.assertEqual('BEF0001', api_response_json['code'])

    def vendor_update_with_invalid_contact_no(self):
        params = VendorRequestParams.put_update_vendor_valid_request_set()
        params = VendorRequestParams.post_register_vendor_invalid_contact_detail_set(params)
        response = self.client.put(self.vendor_update_api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('Invalid contact no.', api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('BF0003', api_response_json['code'])

    def vendor_update_with_companies_currency_and_mode(self):
        # Add a Vendor with Valid Request Params
        response = self.client.post(VendorRequestParams.api_url() + '/api/v1/company/1/vendor/',
            data=json.dumps(VendorRequestParams.post_add_a_vendor_valid_params_set()), content_type='application/json')
        api_response = json.loads(response.content)

        vendor_params = VendorRequestParams.post_add_a_vendor_valid_params_set()
        vendor_email = vendor_params['vendor_details']['email']
        Vendor.find_by(multi=True, email=vendor_email).update(status=1)

        # Update Vendor Companies Currency with Valid Request Params
        response = self.client.put(VendorRequestParams.api_url() + '/api/v1/company/1/vendor/2/',
            data=json.dumps(VendorRequestParams.put_update_a_vendor_valid_params_set()), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual('success', api_response['status'])
        self.assertEqual('Vendor updated successfully.', api_response['message'])
        self.assertEqual(200, api_response['code'])
        self.assertEqual(None, api_response['data'])

        # Update Vendor Companies Currency with Invalid Company ID
        request_params = VendorRequestParams.put_update_a_vendor_valid_params_set()
        request_params['user_companies_currency'].append({"99": {"air_currency": "JPY","lcl_currency": "EUR","fcl_currency": "EUR"}})
        response = self.client.put(VendorRequestParams.api_url() + '/api/v1/company/1/vendor/2/',
            data=json.dumps(request_params), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Company not found', api_response['message'])
        self.assertEqual('F0001', api_response['code'])
        self.assertEqual({}, api_response['data'])

        # Update Vendor Companies Currency with Blank Currency details
        request_params = VendorRequestParams.put_update_a_vendor_valid_params_set()
        request_params['user_companies_currency'][2]['3']['lcl_currency'] = None
        response = self.client.post(VendorRequestParams.api_url() + '/api/v1/company/1/vendor/',
            data=json.dumps(request_params), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Companies currency is required.', api_response['message'])
        self.assertEqual('F0145', api_response['code'])
        self.assertEqual({}, api_response['data'])

        # Update Vendor Companies Mode with invalid mode value
        request_params = VendorRequestParams.put_update_a_vendor_valid_params_set()
        request_params['companies_mode'][1]['2'] = ['ATC', 'FCLE_XYZ', 'LCLE', 'LCLI']
        response = self.client.post(VendorRequestParams.api_url() + '/api/v1/company/1/vendor/',
            data=json.dumps(request_params), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Vendor expertise transport mode is invalid.', api_response['message'])
        self.assertEqual('F0914', api_response['code'])
        self.assertEqual({}, api_response['data'])
