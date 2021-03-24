from enum import Enum
from exceptions.base_exceptions import BaseException


class TransportException(BaseException):

    def getHTTPCode(self):
        return 400

class TransportError(Enum):
    TRANSPORT_NOT_FOUND = {'code': 'F3061','msg': 'Transport data not found'}
    