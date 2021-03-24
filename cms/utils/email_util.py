from django.core import mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.template.loader import get_template
from exceptions import EmailException, EmailError
import smtplib
import socket

class EmailUtil:

    # Initialize connection and setting default values to is_html, is_file_attach and from_email

    def __init__(self):
        self.connection = mail.get_connection()
        self.is_html = False
        self.is_file_attach = False
        self.from_email = None


    # Set basic mail details
    # subject - Email Subject   (String)
    # context - HTML Email Data (Dictionary)

    def set_mail_details(self, subject, context = {}):
        self.subject = subject
        self.context = context


    # Set content based on type of message. If message has html content then passed template will be use as email body
    # If message is not html then plain message will be used as email body
    # template  - HTML Email Body Content (Temlpate)
    # content   - Plain Email Body Content (String)

    def set_content_or_template(self, template = None, content = None):
        if self.is_html == True:
            message_template = get_template(template)
            self.message_content = message_template.render(self.context)
        else:
            self.message_content = content


    # Set from email, default value is None
    # from_email - Value or None (String)

    def set_from(self, from_email = None):
        self.from_email = from_email


    # Set recipients details here
    # to - This will be list of to email id (List)
    # cc - This will be list of cc email id : Optional (List)

    def set_recepients(self, to, cc = []):
        self.to_emails = to
        self.cc_emails = cc
        self.cc_emails.append(settings.ADMIN_EMAIL)


    # This function is used to call generate_messages function and set send_to_all flag
    # send_to_all - This flag defaulr value id False by default, If set to true email will be send to all recipients individually

    def send_messages(self, send_to_all = False):
        self.send_to_all = send_to_all
        messages = self.generate_messages()
        self.send_mail(messages)


    # This function is used to set is_file_attach flag value if true then email will be sent with attachment
    # is_file_attach - True / False (Boolean)

    def is_attachment(self, is_file_attach = False):
        self.is_file_attach = is_file_attach


    # This function is used to attach files
    # attachments - File path (List)

    def set_attachments(self, attachments):
        self.attachments = attachments


    # This funtion is used to send all the messages
    # mail_messages - List of all the messages (List)

    def send_mail(self, mail_messages):

        try:
            self.connection.open()
            self.connection.send_messages(mail_messages)
            self.connection.close()
        except smtplib.SMTPConnectError:
            raise EmailException(EmailError.SMTP_CONNECT_ERROR)
        except smtplib.SMTPAuthenticationError:
            raise EmailException(EmailError.SMTP_AUTHENTICATION_ERROR)
        except socket.error:
            raise EmailException(EmailError.CONNECTION_TIMEOUT)
        except smtplib.SMTPException:
            raise EmailException(EmailError.SMTP_EXCEPTION)


    # Generate message based on the value of send_to_all flag value i.e, True or False
    # if True, then send to all recipients individually
    # if False, send to all the recipients at once

    def generate_messages(self):

        messages = []

        if self.send_to_all == True:
            for recipient in self.to_emails:
                message = self.create_and_get_message(recipient=recipient)
                messages.append(message)
        else:
            message = self.create_and_get_message()
            messages.append(message)

        return messages


    # Create message based on different configuration like email_config and message content type and get all the messages
    # recipient - None or Value (String)

    def create_and_get_message(self, recipient = None):

        email_config = {'subject': self.subject, 'body': self.message_content, 'from_email': self.from_email, 'cc': self.cc_emails}
        if self.send_to_all == True:
            email_config.update({'to': [recipient]})
        else:
            email_config.update({'to': self.to_emails})

        message = EmailMessage(**email_config)
        message.content_subtype = 'html' if self.is_html == True else 'plain'
        message = self.set_mail_attachments(message);

        return message


    # This function is used to attach file to message passed as an argument.
    # message - EmailMessage Object with prefedined email_config and content type settings

    def set_mail_attachments(self, message):

        if self.is_file_attach == True:
            for attachment in self.attachments:
                message.attach_file(attachment);

        return message
