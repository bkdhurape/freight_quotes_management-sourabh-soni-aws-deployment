from django.conf import settings


class TagRequestParameter:

    @staticmethod
    def api_url():
        return settings.API_HOST

    def post_customer_set(self):
        request_params = {
        "customer_details": {
            "name": "shiv",
            "email": "shivo7u1@g.com",
            "secondary_email":["shivs@g.com", "shivsmum@g.com", "shivsin@g.com"],
            "contact_no": [],
            "landline_no_dial_code": "+91",
            "landline_no": "9819123457",
            "customer_type": "impoter_or_exporter",
            "company_name": "fct_o7cA",
            "password": "apple",
            "designation": "accountant",
            "expertise": "import",
            "home_country": 1,
            "home_company": None
                            }
                        }

        return request_params

    def post_tag_set(self):
        request_params = {
            "name": "TestTag1"
        }
        return request_params

    def post_tag_second_set(self):
        request_params = TagRequestParameter.post_tag_set(self)
        request_params['name'] = "TestTag2"
        return request_params

    def get_tag_all(self):
        request_params = [
            {
                
            "id": 2,
            "status": 1,
            "name": "TestTag2",
            "company": 1,
            "parent": None
            },
            {
               
            "id": 1,
            "status": 1,
            "name": "TestTag1",
            "company": 1,
            "parent": None
            }
        ]

        return request_params
