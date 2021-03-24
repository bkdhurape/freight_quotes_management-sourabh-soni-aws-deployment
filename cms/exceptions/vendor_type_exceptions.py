from enum import Enum
from exceptions.base_exceptions import BaseException


class VendorTypeException(BaseException):

    def getHTTPCode(self):
        return 400


class VendorTypeError(Enum):
    VENDOR_TYPE_NOT_FOUND = {'code': 'F0951', 'msg': 'Vendor type data not found.'}
    VENDOR_TYPE_EXISTS = {'code': 'F0952', 'msg': 'Vendor type name already exists.'}
    VENDOR_TYPE_CREATION_FAILED = {'code': 'F0953', 'msg': 'Vendor type not created.'}
    VENDOR_TYPE_ID_REQUIRED = {'code': 'F0954', 'msg': 'Vendor type ID required.'}
    INVALID_VENDOR_TYPE = {'code': 'F0955', 'msg': 'Invalid vendor type'}
    VENDOR_TYPE_IS_REQUIRED = {'code': 'F0956', 'msg': 'vendor type is required'}
