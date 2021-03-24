from django.core import mail
from django.test import TestCase
from utils.email_util import EmailUtil

class TestEmail(TestCase):

    def setUp(self):
        pass

    def setup_email_config(self):
        test_mail = EmailUtil()
        test_mail.set_mail_details(subject='Test Subject')
        test_mail.set_content_or_template(content = "Test Content")
        test_mail.set_recepients(to=['tanveer.khan@mrhomecare.in','tanveerk@freightcrate.in','khanveerr@gmail.com'])
        test_mail.send_messages()



    def test_email_sent(self):
        self.setup_email_config()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Test Subject")
        self.assertEqual(mail.outbox[0].body, "Test Content")
