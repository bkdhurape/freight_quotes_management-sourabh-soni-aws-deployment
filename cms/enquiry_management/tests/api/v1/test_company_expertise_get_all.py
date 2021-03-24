from django.test import TestCase
from enquiry_management.models.company_expertise import CompanyExpertise
from enquiry_management.tests.api.v1.company_expertise_request_params import CompanyExpertiseRequestParams
from rest_framework import status
from rest_framework.test import APIClient
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
import json


# initialize the APIClient app
client = APIClient()

class TestCompanyExpertiseCreate(TestCase):

    fixtures = CompanyExpertiseRequestParams.get_seed_data_list()

    def api_authentication(self):
        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)

    def setUp(self):
        # vendor registration
        self.vendor_post_api_url = CompanyExpertiseRequestParams.api_url() + 'api/v1/vendor/'
        self.vendor_register_params = CompanyExpertiseRequestParams.post_vendor_registration_personal_details_request_set()

        response = client.post(self.vendor_post_api_url, data=json.dumps(
            self.vendor_register_params), content_type='application/json')
        api_response_json = json.loads(response.content)

        vendor_name = self.vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(
            multi=True, name=vendor_name).values_list('id', 'home_company'))[0]
        self.vendor_id, self.company_id = vendor

        encoded_email = encode_data(
            self.vendor_register_params['vendor_details']['email'])
        test_vendor_send_activation_link_api_url =CompanyExpertiseRequestParams.api_url(
        ) + 'api/v1/company/' + str(self.company_id) + '/vendor/send_activation_link/' + encoded_email


        response = client.get(
            test_vendor_send_activation_link_api_url, content_type='application/json')
        self.final_api_response_json = json.loads(response.content)
        self.vendor_add_post_api_url = CompanyExpertiseRequestParams.api_url(
        ) + '/api/v1/company/' + str(self.company_id) + '/vendor/'

        response = client.get(
            self.final_api_response_json['data'], content_type='application/json')
        api_response_json = json.loads(response.content)

        # vendor login
        response = client.post(CompanyExpertiseRequestParams.api_url() + 'user/login/', data=json.dumps(
            CompanyExpertiseRequestParams.login_valid_request_params()), content_type='application/json')
        api_response_json = json.loads(response.content)
        self.jwt_token = api_response_json['data'][0]['token']
        self.api_authentication()

        # company expertise url
        self.company_expertise_api_url= CompanyExpertiseRequestParams.api_url() + 'api/v1/company/' + \
            str(self.company_id)+'/expertise/'

        self.params = CompanyExpertiseRequestParams.company_expertise_post_set(self)

    def test_company_expertise_get_all(self):
      
        response = client.post(self.company_expertise_api_url, data=json.dumps(
            self.params), content_type='application/json')  
        
        response = client.get(self.company_expertise_api_url)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Company Expertise data retrieved successfully.', api_response['message'])
        data = api_response['data']
        company_expertise_keys = CompanyExpertiseRequestParams.company_expertise_get(self)

        for company in data:
            for company_expertise_key in company_expertise_keys:
                self.assertIn(company_expertise_key,company)


    def test_company_expertise_get_all_with_pagination(self):
        self.param2 = CompanyExpertiseRequestParams.company_expertise_post_second_set(self)
        
        response = client.post(self.company_expertise_api_url, data=json.dumps(
            self.param2), content_type='application/json')

        api_url_pagination = CompanyExpertiseRequestParams.api_url()+ 'api/v1/company/' + \
            str(self.company_id)+'/expertise/?page=1&limit=2'

        response = client.get(api_url_pagination)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Company Expertise data retrieved successfully.', api_response['message'])

        data = api_response['data']
        company_expertise_keys = CompanyExpertiseRequestParams.company_expertise_get(self)

        for company in data:
            for company_expertise_key in company_expertise_keys:
                self.assertIn(company_expertise_key,company)

            
    def test_company_expertise_get_all_no_more_records(self):

        api_url_pagination = CompanyExpertiseRequestParams.api_url()+ 'api/v1/company/' + \
            str(self.company_id)+'/expertise/?page=100&limit=200'

        response = client.get(api_url_pagination)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('No more records', api_response['message'])
        self.assertEqual(None, api_response['data'])

    def test_company_expertise_get_all_company_not_found(self):

        api_url_company_not_found = CompanyExpertiseRequestParams.api_url()+ 'api/v1/company/100/expertise/?page=100&limit=200'
        response = client.get(api_url_company_not_found)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(200, api_response['code'])
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Access denied.', api_response['message'])
        self.assertEqual(None, api_response['data'])
