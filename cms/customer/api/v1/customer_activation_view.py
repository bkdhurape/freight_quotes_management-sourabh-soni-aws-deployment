from customer.services.customer_manage_service import CustomerManageService
from rest_framework import generics, status
from utils.responses import success_response, error_response

class CustomerActivationView(generics.GenericAPIView):

    def get(self, request, company_id, token):
        customer_service = CustomerManageService({})
        response = customer_service.activate_customer(token)
        if response:
            if 'success' == response['status']:
                return success_response(message=response['message'],status_code = response['status_code'])
            else:
                return error_response(data=response['data'])
        else:
            return success_response(status_code=status.HTTP_400_BAD_REQUEST, status='failure',
                                   message='Customer activation failure.')


class CustomerActivationResendLinkView(generics.GenericAPIView): 

    def get(self, request, company_id, email):
        customer_service = CustomerManageService({})
        response = customer_service.resend_activation_link(email)
        if 'success' == response['status']:
            return success_response(message='Resend mail sent successfully.', data=response['activation_link'])
        else:
            return success_response(status_code=status.HTTP_400_BAD_REQUEST, status='failure',
                                   message='Cannot resend activation link.')
