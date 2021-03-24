from enum import Enum
from exceptions.base_exceptions import BaseException


class ProductException(BaseException):

    def getHTTPCode(self):
        return 400


class ProductError(Enum):
    PRODUCT_NOT_FOUND = {'code': 'F02011', 'msg': 'Product data not found.'}
    PRODUCT_EXISTS = {'code': 'F02012', 'msg': 'Product name already exists.'}
    PRODUCT_CREATION_FAILED = {'code': 'F02013', 'msg': 'Product not created.'}
    PRODUCT_ID_REQUIRED = {'code': 'F02014', 'msg': 'Product ID required.'}
    PRODUCT_ENTITY_REQUIRED = {'code': 'F02015', 'msg': 'Product Entity required.'}
    PRODUCT_AIRPORT_REQUIRED = {'code': 'F02016', 'msg': 'Product airport required.'}
    PRODUCT_SEAPORT_REQUIRED = {'code': 'F02017', 'msg': 'Product seaport required.'}
    PRODUCT_ADDRESS_REQUIRED = {'code': 'F02020', 'msg': 'Product address required.'}
