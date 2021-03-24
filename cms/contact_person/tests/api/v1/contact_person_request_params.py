from django.conf import settings


class ContactPersonRequestParams:

    @staticmethod
    def api_url():
        return settings.API_HOST

    # Request params: Contact Person request params with valid data
    def contact_person_request_set():
        request_params = {
            "name": "John Doe",
            "contact_no": [
                {
                    "dial_code": "91",
                    "contact_no": 9819123456
                }
            ],
            "landline_no_dial_code": "+91",
            "landline_no": "9819123457",
            "email": "johndoe@demo.com",
            "secondary_email": [
                "johnd@demo.com",
                "johnd@demo.in"
            ],
            "designation": "accountant"
        }
        return request_params

    # Request params: Contact Person request params with name as blank
    def contact_person_blank_name_request_set():
        request_params = {
            "name": "",
            "email": "johndoe@demo.com"
        }
        return request_params

    # Request params: Contact Person request params with invalid name
    def contact_person_invalid_name_request_set():
        request_params = {
            "name": "john-doe",
            "email": "johndoe@demo.com"
        }
        return request_params
        
    # Request params: Contact Person request params with invalid email
    def contact_person_invalid_email_request_set():
        request_params = {
            "name": "john doe",
            "email": "johndoedemo.com"
        }
        return request_params

    # Request params: Contact Person request params with invalid contact_no
    def contact_person_invalid_contact_no_request_set():
        contact_no = [
                {
                    "dial_code": "91",
                    "contact_no": 9819123456
                },
                {
                    "dial_code": "1321",
                    "contact_no": "9819123455wer"
                },
                {
                    "dial_code": "234",
                    "contact_no": 9819123454
                }
            ]
        request_params = {
            "name": "john doe",
            "email": "johndoe@demo.com",
            "contact_no": contact_no

        }
        return request_params

    # Request params: Contact Person request params with valid multiple dataset to test get request
    def contact_person_valid_multiple_request_set():
        request_params = [
            {
                "name": "Jane doe",
                "email": "janedoe@gmail.com"
            },
            {
                "name": "Poonam",
                "email": "poonamd@freightcrate.in"
            },
            {
                "name": "Dakshini",
                "email": "dakshini@gmail.com"
            }
        ]
        
        return request_params
    
    # Update contact person with valid details
    def contact_person_update(self):
        request_params = ContactPersonRequestParams.contact_person_request_set()
        request_params['name'] = "Priyanka_updated"
        request_params['email']= "priyankaupdated@gmail.com"
        return request_params

    # Update conatct person with blank email
    def contact_person_update_blank_email(self):
        request_params = ContactPersonRequestParams.contact_person_request_set()
        request_params['email'] = ""
        return request_params

    # Update contact person with invalid contact
    def contact_person_update_invalid_contact(self):
        request_params = ContactPersonRequestParams.contact_person_request_set()
        request_params['contact_no'][0]['dial_code']="11111111111" 
        return request_params

    # Update contact person with blank landline dial code
    def contact_person_update_blank_landline_dial_code(self):
        request_params = ContactPersonRequestParams.contact_person_request_set()
        request_params['landline_no_dial_code']="" 
        return request_params

    # Update contact person with invalid landline no
    def contact_person_update_invalid_landline_no(self):
        request_params = ContactPersonRequestParams.contact_person_request_set()
        request_params['landline_no']="02222222222222" 
        return request_params
    
    def conatct_person_get_by_id_response(self):
        request_params = {
            "id": 1,
            "status": 1,
            "name": "John Doe",
            "email": "johndoe@demo.com",
            "secondary_email": [
                "johnd@demo.com",
                "johnd@demo.in"
            ],
            "contact_no": [
                {
                    "dial_code": "91",
                    "contact_no": 9819123456
                }
            ],
            "landline_no_dial_code": "+91",
            "landline_no": "9819123457",
            "designation": "accountant",
            "type": "finance",
            "company": 1
        }
        return request_params