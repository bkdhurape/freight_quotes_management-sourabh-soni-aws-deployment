from enum import Enum
from exceptions.base_exceptions import BaseException


class OrganizationException(BaseException):

    def getHTTPCode(self):
        return 400


class OrganizationError(Enum):
    ORGANIZATION_REQUIRED = {'code': 'F0091', 'msg': 'Organization required'}
    ORGANIZATION_NOT_FOUND = {'code': 'F0092',
                              'msg': 'Organization not found '}
