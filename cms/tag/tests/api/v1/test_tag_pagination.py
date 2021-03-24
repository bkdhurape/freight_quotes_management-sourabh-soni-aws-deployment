from customer.models.customer import Customer
from django.core.management import call_command
from rest_framework.test import APITestCase
from tag.tests.api.v1.tag_request_parameter import TagRequestParameter
from texttable import Texttable
import csv
import inspect
import json
import os
import re


class TagPagination(APITestCase):

    @classmethod
    def setUp(cls):

        call_command('loaddata', 'country/fixtures/country.json', verbosity=0)

    def test_get_all_tag(self):
        # Tag creation

        api_url_customer = TagRequestParameter.api_url() + 'api/v1/customer/'

        params_customer = TagRequestParameter.post_customer_set(self)

        response_customer = self.client.post(
            api_url_customer, data=params_customer, format='json')

        get_company_name = params_customer['customer_details']['name']
        get_company_id = list(Customer.find_by(multi=True, name=get_company_name).values_list('id', flat=True))[0]

        api_url = TagRequestParameter.api_url() + 'api/v1/company/'+str(get_company_id)+'/tag/'

        table_list = []
        table_list.append(['Test Case ID', 'Test Scenario', 'Test Case', 'Test Suite', 'Method', 'URL', 'Test Data',
                           'Expected Result', 'Actual Result', 'Status'])

        params = TagRequestParameter.post_tag_set(self)

        self.client.post(api_url, data=params, format='json')

        params = TagRequestParameter.post_tag_second_set(self)

        self.client.post(api_url, data=params, format='json')


        response = self.client.get(api_url, format='json')
        api_response_byte = response.content

        api_response_utf8 = api_response_byte.decode('utf8').replace("'", '"')
        api_response_json = json.loads(api_response_utf8)

        test_scenario_lable = 'Tag get all module.'
        test_case_lable = 'Tag get all'
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

        expected_api_message = 'Tag data retrived successfully'
        actual_api_message = api_response_json['message']
        api_message = True if expected_api_message == actual_api_message else False
        self.assertEqual(expected_api_message, actual_api_message)
        status = 'PASS' if api_message else 'FAIL'
        table_list.append(['1.1.3', test_scenario_lable, test_case_lable,
                           'Check api response message.',
                           api_method_lable, api_url, params_lable, expected_api_message, actual_api_message, status])

        self.maxDiff = None
        expected_api_data = TagRequestParameter.get_tag_all(self)
        actual_api_data = api_response_json['data']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.1.4', test_scenario_lable, test_case_lable,
                           'Check api response data.',
                           api_method_lable, api_url, params_lable, expected_api_data, actual_api_data, status])

        # Company not found

        api_url = TagRequestParameter.api_url() + 'api/v1/company/99/tag/'

        params = TagRequestParameter.post_tag_set(self)

        self.client.post(api_url, data=params, format='json')

        params = TagRequestParameter.post_tag_second_set(self)

        self.client.post(api_url, data=params, format='json')

        response = self.client.get(api_url, format='json')

        api_response_byte = response.content

        api_response_utf8 = api_response_byte.decode('utf8').replace("'", '"')
        api_response_json = json.loads(api_response_utf8)

        test_scenario_lable = 'Tag get all module.'
        test_case_lable = 'Tag get all but company not found'
        api_method_lable = 'Get All'
        params_lable = 'params'

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
        self.assertEqual(expected_api_status_message,
                         actual_api_status_message)
        status = 'PASS' if api_status else 'FAIL'
        table_list.append(['1.2.2', test_scenario_lable, test_case_lable,
                           'Check api response status.',
                           api_method_lable, api_url, params_lable, expected_api_status_message,
                           actual_api_status_message, status])

        expected_api_message = 'Company not found'
        actual_api_message = api_response_json['message']
        api_message = True if expected_api_message == actual_api_message else False
        self.assertEqual(expected_api_message, actual_api_message)
        status = 'PASS' if api_message else 'FAIL'
        table_list.append(['1.2.3', test_scenario_lable, test_case_lable,
                           'Check api response message.',
                           api_method_lable, api_url, params_lable, expected_api_message, actual_api_message, status])

        expected_api_data = 'F0001'
        actual_api_data = api_response_json['code']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.2.4', test_scenario_lable, test_case_lable,
                           'Check api response code.',
                           api_method_lable, api_url, params_lable, expected_api_data, actual_api_data, status])

        expected_api_data = {}
        actual_api_data = api_response_json['data']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.2.5', test_scenario_lable, test_case_lable,
                           'Check api response data.',
                           api_method_lable, api_url, params_lable, expected_api_data, actual_api_data, status])

        # If there is only page size in url link it will display with that page number and default data limit

        api_url = TagRequestParameter.api_url() + 'api/v1/company/'+str(get_company_id)+'/tag/?page=1'

        params = TagRequestParameter.post_tag_set(self)

        self.client.post(api_url, data=params, format='json')

        params = TagRequestParameter.post_tag_second_set(self)

        self.client.post(api_url, data=params, format='json')

        response = self.client.get(api_url, format='json')

        api_response_byte = response.content

        api_response_utf8 = api_response_byte.decode('utf8').replace("'", '"')
        api_response_json = json.loads(api_response_utf8)

        test_scenario_lable = 'Tag get all pagination module.'
        test_case_lable = 'Tag get all with pagination data'
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

        expected_api_message = 'Tag data retrived successfully'
        actual_api_message = api_response_json['message']
        api_message = True if expected_api_message == actual_api_message else False
        self.assertEqual(expected_api_message, actual_api_message)
        status = 'PASS' if api_message else 'FAIL'
        table_list.append(['1.3.3', test_scenario_lable, test_case_lable,
                           'Check api response message.',
                           api_method_lable, api_url, params_lable, expected_api_message, actual_api_message, status])

        self.maxDiff = None
        expected_api_data = TagRequestParameter.get_tag_all(self)
        actual_api_data = api_response_json['data']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.3.4', test_scenario_lable, test_case_lable,
                           'Check api response data.',
                           api_method_lable, api_url, params_lable, expected_api_data, actual_api_data, status])

        # If there is page size and limit of data then it will display as per page size and data limit

        api_url = TagRequestParameter.api_url() + 'api/v1/company/'+str(get_company_id)+'/tag/?page=1&limit=2'

        params = TagRequestParameter.post_tag_set(self)

        self.client.post(api_url, data=params, format='json')

        params = TagRequestParameter.post_tag_second_set(self)

        self.client.post(api_url, data=params, format='json')

        response = self.client.get(api_url, format='json')

        api_response_byte = response.content

        api_response_utf8 = api_response_byte.decode('utf8').replace("'", '"')
        api_response_json = json.loads(api_response_utf8)

        test_scenario_lable = 'Tag get all pagination module.'
        test_case_lable = 'Tag get all with pagination data and data limit'
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

        expected_api_message = 'Tag data retrived successfully'
        actual_api_message = api_response_json['message']
        api_message = True if expected_api_message == actual_api_message else False
        self.assertEqual(expected_api_message, actual_api_message)
        status = 'PASS' if api_message else 'FAIL'
        table_list.append(['1.4.3', test_scenario_lable, test_case_lable,
                           'Check api response message.',
                           api_method_lable, api_url, params_lable, expected_api_message, actual_api_message, status])

        self.maxDiff = None
        expected_api_data = TagRequestParameter.get_tag_all(self)
        actual_api_data = api_response_json['data']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.4.4', test_scenario_lable, test_case_lable,
                           'Check api response data.',
                           api_method_lable, api_url, params_lable, expected_api_data, actual_api_data, status])

        # If there is no data on respective page then it will diaplay no more records

        api_url = TagRequestParameter.api_url() + 'api/v1/company/'+str(get_company_id)+'/tag/?page=10&limit=100'

        params = TagRequestParameter.post_tag_set(self)

        self.client.post(api_url, data=params, format='json')

        params = TagRequestParameter.post_tag_second_set(self)

        self.client.post(api_url, data=params, format='json')

        response = self.client.get(api_url, format='json')

        api_response_byte = response.content

        api_response_utf8 = api_response_byte.decode('utf8').replace("'", '"')
        api_response_json = json.loads(api_response_utf8)

        test_scenario_lable = 'Tag get all pagination module.'
        test_case_lable = 'Tag get all with no records'
        api_method_lable = 'Get All with pagination'
        params_lable = 'params'

        expected_api_status_code = 200
        actual_api_status_code = response.status_code
        status_code = True if expected_api_status_code == actual_api_status_code else False
        self.assertEqual(expected_api_status_code, actual_api_status_code)
        status = 'PASS' if status_code else 'FAIL'
        table_list.append(['1.5.1', test_scenario_lable, test_case_lable,
                           'Check api response status code.',
                           api_method_lable, api_url, params_lable, expected_api_status_code, actual_api_status_code,
                           status])

        expected_api_status_message = 'success'
        actual_api_status_message = api_response_json['status']
        api_status = True if expected_api_status_message == actual_api_status_message else False
        self.assertEqual(expected_api_status_message,
                         actual_api_status_message)
        status = 'PASS' if api_status else 'FAIL'
        table_list.append(['1.5.2', test_scenario_lable, test_case_lable,
                           'Check api response status.',
                           api_method_lable, api_url, params_lable, expected_api_status_message,
                           actual_api_status_message, status])

        expected_api_message = 'No more records'
        actual_api_message = api_response_json['message']
        api_message = True if expected_api_message == actual_api_message else False
        self.assertEqual(expected_api_message, actual_api_message)
        status = 'PASS' if api_message else 'FAIL'
        table_list.append(['1.5.3', test_scenario_lable, test_case_lable,
                           'Check api response message.',
                           api_method_lable, api_url, params_lable, expected_api_message, actual_api_message, status])

        expected_api_data = None
        actual_api_data = api_response_json['data']
        api_data = True if expected_api_data == actual_api_data else False
        self.assertEqual(expected_api_data, actual_api_data)
        status = 'PASS' if api_data else 'FAIL'
        table_list.append(['1.5.4', test_scenario_lable, test_case_lable,
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
