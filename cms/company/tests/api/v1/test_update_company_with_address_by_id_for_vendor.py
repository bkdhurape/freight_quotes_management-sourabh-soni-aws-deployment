from company.models.company import Company
from company.tests.api.v1.company_request_parameters import CompanyRequestParams
from rest_framework.test import APITestCase
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
from vendor.tests.api.v1.vendor_request_params import VendorRequestParams
import json



class TestUpdateCompanyById(APITestCase):

    fixtures = VendorRequestParams.get_seed_data_list()

    def setUp(self):
        self.vendor_post_api_url = VendorRequestParams.api_url() + '/api/v1/vendor/'
        self.vendor_register_params = VendorRequestParams.post_vendor_registration_personal_details_request_set()
        self.params = VendorRequestParams.post_add_vendor_valid_request_set()

        response = self.client.post(
            self.vendor_post_api_url, data=self.vendor_register_params, format='json')
        api_response_json = json.loads(response.content)

        vendor_name = self.vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(
            multi=True, name=vendor_name).values_list('id', 'home_company'))[0]
        self.vendor_id, self.company_id = vendor

        encoded_email = encode_data(
            self.vendor_register_params['vendor_details']['email'])
        test_vendor_send_activation_link_api_url = VendorRequestParams.api_url(
        ) + '/api/v1/company/' + str(self.company_id) + '/vendor/send_activation_link/' + encoded_email

        response = self.client.get(
            test_vendor_send_activation_link_api_url, format='json')
        self.final_api_response_json = json.loads(response.content)
        self.vendor_add_post_api_url = VendorRequestParams.api_url(
        ) + '/api/v1/company/' + str(self.company_id) + '/vendor/'

        response = self.client.get(
            self.final_api_response_json['data'], format='json')
        api_response_json = json.loads(response.content)

        response = self.client.post(VendorRequestParams.api_url(
        ) + '/user/login/', data=VendorRequestParams.login_valid_request_params(), format='json')
        api_response_json = json.loads(response.content)

    def test_company_create(self):
        '''Create company with valid params'''
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/'
        params = CompanyRequestParams.add_new_company_for_vendor()
        response = self.client.post(api_url, data=params, format='json')

        '''Update company with valid request params'''
        company_name = params['name']
        organization_id = params['organization']
        update_company_id = list(Company.find_by(
            multi=True, name=company_name).values_list('id', flat=True))[0]
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/' + \
            str(update_company_id) + '/'
        params = CompanyRequestParams.update_new_company_for_vendor()
        params['organization'] = organization_id
        response = self.client.put(api_url, data=params, format='json')
        api_response_json = json.loads(response.content)


        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response_json['status'])
        self.assertEqual('Company updated successfully',
                         api_response_json['message'])
        self.assertEqual(None, api_response_json['data'])

       
    def test_update_company_with_blank_street_data(self):
        '''Update a company with blank street'''
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/'
        params = CompanyRequestParams.add_new_company_for_vendor()
        response = self.client.post(api_url, data=params, format='json')
        company_name = params['name']
        organization_id = params['organization']
        update_company_id = list(Company.find_by(
            multi=True, name=company_name).values_list('id', flat=True))[0]
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/' + \
            str(update_company_id) + '/'

        params = CompanyRequestParams.update_company_with_Blank_street_for_vendor()
        params['organization'] = organization_id
        response = self.client.put(api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual(' street is required',
                         api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0702', api_response_json['code'])

       
    def test_company_create_update_null_street_data(self):
        
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/'
        params = CompanyRequestParams.add_new_company_for_vendor()
        response = self.client.post(api_url, data=params, format='json')
        company_name = params['name']
        organization_id = params['organization']
        update_company_id = list(Company.find_by(
            multi=True, name=company_name).values_list('id', flat=True))[0]
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/' + \
            str(update_company_id) + '/'

        params = CompanyRequestParams.update_company_with_null_street_for_vendor()
        params['organization'] = organization_id
        response = self.client.put(api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual(' street is required',
                         api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0702', api_response_json['code'])

    def test_update_company_with_null_country(self):

        
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/'
        params = CompanyRequestParams.add_new_company_for_vendor()
        response = self.client.post(api_url, data=params, format='json')
        company_name = params['name']
        organization_id = params['organization']
        update_company_id = list(Company.find_by(
            multi=True, name=company_name).values_list('id', flat=True))[0]
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/' + \
            str(update_company_id) + '/'


        params = CompanyRequestParams.update_company_with_null_country_for_vendor()
        params['organization'] = organization_id
        response = self.client.put(api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('you can not edit country',
                         api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0704', api_response_json['code'])


    def  test_update_company_with_another_country_for_vendor(self):
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/'
        params = CompanyRequestParams.add_new_company_for_vendor()
        response = self.client.post(api_url, data=params, format='json')
        company_name = params['name']
        organization_id = params['organization']


        update_company_id = list(Company.find_by(
            multi=True, name=company_name).values_list('id', flat=True))[0]
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/' + \
            str(update_company_id) + '/'

        params = CompanyRequestParams.update_company_with_another_country_for_vendor()
        params['organization'] = organization_id
        response = self.client.put(api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('you can not edit country',
                         api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0704', api_response_json['code'])

    def update_country_without_address_chunk(self):
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/'
        params = CompanyRequestParams.add_new_company_for_vendor()
        response = self.client.post(api_url, data=params, format='json')
        company_name = params['name']
        organization_id = params['organization']
        update_company_id = list(Company.find_by(
            multi=True, name=company_name).values_list('id', flat=True))[0]
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/' + \
            str(update_company_id) + '/'

        params = CompanyRequestParams.update_company_with_another_country_for_vendor()
        params['organization'] = organization_id
        response = self.client.put(api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('address are required',
                         api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0704', api_response_json['code'])
