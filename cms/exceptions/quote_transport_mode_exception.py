from enum import Enum
from exceptions.base_exceptions import BaseException


class QuoteTransportModeException(BaseException):

    def getHTTPCode(self):
        return 400

class QuoteTransportModeError(Enum):
    QUOTE_TRANSPORT_MODE_NOT_FOUND = {'code': 'F3051','msg': 'Quote transport mode not found'}

   
