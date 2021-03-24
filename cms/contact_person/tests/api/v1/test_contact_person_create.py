from company.models.company import Company
from contact_person.tests.api.v1.contact_person_request_params import ContactPersonRequestParams
from django.test import TestCase, Client
from rest_framework import status
import json


# initialize the APIClient app
client = Client()


class ContactPersonTest(TestCase):
    '''Test modules for creation Contact person (POST method) '''

    def setUp(self):
        company = Company.objects.create(
            name='Test Company'
        )
        self.api_url = ContactPersonRequestParams.api_url() + '/api/v1/company/' + \
            str(company.id)+'/contact_person/'

    def test_create_valid_contact_person(self):

        response = client.post(
            self.api_url,
            data=json.dumps(
                ContactPersonRequestParams.contact_person_request_set()),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual('success', api_response['status'])
        self.assertEqual('Contact person created successfully',
                         api_response['message'])
        self.assertEqual(200, api_response['code'])
        self.assertEqual(None, api_response['data'])

    def test_create_blank_name_contact_person(self):

        response = client.post(
            self.api_url,
            data=json.dumps(
                ContactPersonRequestParams.contact_person_blank_name_request_set()),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('name - This field may not be blank.',
                         api_response['message'])
        self.assertEqual(['This field may not be blank.'],
                         api_response['data']['name'])
        self.assertEqual('BEF0001', api_response['code'])

    def test_create_invalid_name_contact_person(self):

        response = client.post(
            self.api_url,
            data=json.dumps(
                ContactPersonRequestParams.contact_person_invalid_name_request_set()),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('name - Enter a valid value.',
                         api_response['message'])
        self.assertEqual(['Enter a valid value.'],
                         api_response['data']['name'])
        self.assertEqual('BEF0001', api_response['code'])

    def test_create_invalid_email_contact_person(self):

        response = client.post(
            self.api_url,
            data=json.dumps(
                ContactPersonRequestParams.contact_person_invalid_email_request_set()),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('email - Enter a valid email address.',
                         api_response['message'])
        self.assertEqual(['Enter a valid email address.'],
                         api_response['data']['email'])
        self.assertEqual('BEF0001', api_response['code'])

    def test_create_invalid_contact_no_contact_person(self):

        response = client.post(
            self.api_url,
            data=json.dumps(
                ContactPersonRequestParams.contact_person_invalid_contact_no_request_set()),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Invalid contact no.', api_response['message'])
        self.assertEqual({}, api_response['data'])
        self.assertEqual('BF0003', api_response['code'])
