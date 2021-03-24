from company.models.company import Company
from contact_person.tests.api.v1.contact_person_request_params import ContactPersonRequestParams
from contact_person.models.contact_person import ContactPerson
from django.test import TestCase, Client
from rest_framework import status
import json

# initialize the APIClient app
client = Client()


class ContactPersonTest(TestCase):
    '''Test modules for creation Contact person (PUT method) '''

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
        self.api_url_update = ContactPersonRequestParams.api_url() + '/api/v1/company/' + \
            str(self.company.id)+'/contact_person/' + \
            str(self.contact_person_id)+'/'

    def test_update_contact_person(self):

        params = ContactPersonRequestParams.contact_person_update(self)

        response = client.put(
            self.api_url_update,
            data=json.dumps(params),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual(
            'Contact details are updated successfully', api_response['message'])
        self.assertEqual(None, api_response['data'])

    def test_update_contact_person_blank_name(self):

        params = ContactPersonRequestParams.contact_person_blank_name_request_set()

        response = client.put(
            self.api_url_update,
            data=json.dumps(params),
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

    def test_update_contact_person_invalid_name(self):

        params = ContactPersonRequestParams.contact_person_invalid_name_request_set()

        response = client.put(
            self.api_url_update,
            data=json.dumps(params),
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

    def test_update_contact_person_blank_email(self):

        params = ContactPersonRequestParams.contact_person_update_blank_email(
            self)

        response = client.put(
            self.api_url_update,
            data=json.dumps(params),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('email - This field may not be blank.',
                         api_response['message'])
        self.assertEqual(['This field may not be blank.'],
                         api_response['data']['email'])
        self.assertEqual('BEF0001', api_response['code'])

    def test_update_contact_person_invalid_contact(self):

        params = ContactPersonRequestParams.contact_person_update_invalid_contact(
            self)

        response = client.put(
            self.api_url_update,
            data=json.dumps(params),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Invalid contact no.', api_response['message'])
        self.assertEqual({}, api_response['data'])
        self.assertEqual('BF0003', api_response['code'])

    def test_update_contact_person_invalid_email(self):

        params = ContactPersonRequestParams.contact_person_invalid_email_request_set()

        response = client.put(
            self.api_url_update,
            data=json.dumps(params),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('email - Enter a valid email address.',
                         api_response['message'])
        self.assertEqual(["Enter a valid email address."],
                         api_response['data']['email'])
        self.assertEqual('BEF0001', api_response['code'])

    def test_update_contact_person_blank_landline_dial_code(self):

        params = ContactPersonRequestParams.contact_person_update_blank_landline_dial_code(
            self)

        response = client.put(
            self.api_url_update,
            data=json.dumps(params),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual(
            'landline_no_dial_code - This field may not be blank.', api_response['message'])
        self.assertEqual(["This field may not be blank."],
                         api_response['data']['landline_no_dial_code'])
        self.assertEqual('BEF0001', api_response['code'])

    def test_update_contact_person_invalid_landline_no(self):

        params = ContactPersonRequestParams.contact_person_update_invalid_landline_no(
            self)

        response = client.put(
            self.api_url_update,
            data=json.dumps(params),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual(
            'landline_no - Ensure this field has no more than 12 characters.', api_response['message'])
        self.assertEqual(["Ensure this field has no more than 12 characters."],
                         api_response['data']['landline_no'])
        self.assertEqual('BEF0001', api_response['code'])

    def test_update_contact_person_company_not_found(self):
        
        api_url = ContactPersonRequestParams.api_url(
        ) + '/api/v1/company/99/contact_person/'+str(self.contact_person_id)+'/'

        params = ContactPersonRequestParams.contact_person_update(self)

        response = client.put(
            api_url,
            data=json.dumps(params),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Company not found', api_response['message'])
        self.assertEqual({}, api_response['data'])
        self.assertEqual('F0001', api_response['code'])

    def test_update_contact_person_details_not_found(self):

        api_url = ContactPersonRequestParams.api_url() + '/api/v1/company/' + \
            str(self.company.id)+'/contact_person/99/'

        params = ContactPersonRequestParams.contact_person_update(self)

        response = client.put(
            api_url,
            data=json.dumps(params),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('failure', api_response['status'])
        self.assertEqual('Details not found', api_response['message'])
        self.assertEqual({}, api_response['data'])
        self.assertEqual('F0801', api_response['code'])
