from enum import Enum
from exceptions.base_exceptions import BaseException


class BadRequestException(BaseException):

    def getHTTPCode(self):
        return 400


class BadRequestError(Enum):
    INVALID_PARAMS = {'code': 'BF0001', 'msg': 'Invalid Params'}
    MANDATORY_PARAM = {'code': 'BF0002',
                       'msg': 'Please enter appropriate value.'}
    INVALID_CONTACT_NO = {'code': 'BF0003', 'msg': 'Invalid contact no.'}
    INVALID_TOKEN_CONTACT_ADMIN = {'code':'BF0004', 'msg': 'Invalid Token. Please contact admin for your account activation and other queries.'}
