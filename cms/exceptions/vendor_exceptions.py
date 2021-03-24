from enum import Enum
from exceptions.base_exceptions import BaseException


class VendorException(BaseException):

    def getHTTPCode(self):
        return 400


class VendorError(Enum):
    VENDOR_NOT_FOUND = {'code': 'F0901', 'msg': 'Vendor data not found.'}
    VENDOR_EXISTS = {'code': 'F0902', 'msg': 'Vendor name already exists.'}
    VENDOR_CREATION_FAILED = {'code': 'F0903', 'msg': 'Vendor not created.'}
    VENDOR_ID_REQUIRED = {'code': 'F0904', 'msg': 'Vendor ID required.'}
    CONTACT_ADMIN = {'code': 'F0905', 'msg': 'Company already exists. Please contact your admin to register.'}
    ALREADY_ACTIVATED = {'code': 'F0906', 'msg': 'You are already acivated. Please login to continue'}
    INVALID_TOKEN_CONTACT_ADMIN = {'code': 'F0907', 'msg': 'Invalid Token. Please contact admin for your account activation and other queries.'}
    INVALID_TOKEN_RESEND_LINK = {'code': 'F0908', 'msg': 'Invalid Token. Please click here to resend activation link or contact admin for any other queries.'}
    VENDOR_INACTIVE = {'code': 'F0909', 'msg': 'Please contact admin for your account activation and other queries.'}
    VENDOR_COMPANY_BRANCH_NOT_EXISTS = {'code': 'F0910', 'msg': 'The selected branch does not belong to this company.'}
    VENDOR_SUPERVISOR_REQUIRED = {'code': 'F0911', 'msg': 'Vendor supervisor is required.'}
    PASSWORD_DID_NOT_MATCH={'code':'F0912','msg':'password did not match'}
    INVALID_EMAIL={'code':'F0913','msg':'Invalid Email'}
    PASSWORD_IS_REQUIRED={'code':'F0914','msg':'password is required'}
    CONFIRM_PASSWORD_IS_REQUIRED={'code':'F0915','msg':' confirm password is required'}
    VENDOR_EXPERTISE_TRANSPORT_MODE_NOT_FOUND = {'code': 'F0916', 'msg': 'Vendor expertise transport mode not found.'}
    VENDOR_EXPERTISE_TRANSPORT_MODE_REQUIRED = {'code': 'F0917', 'msg': 'Vendor expertise transport mode is required.'}
    VENDOR_EXPERTISE_TRANSPORT_MODE_IS_INVALID = {'code': 'F0918', 'msg': 'Vendor expertise transport mode is invalid.'}
    CONTACT_NO_OR_LANDLINE_NO_REQUIRED = {'code': 'F0919', 'msg':'Enter either contact no or landline no.'}
