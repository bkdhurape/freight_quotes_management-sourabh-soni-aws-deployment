from django.test import TestCase
from enquiry_management.models.company_expertise import CompanyExpertise
from enquiry_management.tests.api.v1.company_expertise_request_params import CompanyExpertiseRequestParams
from rest_framework import status
from rest_framework.test import APIClient
from utils.helpers import encode_data
from vendor.models.vendor import Vendor
import json


# initialize the APIClient app
client = APIClient()

class TestCompanyExpertiseCreate(TestCase):

    fixtures = CompanyExpertiseRequestParams.get_seed_data_list()
    def api_authentication(self):
        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)


    def setUp(self):
        # vendor registration
        self.vendor_post_api_url = CompanyExpertiseRequestParams.api_url() + 'api/v1/vendor/'
        self.vendor_register_params = CompanyExpertiseRequestParams.post_vendor_registration_personal_details_request_set()

        response = client.post(self.vendor_post_api_url, data=json.dumps(
            self.vendor_register_params), content_type='application/json')
        api_response_json = json.loads(response.content)

        vendor_name = self.vendor_register_params['vendor_details']['name']
        vendor = list(Vendor.find_by(
            multi=True, name=vendor_name).values_list('id', 'home_company'))[0]
        self.vendor_id, self.company_id = vendor

        encoded_email = encode_data(
            self.vendor_register_params['vendor_details']['email'])
        test_vendor_send_activation_link_api_url =CompanyExpertiseRequestParams.api_url(
        ) + 'api/v1/company/' + str(self.company_id) + '/vendor/send_activation_link/' + encoded_email


        response = client.get(
            test_vendor_send_activation_link_api_url, content_type='application/json')
        self.final_api_response_json = json.loads(response.content)
        self.vendor_add_post_api_url = CompanyExpertiseRequestParams.api_url(
        ) + '/api/v1/company/' + str(self.company_id) + '/vendor/'

        response = client.get(
            self.final_api_response_json['data'], content_type='application/json')
        api_response_json = json.loads(response.content)

        # vendor login
        response = client.post(CompanyExpertiseRequestParams.api_url() + 'user/login/', data=json.dumps(
            CompanyExpertiseRequestParams.login_valid_request_params()), content_type='application/json')
        api_response_json = json.loads(response.content)
        self.jwt_token = api_response_json['data'][0]['token']
        self.api_authentication()


        # company expertise url
        self.company_expertise_api_url= CompanyExpertiseRequestParams.api_url() + 'api/v1/company/' + \
            str(self.company_id)+'/expertise/'


    # create company expertise
    def test_company_expertise_with_air_transport_mode_create(self):

        params = CompanyExpertiseRequestParams.company_expertise_post_set(self)

        response = client.post(self.company_expertise_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', api_response['status'])
        self.assertEqual('company expertise added successfully',
                         api_response['message'])
        self.assertEqual(None, api_response['data'])

    # company expertise with blank commodity
    def test_company_expertise_blank_commodities(self):

        params = CompanyExpertiseRequestParams.post_company_expertise_blank_commodity(self)

        response = client.post(self.company_expertise_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('BEF0001', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('commodity - This field may not be null.',
                         api_response['message'])
        self.assertEqual( {'commodity': ['This field may not be null.']}, api_response['data'])

    # company expertise with blank choice commodity
    def test_company_expertise_blank_list_commodities(self):

        params = CompanyExpertiseRequestParams.post_company_expertise_blank_list_commodity(self)

        response = client.post(self.company_expertise_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('BEF0001', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('commodity - This list may not be empty.',
                         api_response['message'])
        self.assertEqual({'commodity': ['This list may not be empty.']}, api_response['data'])

    # blank container type for fcl Imoprt,export and third country
    def test_company_expertise_blank_container_type_for_fcl(self):

        params = CompanyExpertiseRequestParams.company_expertise_invalid_container_type_fcl_set(self)

        response = client.post(self.company_expertise_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F0602', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual(' for FCLI,FCLE,FCLTC container type is required.',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])
        
    # for fcl,lcl,air,air courier  third country trade_lanes required
    def test_company_expertise_blank_from_and_to_tradelanes_for_third_country(self):

        params = CompanyExpertiseRequestParams.post_company_expertise_invalid_third_country(self)

        response = client.post(self.company_expertise_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F0603', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('For Third Country, from_trade_lanes and to_trade_lanes are required.',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    # for import/export trade_lanes is required
    def test_company_expertise_blank_tradelanes_for_import_export(self):

        params = CompanyExpertiseRequestParams.post_company_expertise_trade_lanes_required(self)

        response = client.post(self.company_expertise_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('F0604', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('For AI, AE, FCLI, FCLE, LCLI, LCLE,ACI,ACE trade_lanes is required.',
                         api_response['message'])
        self.assertEqual({}, api_response['data'])

    # for single company duplicate transport mode are not allowed
    def test_company_expertise_with_duplicate_entry_transport_mode_in_same_company_id(self):

        params = CompanyExpertiseRequestParams.company_expertise_post_set(self)

        response = client.post(self.company_expertise_api_url, data=json.dumps(
            params), content_type='application/json')
        response = client.post(self.company_expertise_api_url, data=json.dumps(
            params), content_type='application/json')
        api_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('BEF0001', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('non_field_errors - The fields company, transport_mode must make a unique set.',
                         api_response['message'])
        self.assertEqual(['The fields company, transport_mode must make a unique set.'], api_response['data']['non_field_errors'])

    # company expertise with invalid company id which is not present in db
    def test_company_expertise_invalid_company_id(self):

        api_url_invalid_company_id = CompanyExpertiseRequestParams.api_url()+'api/v1/company/9999999/expertise/'

        params =CompanyExpertiseRequestParams.company_expertise_post_set(self)

        response = client.post(api_url_invalid_company_id, data=json.dumps(
            params), content_type='application/json')
        api_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(200, api_response['code'])
        self.assertEqual('success', api_response['status'])
        self.assertEqual('Access denied.',api_response['message'])
        self.assertEqual(None, api_response['data'])

    # create company expertise with invalid transport mode
    def test_company_expertise_invalid_transport_mode(self):

        params =CompanyExpertiseRequestParams.post_transport_mode_invalid_transport_mode_set(self)

        response = client.post(self.company_expertise_api_url, data=json.dumps(
            params), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        api_response = json.loads(response.content)

        self.assertEqual('BEF0001', api_response['code'])
        self.assertEqual('failure', api_response['status'])
        self.assertEqual('transport_mode - "LCLIT" is not a valid choice.',api_response['message'])
        self.assertEqual({'transport_mode': ['"LCLIT" is not a valid choice.']}, api_response['data'])