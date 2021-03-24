from company.models.company import Company
from company.models.organization import Organization
from company.tests.api.v1.company_request_params import CompanyRequestParams
from rest_framework.test import APITestCase
from texttable import Texttable
import csv
import inspect
import json
import os
import re


class TestUpdateCompanyById(APITestCase):

    fixtures = [
        'country/fixtures/country.json'
        ]

    def test_company_create(self):

        # Create company with valid params 
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/'
        params = CompanyRequestParams.create_company_valid_response()
        response = self.client.post(api_url, data=params, format='json')

        table_list = []
        table_list.append(['Test Case ID', 'Test Scenario', 'Test Case', 'Test Suite', 'Method', 'URL', 'Test Data',
                           'Expected Result', 'Actual Result', 'Status'])

        # Update company with valid request params
        company_name = params['name']
        update_company_id = list(Company.find_by(multi=True, name=company_name).values_list('id', flat=True))[0]
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/' + str(update_company_id) + '/'
        # print('POST, URL = ', api_url)
        
        params = CompanyRequestParams.create_company_valid_response()
        params['industry'] = ["consumer_goods_or_fmcg", "marine"]
        params['business_activity'] = ["manufacturer", "agriculture"]
        params['organization'] = list(Organization.find_by(multi=True, name=company_name).values_list('id', flat=True))[0]
        # print('---params---', params)
        response = self.client.put(api_url, data=params, format='json')
        # print('response-status-code = ', response.status_code)
        api_response_byte = response.content
        api_response_utf8 = api_response_byte.decode('utf8').replace("'", '"')
        api_response_json = json.loads(api_response_utf8)
        # print('api_response_json =', api_response_json)
        
        test_scenario_lable = 'Update a company module.'
        test_case_lable = 'Update a company with valid details.'
        api_method_lable = 'PUT'
        params_lable = 'params'
        
        expected_api_status_code = 200
        actual_api_status_code = response.status_code
        status_code = True if expected_api_status_code == actual_api_status_code else False
        self.assertEqual(expected_api_status_code, actual_api_status_code)
        status = 'PASS' if status_code else 'FAIL'
        table_list.append(['1.1.1', test_scenario_lable, test_case_lable,
                           'Check api response status code.',
                           api_method_lable, api_url, params_lable, expected_api_status_code, actual_api_status_code,
                           status])

        expected_api_status_message = 'success'
        actual_api_status_message = api_response_json['status']
        api_status = True if expected_api_status_message == actual_api_status_message else False
        self.assertEqual(expected_api_status_message, actual_api_status_message)
        status = 'PASS' if api_status else 'FAIL'
        table_list.append(['1.1.2', test_scenario_lable, test_case_lable,
                           'Check api response status.',
                           api_method_lable, api_url, params_lable, expected_api_status_message,
                           actual_api_status_message, status])

        expected_api_message = "Company updated successfully"
        actual_api_message = api_response_json['message']
        api_message = True if expected_api_message == actual_api_message else False
        self.assertEqual(expected_api_message, actual_api_message)
        status = 'PASS' if api_message else 'FAIL'
        table_list.append(['1.1.3', test_scenario_lable, test_case_lable,
                           'Check api response message.',
                           api_method_lable, api_url, params_lable, expected_api_message, actual_api_message, status])

        expected_api_data = None
        actual_api_data = api_response_json['data']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.1.4', test_scenario_lable, test_case_lable,
                           'Check api response data.',
                           api_method_lable, api_url, params_lable, expected_api_data, actual_api_data, status])
        
        # Update a company with invalid industry & business activity data 
        company_name = params['name']
        update_company_id = list(Company.find_by(multi=True, name=company_name).values_list('id', flat=True))[0]
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/' + str(update_company_id) + '/'
        print('POST, URL = ', api_url)
        
        params = CompanyRequestParams.create_company_valid_response()
        params['industry'] = ["consumer_goods_or_fmcg", "marine_2"]
        params['business_activity'] = ["manufacturer", "agriculture_2"]
        params['organization'] = list(Organization.find_by(multi=True, name=company_name).values_list('id', flat=True))[0]
        print('---params---', params)
        response = self.client.put(api_url, data=params, format='json')
        print('response-status-code = ', response.status_code)
        api_response_byte = response.content
        api_response_utf8 = api_response_byte.decode('utf8').replace("'", '"')
        api_response_json = json.loads(api_response_utf8)
        print('api_response_json =', api_response_json)

        test_case_lable = 'Update a company with invalid industry & business activity data.'
        
        expected_api_status_code = 400
        actual_api_status_code = response.status_code
        status_code = True if expected_api_status_code == actual_api_status_code else False
        self.assertEqual(expected_api_status_code, actual_api_status_code)
        status = 'PASS' if status_code else 'FAIL'
        table_list.append(['1.2.1', test_scenario_lable, test_case_lable,
                           'Check api response status code.',
                           api_method_lable, api_url, params_lable, expected_api_status_code, actual_api_status_code,
                           status])

        expected_api_status_message = 'failure'
        actual_api_status_message = api_response_json['status']
        api_status = True if expected_api_status_message == actual_api_status_message else False
        self.assertEqual(expected_api_status_message, actual_api_status_message)
        status = 'PASS' if api_status else 'FAIL'
        table_list.append(['1.2.2', test_scenario_lable, test_case_lable,
                           'Check api response status.',
                           api_method_lable, api_url, params_lable, expected_api_status_message,
                           actual_api_status_message, status])

        expected_api_message = ''
        actual_api_message = api_response_json['message']
        api_message = True if expected_api_message == actual_api_message else False
        self.assertEqual(expected_api_message, actual_api_message)
        status = 'PASS' if api_message else 'FAIL'
        table_list.append(['1.2.3', test_scenario_lable, test_case_lable,
                           'Check api response message.',
                           api_method_lable, api_url, params_lable, expected_api_message, actual_api_message, status])

        expected_api_data = {'industry': {'1': ['"marine_2" is not a valid choice.']}, 'business_activity': {'1': ['"agriculture_2" is not a valid choice.']}}
        actual_api_data = api_response_json['data']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.2.4', test_scenario_lable, test_case_lable,
                           'Check api response data.',
                           api_method_lable, api_url, params_lable, expected_api_data, actual_api_data, status])

        expected_api_data = 'BEF0001'
        actual_api_data = api_response_json['code']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.2.5', test_scenario_lable, test_case_lable,
                           'Check api response code.',
                           api_method_lable, api_url, params_lable, expected_api_data, actual_api_data, status])
        
        # Update a company with invalid industry & business activity as null data 
        company_name = params['name']
        update_company_id = list(Company.find_by(multi=True, name=company_name).values_list('id', flat=True))[0]
        api_url = CompanyRequestParams.api_url() + '/api/v1/company/' + str(update_company_id) + '/'
        print('POST, URL = ', api_url)
        
        params = CompanyRequestParams.create_company_valid_response()
        params['industry'] = None
        params['business_activity'] = None
        params['organization'] = list(Organization.find_by(multi=True, name=company_name).values_list('id', flat=True))[0]
        print('---params---', params)
        response = self.client.put(api_url, data=params, format='json')
        print('response-status-code = ', response.status_code)
        api_response_byte = response.content
        api_response_utf8 = api_response_byte.decode('utf8').replace("'", '"')
        api_response_json = json.loads(api_response_utf8)
        print('api_response_json =', api_response_json)
        
        test_case_lable = 'Update a company with invalid industry & business activity as null data.'
        
        expected_api_status_code = 400
        actual_api_status_code = response.status_code
        status_code = True if expected_api_status_code == actual_api_status_code else False
        self.assertEqual(expected_api_status_code, actual_api_status_code)
        status = 'PASS' if status_code else 'FAIL'
        table_list.append(['1.3.1', test_scenario_lable, test_case_lable,
                           'Check api response status code.',
                           api_method_lable, api_url, params_lable, expected_api_status_code, actual_api_status_code,
                           status])

        expected_api_status_message = 'failure'
        actual_api_status_message = api_response_json['status']
        api_status = True if expected_api_status_message == actual_api_status_message else False
        self.assertEqual(expected_api_status_message, actual_api_status_message)
        status = 'PASS' if api_status else 'FAIL'
        table_list.append(['1.3.2', test_scenario_lable, test_case_lable,
                           'Check api response status.',
                           api_method_lable, api_url, params_lable, expected_api_status_message,
                           actual_api_status_message, status])

        expected_api_message = 'industry - This field may not be null.,business_activity - This field may not be null.'
        actual_api_message = api_response_json['message']
        api_message = True if expected_api_message == actual_api_message else False
        self.assertEqual(expected_api_message, actual_api_message)
        status = 'PASS' if api_message else 'FAIL'
        table_list.append(['1.3.3', test_scenario_lable, test_case_lable,
                           'Check api response message.',
                           api_method_lable, api_url, params_lable, expected_api_message, actual_api_message, status])

        expected_api_data = {'industry': ['This field may not be null.'], 'business_activity': ['This field may not be null.']}
        actual_api_data = api_response_json['data']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.3.4', test_scenario_lable, test_case_lable,
                           'Check api response data.',
                           api_method_lable, api_url, params_lable, expected_api_data, actual_api_data, status])

        expected_api_data = 'BEF0001'
        actual_api_data = api_response_json['code']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.3.5', test_scenario_lable, test_case_lable,
                           'Check api response code.',
                           api_method_lable, api_url, params_lable, expected_api_data, actual_api_data, status])
        
        # Draw tables in CMD prompt
        draw_table = Texttable()
        draw_table.add_rows(table_list)
        print(draw_table.draw())

        filepath = re.sub(r'[.]', '/', __package__)
        directory = 'media/testcase/' + filepath
        class_name = __class__.__name__
        function_name = inspect.stack()[0][3]
        filename = directory + '/TestCaseReport_' + class_name + '.csv'
        print('filename = ', filename)

        # Create dir if not present
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Create TestCaseReport_***.csv file
        if table_list:
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(table_list)
