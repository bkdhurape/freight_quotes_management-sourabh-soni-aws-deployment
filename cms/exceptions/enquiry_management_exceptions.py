from enum import Enum
from exceptions.base_exceptions import BaseException


class EnquiryManagementException(BaseException):
    def getHTTPCode(self):
        return 400


class EnquiryManagementError(Enum):
    COMPANY_EXPERTISE_NOT_FOUND = {'code': 'F0601', 'msg': 'company expertise not found'}
    COMPANY_EXPERTISE_CONTAINER_TYPE_REQUIRED = {'code': 'F0602', 'msg': ' for FCLI,FCLE,FCLTC container type is required.'}
    COMPANY_EXPERTISE_THIRD_COUNTRY = {'code': 'F0603', 'msg': 'For Third Country, from_trade_lanes and to_trade_lanes are required.'}
    COMPANY_EXPERTISE_TRADE_LANES_REQUIRED = {'code': 'F0604', 'msg': 'For AI, AE, FCLI, FCLE, LCLI, LCLE,ACI,ACE trade_lanes is required.'}
    