from company.models.company import Company
from contact_person.tests.api.v1.contact_person_request_params import ContactPersonRequestParams
from contact_person.models.contact_person import ContactPerson
from django.test import TestCase, Client
from rest_framework import status
import json

# initialize the APIClient app
client = Client()


class ContactPersonTest(TestCase):
    '''Test modules for creation Contact person (Get by id method) '''

    def setUp(self):
        self.company = Company.objects.create(
            name='Test Company'
        )
        api_url = ContactPersonRequestParams.api_url() + '/api/v1/company/' + \
            str(self.company.id)+'/contact_person/'

        params = ContactPersonRequestParams.contact_person_request_set()

        response = client.post(
            api_url,
            data=json.dumps(params),
            content_type='application/json'
        )

        contact_person_name = params['name']
        self.contact_person_id = list(ContactPerson.find_by(
            multi=True, name=contact_person_name).values_list('id', flat=True))[0]

    def test_contact_person_get_by_id(self):
        api_url_get_by_id = ContactPersonRequestParams.api_url() + '/api/v1/company/' + \
            str(self.company.id)+'/contact_person/' + \
            str(self.contact_person_id)+'/'
        response = self.client.get(api_url_get_by_id, format='json')
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual(
            'Contact detail is retrieved successfully', api_response['message'])
        self.maxDiff = None
        self.assertEqual(ContactPersonRequestParams.conatct_person_get_by_id_response(
            self), api_response['data'])

    def test_contact_person_get_company_not_found(self):
        api_url = ContactPersonRequestParams.api_url() + '/api/v1/company/99999/contact_person/' + \
            str(self.contact_person_id)+'/'

        response = self.client.get(api_url, format='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Company not found', api_response['message'])
        self.assertEqual({}, api_response['data'])
        self.assertEqual('F0001', api_response['code'])

    def test_contact_person_get_details_not_found(self):

        api_url = ContactPersonRequestParams.api_url() + '/api/v1/company/' + \
            str(self.company.id)+'/contact_person/99999999/'

        response = client.put(api_url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Details not found', api_response['message'])
        self.assertEqual({}, api_response['data'])
        self.assertEqual('F0801', api_response['code'])
