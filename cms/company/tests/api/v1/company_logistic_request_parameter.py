from company.models.organization import Organization
from django.conf import settings


class CompanyLogisticRequestParams:

    @staticmethod
    def api_url():
        return settings.API_HOST

    def get_company_logistic_Info_with_currency():
        request_response = {

            "additional_details": {
                    "id": 1,
                    "status": 1,
                    "annaul_logistic_spend_currency": "USD",
                    "annual_logistic_spend": "3000.000",
                    "annual_air_shipments": 300,
                    "annual_lcl_shipments": 300,
                    "annual_fcl_shipments": 300,
                    "total_shipments": 900,
                    "annual_air_volume": "300.000",
                    "annual_lcl_volume": "300.000",
                    "annual_fcl_volume": "300.000",
                    "incorporation_year": 2019,
                    "incorporation_number": "ABCXYZ",
                    "annual_revenue_currency": "USD",
                    "annual_revenue": "2000.000",
                    "company": 1
                },
            "currency_profile_detail": {
                    "id": 1,
                    "entity_type": "company",
                    "entity_id": 1,
                    "air_currency": "usd",
                    "lcl_currency": "usd",
                    "fcl_currency": "usd"
                }
            
        }
        return request_response

    def get_company_logistic_Info_with_default_currency():
        request_response = {

            "additional_details": {
                    "id": 2,
                    "status": 1,
                    "annaul_logistic_spend_currency": "USD",
                    "annual_logistic_spend": "3000.000",
                    "annual_air_shipments": 300,
                    "annual_lcl_shipments": 300,
                    "annual_fcl_shipments": 300,
                    "total_shipments": 900,
                    "annual_air_volume": "300.000",
                    "annual_lcl_volume": "300.000",
                    "annual_fcl_volume": "300.000",
                    "incorporation_year": 2019,
                    "incorporation_number": "ABCXYZ",
                    "annual_revenue_currency": "USD",
                    "annual_revenue": "2000.000",
                    "company":2,
                    
                },
            "currency_profile_detail": {
                    "id": 2,
                    "entity_type": "company",
                    "entity_id": 2,
                    "air_currency": "INR",
                    "lcl_currency": "INR",
                    "fcl_currency": "INR"
                }
        
        }
        return request_response
    '''update the currency'''
    def update_company_logistic_Info_with_currency():
        request_response = {

        "annaul_logistic_spend_currency": "USD",
        "annual_logistic_spend": "3000.000",
        "annual_air_shipments": 300,
        "annual_lcl_shipments": 300,
        "annual_fcl_shipments": 300,
        "total_shipments": 900,
        "annual_air_volume": "300.000",
        "annual_lcl_volume": "300.000",
        "annual_fcl_volume": "300.000",
        "incorporation_year": 2019,
        "incorporation_number": "ABCXYZ",
        "annual_revenue_currency": "USD",
        "annual_revenue": "2000.000",
        "currency_profile_detail": {
            'id':1,
            "air_currency": "INR",
            "lcl_currency": "INR",
            "fcl_currency": "INR"
        }
    
        }

        return request_response


    def get_company_logistic_Info_with_currency_by_id():
        request_response = {

             "additional_details": {
                    "id": 1,
                    "status": 1,
                    "annaul_logistic_spend_currency": "USD",
                    "annual_logistic_spend": "3000.000",
                    "annual_air_shipments": 300,
                    "annual_lcl_shipments": 300,
                    "annual_fcl_shipments": 300,
                    "total_shipments": 900,
                    "annual_air_volume": "300.000",
                    "annual_lcl_volume": "300.000",
                    "annual_fcl_volume": "300.000",
                    "incorporation_year": 2019,
                    "incorporation_number": "ABCXYZ",
                    "annual_revenue_currency": "USD",
                    "annual_revenue": "2000.000",
                    "company": 1
                },
            "currency_profile_detail": {
                    "id": 1,
                    "entity_type": "company",
                    "entity_id": 1,
                    "air_currency": "usd",
                    "lcl_currency": "usd",
                    "fcl_currency": "usd"
                }
            
        }
        return request_response

    def get_company_logistic_Info_with_default_currency_by_id():
        request_response = {

             "additional_details": {
                    "id": 2,
                    "status": 1,
                    "annaul_logistic_spend_currency": "USD",
                    "annual_logistic_spend": "3000.000",
                    "annual_air_shipments": 300,
                    "annual_lcl_shipments": 300,
                    "annual_fcl_shipments": 300,
                    "total_shipments": 900,
                    "annual_air_volume": "300.000",
                    "annual_lcl_volume": "300.000",
                    "annual_fcl_volume": "300.000",
                    "incorporation_year": 2019,
                    "incorporation_number": "ABCXYZ",
                    "annual_revenue_currency": "USD",
                    "annual_revenue": "2000.000",
                    "company":2,
                    
                },
            "currency_profile_detail": {
                    "id": 2,
                    "entity_type": "company",
                    "entity_id": 2,
                    "air_currency": "INR",
                    "lcl_currency": "INR",
                    "fcl_currency": "INR"
                }
        
        }
        return request_response
