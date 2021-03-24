from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailNotification:

    @staticmethod
    def verification_email(customer_details,absolute_link):

        data = {'email':customer_details['email'], 'user_name':customer_details['name'], 'absolute_link':absolute_link}
        subject = 'Please activate your account'
        html_message = render_to_string(template_name='verification_email.html', context=data) 
        # message = strip_tags(html_message)
        message = None
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [customer_details['email']]    
        send_mail(subject, from_email, message, recipient_list, html_message=html_message, fail_silently=True)

    
    @staticmethod
    def forgot_password(email_data):
        subject = 'Please set your new password'
        html_message = render_to_string(template_name='forgot_password.html', context=email_data) 
        message = None
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email_data['email']]    
        send_mail(subject, from_email, message, recipient_list, html_message=html_message, fail_silently=True)


    @staticmethod
    def set_profile_email(datasets):
        subject = 'Please activate your account'
        html_message = render_to_string(template_name='set_profile_email.html', context=datasets)
        message = None
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [datasets['customer_email'], settings.ADMIN_EMAIL]
        send_mail(subject, from_email, message, recipient_list, html_message=html_message, fail_silently=True)


    @staticmethod
    def vendor_activation(email_data):
        subject = 'Activate your account'
        html_message = render_to_string(template_name='vendor_activation.html', context=email_data)
        message = None
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email_data['email'], settings.ADMIN_EMAIL]
        send_mail(subject, from_email, message, recipient_list, html_message=html_message, fail_silently=True)

    @staticmethod
    def invite_vendor(email_data):
        subject = 'New vendor addition'
        html_message = render_to_string(template_name='vendor_invitation.html', context=email_data)
        message = None
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email_data['vendor_super_admin_email'], settings.ADMIN_EMAIL]
        send_mail(subject, from_email, message, recipient_list, html_message=html_message, fail_silently=True)

    @staticmethod
    def invite_vendor_with_link(email_data):
        subject = 'Vendor invitation with link'
        html_message = render_to_string(template_name='vendor_invitation_link.html', context=email_data)
        message = None
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email_data['email'], settings.ADMIN_EMAIL]
        send_mail(subject, from_email, message, recipient_list, html_message=html_message, fail_silently=True)

