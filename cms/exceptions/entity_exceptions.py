from enum import Enum
from exceptions.base_exceptions import BaseException


class EntityException(BaseException):

    def getHTTPCode(self):
        return 400


class EntityError(Enum):
    ENTITY_NOT_FOUND = {'code': 'F02001', 'msg': 'Entity data not found.'}
    ENTITY_EXISTS = {'code': 'F02002', 'msg': 'Entity name already exists.'}
    ENTITY_CREATION_FAILED = {'code': 'F02003', 'msg': 'Entity not created.'}
    ENTITY_ID_REQUIRED = {'code': 'F02004', 'msg': 'Entity ID required.'}
    ENTITY_TYPE_REQUIRED = {'code': 'F02005', 'msg': 'You must select atleast one entity i.e. Shipper or Consignee'}
