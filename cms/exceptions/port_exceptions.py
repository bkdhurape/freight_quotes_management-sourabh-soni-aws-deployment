from enum import Enum
from exceptions.base_exceptions import BaseException


class PortException(BaseException):

    def getHTTPCode(self):
        return 400


class PortError(Enum):
    PORT_NOT_FOUND = {'code': 'F02005', 'msg': 'Port data not found.'}
    PORT_EXISTS = {'code': 'F02006', 'msg': 'Port name already exists.'}
    PORT_CREATION_FAILED = {'code': 'F02007', 'msg': 'Port not created.'}
    PORT_ID_REQUIRED = {'code': 'F02008', 'msg': 'Port ID required.'}
    PORT_CODE_REQUIRED = {'code': 'F02009', 'msg': 'Port Code required.'}
    PORT_IATA_REQUIRED = {'code': 'F02010', 'msg': 'Port IATA required.'}
    INVALID_SEAPORT_ID = {'code': 'F02018', 'msg': 'Invalid seaport id'}
    INVALID_AIRPORT_ID = {'code': 'F02019', 'msg': 'Invalid airport id'}
