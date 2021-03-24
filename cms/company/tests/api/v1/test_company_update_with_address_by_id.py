from company.models.company import Company
from company.tests.api.v1.company_request_parameters import CompanyRequestParams
from customer.tests.api.v1.customer_request_params import CustomerRequestParams
from django.core.management import call_command
from django.test import Client, TestCase
from login.tests.api.v1.request_response_params import RequestResponseParams
from rest_framework.test import APITestCase
import json

client = Client()

class TestCompanyUpdateById(APITestCase):

    fixtures = CompanyRequestParams.get_seed_data_list()
    def setUp(self):

        self.api_url_host = RequestResponseParams.api_url()

        # Customer Registration
        response = client.post(self.api_url_host + '/api/v1/customer/',
                               data=json.dumps(
                                   CustomerRequestParams.post_customer_registration_personal_details_request_set()),
                               content_type='application/json')
        api_response = json.loads(response.content)
        activation_link = api_response['data']
        client.get(activation_link)
        response = self.client.post(self.api_url_host + '/user/login/', data=json.dumps(
            RequestResponseParams.login_valid_request_params()), content_type='application/json')
        self.company_post_api_url = CompanyRequestParams.api_url() + '/api/v1/company/'
        self.add_company_params = CompanyRequestParams.create_company_with_defaut_currency_based_on_home_country()

    def test_company_create(self):
        '''Create company with valid params'''
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/'
        params = CompanyRequestParams.create_company_valid_response()
        response = self.client.post(api_url, data=params, format='json')

        '''Update company with valid request params'''
        company_name = params['name']
        organization_id = params['organization']
        update_company_id = list(Company.find_by(
            multi=True, name=company_name).values_list('id', flat=True))[0]
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/' + \
            str(update_company_id) + '/'
        params = CompanyRequestParams.create_company_valid_response()
        params['name']='company_test_05'
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
        params = CompanyRequestParams.create_company_valid_response()
        response = self.client.post(api_url, data=params, format='json')
        company_name = params['name']
        organization_id = params['organization']
        update_company_id = list(Company.find_by(
            multi=True, name=company_name).values_list('id', flat=True))[0]
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/' + \
            str(update_company_id) + '/'

        params = CompanyRequestParams.create_company_with_Blank_street()
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
        params = CompanyRequestParams.create_company_valid_response()
        response = self.client.post(api_url, data=params, format='json')
        company_name = params['name']
        organization_id = params['organization']
        update_company_id = list(Company.find_by(
            multi=True, name=company_name).values_list('id', flat=True))[0]
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/' + \
            str(update_company_id) + '/'

        params = CompanyRequestParams.create_company_with_null_street()
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
        params = CompanyRequestParams.create_company_valid_response()
        response = self.client.post(api_url, data=params, format='json')
        company_name = params['name']
        organization_id = params['organization']
        update_company_id = list(Company.find_by(
            multi=True, name=company_name).values_list('id', flat=True))[0]
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/' + \
            str(update_company_id) + '/'


        params = CompanyRequestParams.create_company_with_null_country()
        params['organization'] = organization_id
        response = self.client.put(api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('you can not edit country',
                         api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0704', api_response_json['code'])


    def test_update_company_with_another_country(self):
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/'
        params = CompanyRequestParams.create_company_valid_response()
        response = self.client.post(api_url, data=params, format='json')
        company_name = params['name']
        organization_id = params['organization']


        update_company_id = list(Company.find_by(
            multi=True, name=company_name).values_list('id', flat=True))[0]
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/' + \
            str(update_company_id) + '/'

        params = CompanyRequestParams.update_company_with_another_country()
        params['organization'] = organization_id
        response = self.client.put(api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('you can not edit country',
                         api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0704', api_response_json['code'])

    def test_update_country_without_address_chunk(self):
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/'
        params = CompanyRequestParams.create_company_valid_response()
        response = self.client.post(api_url, data=params, format='json')
        company_name = params['name']
        organization_id = params['organization']
        update_company_id = list(Company.find_by(
            multi=True, name=company_name).values_list('id', flat=True))[0]
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/' + \
            str(update_company_id) + '/'

        params = CompanyRequestParams.create_or_update_company_blank_address_details()
        params['organization'] = organization_id
        response = self.client.put(api_url, data=params, format='json')
        api_response_json = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('failure', api_response_json['status'])
        self.assertEqual('address are required',
                         api_response_json['message'])
        self.assertEqual({}, api_response_json['data'])
        self.assertEqual('F0703', api_response_json['code'])
