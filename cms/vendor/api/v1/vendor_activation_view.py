from rest_framework import generics, status
from utils.responses import success_response,error_response
from vendor.services.vendor_manage_service import VendorManageService

class VendorActivationView(generics.GenericAPIView):
    def get(self, request, company_id, token):
        vendor_service = VendorManageService({})
        response = vendor_service.activate_vendor(token)
        if response:
            if 'success' == response['status']:
                return success_response(message=response['message'],status_code = response['status_code'])
            else:
                return error_response(data=response['data'])
        else:
            return success_response(status_code=status.HTTP_400_BAD_REQUEST, status='error',
                                   message='Vendor activation failure.')


class VendorActivationResendLinkView(generics.GenericAPIView):

    def get(self, request, company_id, email):
        vendor_service = VendorManageService({})
        response = vendor_service.resend_activation_link(email = email)

        if 'success' == response['status']:
            return success_response(message=response['message'],status_code=response['status_code'])
        else:
            return success_response(status_code=status.HTTP_400_BAD_REQUEST, status='error',
                                   message='Cannot resend activation link.')
