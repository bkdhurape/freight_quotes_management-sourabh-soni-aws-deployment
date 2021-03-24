from customer.models.customer import Customer
from department.models.department import Department
from department.tests.api.v1.department_request_parameter import DepartmentRequestParameter
from django.test import TestCase, Client
from rest_framework import status
from utils.helpers import encode_data
import json

# initialize the APIClient app
client = Client()


class TestDepartmentCreate(TestCase):

    fixtures = DepartmentRequestParameter.get_seed_data_list()

    def setUp(self):
        self.customer_post_api_url = DepartmentRequestParameter.api_url() + \
            '/api/v1/customer/'
        self.customer_register_params = DepartmentRequestParameter.post_customer_registration_personal_details_request_set(self)
        self.params = DepartmentRequestParameter.post_add_customer_valid_request_set(self)

        response = client.post(self.customer_post_api_url, data=json.dumps(
            self.customer_register_params), content_type='application/json')
        api_response_json = json.loads(response.content)

        customer_name = self.customer_register_params['customer_details']['name']
        self.company_id = list(Customer.find_by(
            multi=True, name=customer_name).values_list('home_company', flat=True))[0]
        
        response = client.get(
            api_response_json['data'], content_type='application/json')
        response = client.post(DepartmentRequestParameter.api_url() + '/user/login/', data=json.dumps(
            DepartmentRequestParameter.login_valid_request_params(self)), content_type='application/json')

        self.department_api_url = DepartmentRequestParameter.api_url() + '/api/v1/company/' + \
            str(self.company_id) + '/department/'

    def test_department_post(self):

        params = DepartmentRequestParameter.post_department_set(self)

        response = client.post(self.department_api_url, data=json.dumps(
            params), content_type='application/json')


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Department created successfully',
                         api_response['message'])
        self.assertEqual(None, api_response['data'])

    def test_department_already_exist(self):

        params = DepartmentRequestParameter.post_department_set(self)

        response = client.post(self.department_api_url, data=json.dumps(
            params), content_type='application/json')

        params = DepartmentRequestParameter.post_department_name_already_exist(self)


        response = client.post(self.department_api_url, data=json.dumps(
            params), content_type='application/json')
            

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Department name already exists', api_response['message'])
        self.assertEqual({}, api_response['data'])
        self.assertEqual('F0202', api_response['code'])


    def test_company_not_found(self):

        api_url = DepartmentRequestParameter.api_url() + '/api/v1/company/999999/department/'

        params = DepartmentRequestParameter.post_department_set(self)

        response = client.post(api_url, data=json.dumps(
            params), content_type='application/json')


        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F0001', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Company not found',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    def test_name_cant_be_blank(self):

        params = DepartmentRequestParameter.post_department_cant_be_blank(self)

        response = client.post(self.department_api_url, data=json.dumps(
            params), content_type='application/json')
            

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('name - This field may not be blank.', api_response['message'])
        self.assertEqual(['This field may not be blank.'], api_response['data']['name'])
        self.assertEqual('BEF0001', api_response['code'])

