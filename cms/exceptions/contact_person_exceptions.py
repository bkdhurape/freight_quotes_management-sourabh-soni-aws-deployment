from enum import Enum
from exceptions.base_exceptions import BaseException


class ContactPersonException(BaseException):

    def getHTTPCode(self):
        return 400


class ContactPersonError(Enum):
    
    CONTACT_PERSON_NOT_FOUND = {'code': 'F0801', 'msg': 'Details not found'}
    CONTACT_NAME_REQUIRED = {'code': 'F0802', 'msg':'Contact name is required'}
    CONTACT_EMAIL_REQUIRED = {'code': 'F0803', 'msg':'Contact email is required'}
    CONTACT_NAME_AND_EMAIL_REQUIRED = {'code': 'F0804', 'msg':'Contact name and email are required'}    