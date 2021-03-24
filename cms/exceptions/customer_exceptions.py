from enum import Enum
from exceptions.base_exceptions import BaseException


class CustomerException(BaseException):

    def getHTTPCode(self):
        return 400


class CustomerError(Enum):
    CUSTOMER_NOT_FOUND = {'code': 'F0101', 'msg': 'Customer data not found.'}
    CUSTOMER_EXISTS = {'code': 'F0102', 'msg': 'Customer name already exists.'}
    CUSTOMER_CREATION_FAILED = {'code': 'F0103', 'msg': 'Customer not created.'}
    CUSTOMER_ID_REQUIRED = {'code': 'F0104', 'msg': 'Customer ID required.'}
    CONTACT_ADMIN = {'code': 'F0105', 'msg': 'Company already exists. Please contact your admin to register.'}
    CUSTOMER_COMPANY_DEPARTMENT_NOT_EXISTS = {'code': 'F0106', 'msg': 'For this company department does not exist.'}
    ALREADY_ACTIVATED = {'code': 'F0107', 'msg': 'You are already acivated. Please login to continue'}
    INVALID_TOKEN_CONTACT_ADMIN = {'code': 'F0108', 'msg': 'Invalid Token. Please contact admin for your account activation and other queries.'}
    INVALID_TOKEN_RESEND_LINK = {'code': 'F0109', 'msg': 'Invalid Token. Please click here to resend activation link or contact admin for any other queries.'}
    CUSTOMER_INVALID_CONTACT_NO = {'code': 'F0110', 'msg': 'Invalid contact no.'}
    PASSWORD_DID_NOT_MATCH={'code':'F0111','msg':'password did not match'}
    INVALID_EMAIL={'code':'F0112','msg':'Invalid Email'}
    PASSWORD_IS_REQUIRED={'code':'F0113','msg':'password is required'}
    CONFIRM_PASSWORD_IS_REQUIRED={'code':'F0114','msg':' confirm password is required'}
    CUSTOMER_SUPERVISOR_REQUIRED = {'code': 'F0115', 'msg': 'Customer supervisor is required.'}
    CUSTOMER_SUPERVISOR_IS_INVALID = {'code': 'F0116', 'msg': 'Invalid supervisor in request params.'}
    CUSTOMER_COMPANY_NOT_EXISTS = {'code': 'F0117', 'msg': 'For this customer company does not exist.'}
    CONTACT_NO_OR_LANDLINE_NO_REQUIRED = {'code': 'F0118', 'msg':'Enter either contact no or landline no.'}
    CUSTOMER_TYPE_OTHER_REQUIRED = {'code': 'F0119', 'msg':'Customer Type other is required.'}
    CUSTOMER_TYPE_REQUIRED = {'code': 'F0120', 'msg':'Customer Type is required.'}

