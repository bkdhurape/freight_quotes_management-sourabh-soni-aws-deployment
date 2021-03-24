from company.models.company import Company
from contact_person.models.contact_person import ContactPerson
from contact_person.serializers import ContactPersonSerializer
from exceptions import ContactPersonException , ContactPersonError
from utils.base_models import StatusBase
from utils.responses import get_paginated_data


class ContactPersonService:

    def __init__(self, data):
        self.data = data

    def get_details(self, company_id, contact_person_type):

        contact_person_data = ContactPerson.find_by(
            multi=True, join=False, company=company_id, contact_person_type=contact_person_type, status=StatusBase.ACTIVE).order_by('-id')

        contact_person_paginated_data = get_paginated_data(
            ContactPersonSerializer, contact_person_data, self.data)

        return contact_person_paginated_data
        

    def get_details_by_id(self, company_id, contact_person_id, contact_person_type):

        contact_person_data = ContactPerson.find_by(
            company=company_id, id=contact_person_id, contact_person_type=contact_person_type, status=StatusBase.ACTIVE)

        contact_person_serializer = ContactPersonSerializer(
            contact_person_data, many=False)

        return contact_person_serializer.data
    