from enum import Enum
from exceptions.base_exceptions import BaseException


class CurrencyException(BaseException):

    def getHTTPCode(self):
        return 400


class CurrencyError(Enum):
    CURRENCY_NOT_FOUND = {'code': 'F0141', 'msg': 'Currency not found.'}
    CURRENCY_EXISTS = {'code': 'F0142', 'msg': 'Currency name already exists.'}
    CURRENCY_CREATION_FAILED = {'code': 'F0143', 'msg': 'Currency not created.'}
    CURRENCY_ID_REQUIRED = {'code': 'F0144', 'msg': 'Currency ID required.'}
    COMPANIES_CURRENCY_REQUIRED = {'code': 'F0145', 'msg': 'Companies currency is required.'}
