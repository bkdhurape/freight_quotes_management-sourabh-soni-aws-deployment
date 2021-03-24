from company.tests.api.v1.company_request_pagination import CompanyRequestPagination
from django.core.management import call_command
from rest_framework.test import APITestCase
from texttable import Texttable
import csv
import inspect
import json
import os
import re



class TestCompanyPagination(APITestCase):

    @classmethod
    def setUp(cls):

        call_command('loaddata', 'country/fixtures/country.json', verbosity=0)
        call_command('loaddata', 'state/fixtures/state.json', verbosity=0)
        call_command('loaddata', 'city/fixtures/city.json', verbosity=0)

    def test_get_all_company(self):
        # Company creation

        api_url = CompanyRequestPagination.api_url() + 'api/v1/company/'

        table_list = []
        table_list.append(['Test Case ID', 'Test Scenario', 'Test Case', 'Test Suite', 'Method', 'URL', 'Test Data',
                           'Expected Result', 'Actual Result', 'Status'])

        params = CompanyRequestPagination.post_company_set(self)

        self.client.post(api_url, data=params, format='json')

        params = CompanyRequestPagination.post_company_second_set(self)

        self.client.post(api_url, data=params, format='json')

        response = self.client.get(api_url, format='json')

        api_response_byte = response.content

        api_response_utf8 = api_response_byte.decode('utf8').replace("'", '"')
        api_response_json = json.loads(api_response_utf8)

        test_scenario_lable = 'Company get all module.'
        test_case_lable = 'Company get all'
        api_method_lable = 'Get All'
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
        self.assertEqual(expected_api_status_message,
                         actual_api_status_message)
        status = 'PASS' if api_status else 'FAIL'
        table_list.append(['1.1.2', test_scenario_lable, test_case_lable,
                           'Check api response status.',
                           api_method_lable, api_url, params_lable, expected_api_status_message,
                           actual_api_status_message, status])

        expected_api_message = 'Company Data retrived successfully'
        actual_api_message = api_response_json['message']
        api_message = True if expected_api_message == actual_api_message else False
        self.assertEqual(expected_api_message, actual_api_message)
        status = 'PASS' if api_message else 'FAIL'
        table_list.append(['1.1.3', test_scenario_lable, test_case_lable,
                           'Check api response message.',
                           api_method_lable, api_url, params_lable, expected_api_message, actual_api_message, status])

        self.maxDiff = None
        expected_api_data = CompanyRequestPagination.get_all_company(self)
        actual_api_data = api_response_json['data']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.1.4', test_scenario_lable, test_case_lable,
                           'Check api response data.',
                           api_method_lable, api_url, params_lable, expected_api_data, actual_api_data, status])

        
        # If there is only page size in url link it will display with that page number and default data limit

        api_url = CompanyRequestPagination.api_url() + 'api/v1/company/?page=1'

        params = CompanyRequestPagination.post_company_set(self)

        self.client.post(api_url, data=params, format='json')

        params = CompanyRequestPagination.post_company_second_set(self)

        self.client.post(api_url, data=params, format='json')

        response = self.client.get(api_url, format='json')

        api_response_byte = response.content

        api_response_utf8 = api_response_byte.decode('utf8').replace("'", '"')
        api_response_json = json.loads(api_response_utf8)

        test_scenario_lable = 'Company get all pagination module.'
        test_case_lable = 'Company get all with pagination data'
        api_method_lable = 'Get All with pagination'
        params_lable = 'params'

        expected_api_status_code = 200
        actual_api_status_code = response.status_code
        status_code = True if expected_api_status_code == actual_api_status_code else False
        self.assertEqual(expected_api_status_code, actual_api_status_code)
        status = 'PASS' if status_code else 'FAIL'
        table_list.append(['1.2.1', test_scenario_lable, test_case_lable,
                           'Check api response status code.',
                           api_method_lable, api_url, params_lable, expected_api_status_code, actual_api_status_code,
                           status])

        expected_api_status_message = 'success'
        actual_api_status_message = api_response_json['status']
        api_status = True if expected_api_status_message == actual_api_status_message else False
        self.assertEqual(expected_api_status_message,
                         actual_api_status_message)
        status = 'PASS' if api_status else 'FAIL'
        table_list.append(['1.2.2', test_scenario_lable, test_case_lable,
                           'Check api response status.',
                           api_method_lable, api_url, params_lable, expected_api_status_message,
                           actual_api_status_message, status])

        expected_api_message = 'Company Data retrived successfully'
        actual_api_message = api_response_json['message']
        api_message = True if expected_api_message == actual_api_message else False
        self.assertEqual(expected_api_message, actual_api_message)
        status = 'PASS' if api_message else 'FAIL'
        table_list.append(['1.2.3', test_scenario_lable, test_case_lable,
                           'Check api response message.',
                           api_method_lable, api_url, params_lable, expected_api_message, actual_api_message, status])

        self.maxDiff = None
        expected_api_data = CompanyRequestPagination.get_all_company(self)
        actual_api_data = api_response_json['data']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.2.4', test_scenario_lable, test_case_lable,
                           'Check api response data.',
                           api_method_lable, api_url, params_lable, expected_api_data, actual_api_data, status])

        # If there is page size and limit of data then it will display as per page size and data limit

        api_url = CompanyRequestPagination.api_url() + 'api/v1/company/?page=1&limit=2'

        params = CompanyRequestPagination.post_company_set(self)

        self.client.post(api_url, data=params, format='json')

        params = CompanyRequestPagination.post_company_second_set(self)

        self.client.post(api_url, data=params, format='json')

        response = self.client.get(api_url, format='json')

        api_response_byte = response.content

        api_response_utf8 = api_response_byte.decode('utf8').replace("'", '"')
        api_response_json = json.loads(api_response_utf8)

        test_scenario_lable = 'Company get all pagination module.'
        test_case_lable = 'Company get all with pagination data and data limit'
        api_method_lable = 'Get All with pagination'
        params_lable = 'params'

        expected_api_status_code = 200
        actual_api_status_code = response.status_code
        status_code = True if expected_api_status_code == actual_api_status_code else False
        self.assertEqual(expected_api_status_code, actual_api_status_code)
        status = 'PASS' if status_code else 'FAIL'
        table_list.append(['1.3.1', test_scenario_lable, test_case_lable,
                           'Check api response status code.',
                           api_method_lable, api_url, params_lable, expected_api_status_code, actual_api_status_code,
                           status])

        expected_api_status_message = 'success'
        actual_api_status_message = api_response_json['status']
        api_status = True if expected_api_status_message == actual_api_status_message else False
        self.assertEqual(expected_api_status_message,
                         actual_api_status_message)
        status = 'PASS' if api_status else 'FAIL'
        table_list.append(['1.3.2', test_scenario_lable, test_case_lable,
                           'Check api response status.',
                           api_method_lable, api_url, params_lable, expected_api_status_message,
                           actual_api_status_message, status])

        expected_api_message = 'Company Data retrived successfully'
        actual_api_message = api_response_json['message']
        api_message = True if expected_api_message == actual_api_message else False
        self.assertEqual(expected_api_message, actual_api_message)
        status = 'PASS' if api_message else 'FAIL'
        table_list.append(['1.3.3', test_scenario_lable, test_case_lable,
                           'Check api response message.',
                           api_method_lable, api_url, params_lable, expected_api_message, actual_api_message, status])

        self.maxDiff = None
        expected_api_data = CompanyRequestPagination.get_all_company(self)
        actual_api_data = api_response_json['data']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.3.4', test_scenario_lable, test_case_lable,
                           'Check api response data.',
                           api_method_lable, api_url, params_lable, expected_api_data, actual_api_data, status])

        # If there is no data on respective page then it will diaplay no more records

        api_url = CompanyRequestPagination.api_url() + 'api/v1/company/?page=10&limit=100'

        params = CompanyRequestPagination.post_company_set(self)

        self.client.post(api_url, data=params, format='json')

        params = CompanyRequestPagination.post_company_second_set(self)

        self.client.post(api_url, data=params, format='json')

        response = self.client.get(api_url, format='json')

        api_response_byte = response.content

        api_response_utf8 = api_response_byte.decode('utf8').replace("'", '"')
        api_response_json = json.loads(api_response_utf8)

        test_scenario_lable = 'Company get all pagination module.'
        test_case_lable = 'Company get all with no records'
        api_method_lable = 'Get All with pagination'
        params_lable = 'params'

        expected_api_status_code = 200
        actual_api_status_code = response.status_code
        status_code = True if expected_api_status_code == actual_api_status_code else False
        self.assertEqual(expected_api_status_code, actual_api_status_code)
        status = 'PASS' if status_code else 'FAIL'
        table_list.append(['1.4.1', test_scenario_lable, test_case_lable,
                           'Check api response status code.',
                           api_method_lable, api_url, params_lable, expected_api_status_code, actual_api_status_code,
                           status])

        expected_api_status_message = 'success'
        actual_api_status_message = api_response_json['status']
        api_status = True if expected_api_status_message == actual_api_status_message else False
        self.assertEqual(expected_api_status_message,
                         actual_api_status_message)
        status = 'PASS' if api_status else 'FAIL'
        table_list.append(['1.4.2', test_scenario_lable, test_case_lable,
                           'Check api response status.',
                           api_method_lable, api_url, params_lable, expected_api_status_message,
                           actual_api_status_message, status])

        expected_api_message = 'No more records'
        actual_api_message = api_response_json['message']
        api_message = True if expected_api_message == actual_api_message else False
        self.assertEqual(expected_api_message, actual_api_message)
        status = 'PASS' if api_message else 'FAIL'
        table_list.append(['1.4.3', test_scenario_lable, test_case_lable,
                           'Check api response message.',
                           api_method_lable, api_url, params_lable, expected_api_message, actual_api_message, status])

        expected_api_data = None
        actual_api_data = api_response_json['data']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.4.4', test_scenario_lable, test_case_lable,
                           'Check api response data.',
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
