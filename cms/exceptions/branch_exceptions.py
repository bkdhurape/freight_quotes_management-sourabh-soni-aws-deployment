from enum import Enum
from exceptions.base_exceptions import BaseException


class BranchException(BaseException):

    def getHTTPCode(self):
        return 400

class BranchError(Enum):
    BRANCH_NOT_FOUND = {'code': 'F0851','msg': 'Branch not found'}
    BRANCH_EXISTS = {'code': 'F0852','msg': 'Branch name already exists'}
    BRANCH_CREATION_FAILED = {'code': 'F0853', 'msg': 'Branch not created'}
    HEAD_BRANCH_CANT_DELETE= {'code':'F0859', 'msg':'You can not delete Head Branch'}
    MINIMUM_WEIGHT_REQUIRED = {'code':'F0860', 'msg':'Minimum weight is required'}
    MAXIMUM_WEIGHT_REQUIRED = {'code':'F0861', 'msg':'Maximum weight is required'}
    WEIGHT_UNIT_REQUIRED = {'code':'F0862', 'msg':'Weight unit is required'}
    MAXIMUM_WEIGHT_SHOULD_BE_GREATER = {'code':'F0863', 'msg':'Maximum weight should be more than minimum weight'}
    MINIMUM_RADIUS_REQUIRED = {'code':'F0864', 'msg':'Minimum radius is required'}
    MAXIMUM_RADIUS_REQUIRED = {'code':'F0865', 'msg':'Maximum radius is required'}
    RADIUS_UNIT_REQUIRED = {'code':'F0866', 'msg':'Radius unit is required'}
    MAXIMUM_RADIUS_SHOULD_BE_GREATER = {'code':'F0867', 'msg':'Maximum radius should be more than minimum radius'}