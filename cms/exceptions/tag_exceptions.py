from enum import Enum
from exceptions.base_exceptions import BaseException


class TagException(BaseException):

    def getHTTPCode(self):
        return 400

class TagError(Enum):
    TAG_NOT_FOUND = {'code': 'F0301','msg': 'Tag not found'}

    TAG_EXISTS = {'code': 'F0302','msg': 'Tag name already exists'}
    TAG_CREATION_FAILED = {'code': 'F0303', 'msg': 'Tag not created'}
    