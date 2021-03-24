from company.models.company import Company
from contact_person.models.contact_person import ContactPerson
from contact_person.tests.api.v1.contact_person_request_params import ContactPersonRequestParams
from django.test import TestCase, Client
from rest_framework import status
import json


class ContactPersonTest(TestCase):
    '''Test modules for getting Contact person Details(Get method) '''

    def setUp(self):
        company = Company.objects.create(
            name='Test Company'
        )
        self.api_url = ContactPersonRequestParams.api_url() + '/api/v1/company/' + \
            str(company.id)+'/contact_person/'

        self.client.post(
            self.api_url,
            data=json.dumps(
                ContactPersonRequestParams.contact_person_request_set()),
            content_type='application/json'
        )

        for request_data in ContactPersonRequestParams.contact_person_valid_multiple_request_set():
            self.client.post(
                self.api_url,
                data=json.dumps(request_data),
                content_type='application/json'
            )

    def test_get_all_contact_person_of_company_with_records(self):
        api_url = self.api_url + '?page=1&limit=2'
        response = self.client.get(api_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        api_response = json.loads(response.content)

        self.assertEqual('success', api_response['status'])
        self.assertEqual(
            'Contact details retrieved successfully.', api_response['message'])
        self.assertEqual(200, api_response['code'])

        data = api_response['data']
        self.assertEqual(2, len(data))
        for contact in data:
            self.assertIn('id', contact)
            self.assertIn('status', contact)
            self.assertIn('name', contact)
            self.assertIn('email', contact)
            self.assertIn('secondary_email', contact)
            self.assertIn('contact_no', contact)
            self.assertIn('landline_no', contact)
            self.assertIn('landline_no_dial_code', contact)
            self.assertIn('designation', contact)
            self.assertIn('type', contact)

    def test_get_all_contact_person_of_company_with_no_records(self):
        api_url = self.api_url + '?page=3&limit=2'

        response = self.client.get(api_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        api_response = json.loads(response.content)

        self.assertEqual('success', api_response['status'])
        self.assertEqual('No more records', api_response['message'])
        self.assertEqual(200, api_response['code'])
        self.assertEqual(None, api_response['data'])

    def test_get_all_contact_person_of_other_company(self):
        api_url = ContactPersonRequestParams.api_url(
        ) + '/api/v1/company/9999999999/contact_person/'

        response = self.client.get(api_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        api_response = json.loads(response.content)

        self.assertEqual('success', api_response['status'])
        self.assertEqual('No more records', api_response['message'])
        self.assertEqual(200, api_response['code'])
        self.assertEqual(None, api_response['data'])
