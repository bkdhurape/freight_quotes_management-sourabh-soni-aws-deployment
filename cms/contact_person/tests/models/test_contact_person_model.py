from company.models.company import Company
from contact_person.models.contact_person import ContactPerson
from django.test import TestCase


class ContactPersonTest(TestCase):
    '''Test modules for Contact person Model '''

    def setUp(self):
        company = Company.objects.create(
            name='Test Company'
        )

        ContactPerson.objects.create(
            company_id=company.id,
            name="Test Prashant",
            contact_no=[
                {
                    "dial_code": "91",
                    "contact_no": 9819123456
                }
            ],
            landline_no_dial_code="+91",
            landline_no="9819123457",
            email="shivu5d@g.demo",
            secondary_email=[
                "shivs@g.com",
                "shivmum@g.com",
            ],
            designation="accountant",
        )

        ContactPerson.objects.create(
            company_id=company.id,
            name="Test poonam",
            email="pd@g.demo"
        )

    def test_contact_person_db(self):
        contact_person_prashant = ContactPerson.objects.get(
            email="shivu5d@g.demo")
        contact_person_poonam = ContactPerson.objects.get(email="pd@g.demo")


        self.assertEqual(contact_person_prashant.name, "Test Prashant")
        self.assertEqual(contact_person_poonam.name, "Test poonam")

