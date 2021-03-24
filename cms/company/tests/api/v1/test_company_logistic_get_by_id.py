from company.tests.api.v1.company_logistic_request_parameter import CompanyLogisticRequestParams
from company.tests.api.v1.company_request_parameters import CompanyRequestParams
from company.models.company import Company
from company.models import CompanyLogisticInfo
from django.core.management import call_command
from rest_framework.test import APITestCase
from texttable import Texttable
import csv
import inspect
import json
import os
import re


class TestCompanyLogisticInfoGetById(APITestCase):

    fixtures = CompanyRequestParams.get_seed_data_list()

    def test_company_create(self):

        api_url = CompanyLogisticRequestParams.api_url() + '/api/v1/company/'
        '''Create company with valid request params'''
        params = CompanyRequestParams.create_company_valid_response()
        response = self.client.post(api_url, data=params, format='json')
        table_list = []
        table_list.append(['Test Case ID', 'Test Scenario', 'Test Case', 'Test Suite', 'Method', 'URL', 'Test Data',
                           'Expected Result', 'Actual Result', 'Status'])

        # Make a request to get companyLogistic with currency  details by ID
        company_name = params['name']
        company_id = list(Company.find_by(
            multi=True, name=company_name).values_list('id', flat=True))[0]
        Companylogisticinfo_id = list(CompanyLogisticInfo.find_by(multi=True,company=company_id).values_list('id', flat=True))[0]
        api_url = CompanyLogisticRequestParams.api_url() + '/api/v1/company/' + \
            str(company_id) + '/company_logistic_info/' + str(Companylogisticinfo_id) + '/'

        print('POST, URL = ', api_url)
        response = self.client.get(api_url, format='json')
        print('response-status-code = ', response.status_code)
        api_response_byte = response.content
        api_response_utf8 = api_response_byte.decode('utf8')
        api_response_json = json.loads(api_response_utf8)

        test_scenario_lable = 'GET companylogisticInfo with currency details in companylogisticInfo module.'
        test_case_lable = 'GET companylogisticInfo valid details by id.'
        api_method_lable = 'GET'
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

        expected_api_message = "Company logistic info retrived successfully"
        actual_api_message = api_response_json['message']
        api_message = True if expected_api_message == actual_api_message else False
        self.assertEqual(expected_api_message, actual_api_message)
        status = 'PASS' if api_message else 'FAIL'
        table_list.append(['1.1.3', test_scenario_lable, test_case_lable,
                           'Check api response message.',
                           api_method_lable, api_url, params_lable, expected_api_message, actual_api_message, status])
        self.maxDiff = None
        expected_api_data = CompanyLogisticRequestParams.get_company_logistic_Info_with_currency_by_id()
        actual_api_data = api_response_json['data']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.1.4', test_scenario_lable, test_case_lable,
                           'Check api response data.',
                           api_method_lable, api_url, params_lable, expected_api_data, actual_api_data, status])

        api_url = CompanyLogisticRequestParams.api_url() + '/api/v1/company/'
        '''Create company with valid request params'''
        params = CompanyRequestParams.create_company_with_defaut_currency_based_on_home_country()
        response = self.client.post(api_url, data=params, format='json')
        # Make a request to get companyLogistic with currency  details by ID
        company_name = params['name']
        company_id = list(Company.find_by(
            multi=True, name=company_name).values_list('id', flat=True))[0]
        Companylogisticinfo_id = list(CompanyLogisticInfo.find_by(multi=True,company=company_id).values_list('id', flat=True))[0]
        api_url = CompanyLogisticRequestParams.api_url() + '/api/v1/company/' + \
            str(company_id) + '/company_logistic_info/' + str(Companylogisticinfo_id) + '/'

        response = self.client.get(api_url, format='json')
        api_response_byte = response.content
        api_response_utf8 = api_response_byte.decode('utf8')
        api_response_json = json.loads(api_response_utf8)

        test_case_lable = 'GET companylogisticInfo valid details by id.'
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

        expected_api_message = "Company logistic info retrived successfully"
        actual_api_message = api_response_json['message']
        api_message = True if expected_api_message == actual_api_message else False
        self.assertEqual(expected_api_message, actual_api_message)
        status = 'PASS' if api_message else 'FAIL'
        table_list.append(['1.2.3', test_scenario_lable, test_case_lable,
                           'Check api response message.',
                           api_method_lable, api_url, params_lable, expected_api_message, actual_api_message, status])
        self.maxDiff = None
        expected_api_data = CompanyLogisticRequestParams.get_company_logistic_Info_with_default_currency_by_id()
        actual_api_data = api_response_json['data']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.2.4', test_scenario_lable, test_case_lable,
                           'Check api response data.',
                           api_method_lable, api_url, params_lable, expected_api_data, actual_api_data, status])

        # Make a request to get companyLogistic with currency  details by invalid company ID

        company_name = params['name']
        company_id = list(Company.find_by(
            multi=True, name=company_name).values_list('id', flat=True))[0]
        Companylogisticinfo_id = list(CompanyLogisticInfo.find_by(multi=True,company=company_id).values_list('id', flat=True))[0]
        api_url = CompanyLogisticRequestParams.api_url() + '/api/v1/company/' + \
            str(company_id) + '/company_logistic_info/1' + str(Companylogisticinfo_id) + '/'
        response = self.client.get(api_url, format='json')
        api_response_byte = response.content
        api_response_utf8 = api_response_byte.decode('utf8')
        api_response_json = json.loads(api_response_utf8)

        test_case_lable = 'GET companylogisticInfo valid details by invalid  id.'

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
        self.assertEqual(expected_api_status_message,
                         actual_api_status_message)
        status = 'PASS' if api_status else 'FAIL'
        table_list.append(['1.3.2', test_scenario_lable, test_case_lable,
                           'Check api response status.',
                           api_method_lable, api_url, params_lable, expected_api_status_message,
                           actual_api_status_message, status])

        expected_api_message = 'Company not found'
        actual_api_message = api_response_json['message']
        api_message = True if expected_api_message == actual_api_message else False
        self.assertEqual(expected_api_message, actual_api_message)
        status = 'PASS' if api_message else 'FAIL'
        table_list.append(['1.3.3', test_scenario_lable, test_case_lable,
                           'Check api response message.',
                           api_method_lable, api_url, params_lable, expected_api_message, actual_api_message, status])
        self.maxDiff = None
        expected_api_data = {}
        actual_api_data = api_response_json['data']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.3.4', test_scenario_lable, test_case_lable,
                           'Check api response data.',
                           api_method_lable, api_url, params_lable, expected_api_data, actual_api_data, status])

        expected_api_data = "F0001"
        actual_api_data = api_response_json['code']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.3.5', test_scenario_lable, test_case_lable,
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
