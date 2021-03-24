from enum import Enum
from exceptions.base_exceptions import BaseException


class BranchTransportModeException(BaseException):

    def getHTTPCode(self):
        return 400

class BranchTransportModeError(Enum):
    BRANCH_TRANSPORT_MODE_NOT_FOUND = {'code': 'F0854','msg': 'Branch transport mode not found'}
    BRANCH_EXISTS = {'code': 'F0855','msg': 'Branch name already exists'}
    BRANCH_CREATION_FAILED = {'code': 'F0856', 'msg': 'Branch not created'}
    BRANCH_FCL_CONTAINER_TYPE_REQUIRED = {'code': 'F0857', 'msg': 'For FCLI and FCLE, container type can\'t be empty.'}
    BRANCH_CONTAINER_NOT_REQUIRED = {'code': 'F0858', 'msg': 'For AI , AE, LCLI and LCLE container type should be empty.'}
    BRANCH_THIRD_COUNTRY = {'code': 'F0860', 'msg': 'For Third Country, from_trade_lanes and to_trade_lanes are required.'}
    BRANCH_TRADE_LANES_REQUIRED = {'code': 'F0861', 'msg': 'For AI, AE, FCLI, FCLE, LCLI, LCLE trade_lanes is required.'}
    