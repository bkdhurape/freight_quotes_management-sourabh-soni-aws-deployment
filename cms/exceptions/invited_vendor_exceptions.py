from enum import Enum
from exceptions.base_exceptions import BaseException


class InvitedVendorException(BaseException):

    def getHTTPCode(self):
        return 400


class InvitedVendorError(Enum):
    INVITED_VENDOR_NOT_FOUND = {'code': 'F0181', 'msg': 'Invited vendor data not found.'}
    INVITED_VENDOR_EXISTS = {'code': 'F0182', 'msg': 'Invited vendor name already exists.'}
    INVITED_VENDOR_CREATION_FAILED = {'code': 'F0183', 'msg': 'Invited vendor not created.'}
    INVITED_VENDOR_ID_REQUIRED = {'code': 'F0184', 'msg': 'Invited vendor ID required.'}
    VENDOR_ALREADY_EXISTS = {'code': 'F0185', 'msg': 'Vendor already exists.'}
    CLIENT_ACTION_REQUIRED = {'code': 'F0186', 'msg': 'You can either ACCEPT or REJECT client'}
    INVITED_VENDOR_CANNOT_BE_DELETED = {'code': 'F0187', 'msg': 'You cannot delete this vendor.'}
    CANNOT_ACCEPT_OR_REJECT_CLIENT = {'code': 'F0188', 'msg': 'You cannot ACCEPT or REJECT this client.'}
