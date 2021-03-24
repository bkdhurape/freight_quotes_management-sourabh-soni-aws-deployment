from company.models.organization import Organization
from django.conf import settings


class CompanyRequestPagination:

    @staticmethod
    def api_url():
        return settings.API_HOST

    def create_organization_data(self):
        org = Organization.objects.create(name='fc')
        org.save()
        organization_id = org.id
        return organization_id

    def post_company_set(self):
        organization = Organization.objects.create(name='fc')
        organization.save()
        organization_id = organization.id
        request_response = {
            "name": "companytest1",
            "company_type": "sole_proprietorship",
            "company_bio": "bio", 
            "company_structure": "company_structure",
            "industry": ["other"],
            "industry_other": "hekko",
            "business_activity": ["manufacturer", "supplier", "wholesaler"],
            "business_activity_other": "",
            "iec": 1233214567,
            "pan": "asdfg2344n",
            "gst": "12ABCDE1234A1Z1",
            "cin": "U67190TN2014PTC096978",
            "annual_revenue": 234,
            "organization": organization_id,
            "type": "customer",
            "address_details": {
                "street": "street123",
                "country": 1,
                "city": 1,
                "state": 1,
                "pincode": "1234567"

            }}

        return request_response

    def post_company_second_set(self):
        request_params = CompanyRequestPagination.post_company_set(self)
        request_params['name'] = "companytest2"
        return request_params


    def get_all_company(self):
        request_params = [
            {
                "id": 1,
                "status": 1,
                "name": "companytest1",
                "company_type": "sole_proprietorship",
                "industry": [
                    "other"
                ],
                "industry_other": "hekko",
                "business_activity": [
                    "manufacturer",
                    "supplier",
                    "wholesaler"
                ],
                "business_activity_other": "",
                "iec": "1233214567",
                "gst": "12ABCDE1234A1Z1",
                "pan": "asdfg2344n",
                "cin": "U67190TN2014PTC096978",
                "company_bio": "bio",
                "company_structure": "company_structure",
                "type": "customer",
                "organization": 1,
                "address_details": {
                        "id": 1,
                        "status": 1,
                        "entity_type": "company",
                        "entity_id": 1,
                        "address2": None,
                        "pincode": "1234567",
                        "type": None,
                        "country": 1,
                        "state": 1,
                        "city": 1, 
                        "street": "street123"
                    } 
                },
            {
                "id": 2,
                "status": 1,
                "name": "companytest2",
                "company_type": "sole_proprietorship",
                "industry": [
                    "other"
                ],
                "industry_other": "hekko",
                "business_activity": [
                    "manufacturer",
                    "supplier",
                    "wholesaler"
                ],
                "business_activity_other": "",
                "iec": "1233214567",
                "gst": "12ABCDE1234A1Z1",
                "pan": "asdfg2344n",
                "cin": "U67190TN2014PTC096978",
                "company_bio": "bio",
                "company_structure": "company_structure",
                "type": "customer",
                "organization": 2,
                "address_details": {
                        "id": 2,
                        "status": 1,
                        "entity_type": "company",
                        "entity_id": 2,
                        "address2": None,
                        "pincode": "1234567",
                        "type": None,
                        "country": 1,
                        "state": 1,
                        "city": 1,
                        "street": "street123"
                            }
            }
        ]

        return request_params
