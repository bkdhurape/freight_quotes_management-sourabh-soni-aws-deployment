from enum import Enum
from exceptions.base_exceptions import BaseException


class EmailException(BaseException):

    def getHTTPCode(self):
        return 400


class EmailError(Enum):
    SMTP_CONNECT_ERROR = {'code': 'F02501', 'msg': 'Error connecting to the SMTP Server.'}
    SMTP_AUTHENTICATION_ERROR = {'code': 'F02502', 'msg': 'The server didn’t accept the username/password combination.'}
    CONNECTION_TIMEOUT = {'code': 'F02503', 'msg': 'Connection timeout.'}
    SMTP_EXCEPTION = {'code': 'F02504', 'msg': 'Something went wrong in SMTP module.'}
