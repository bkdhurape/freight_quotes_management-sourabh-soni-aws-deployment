from enum import Enum
from exceptions.base_exceptions import BaseException


class AddressException(BaseException):
    def getHTTPCode(self):
        return 400


class AddressError(Enum):
    ADDRESS_NOT_FOUND = {'code': 'F0701', 'msg': 'address not found'}
    STREET_IS_REQUIRED = {
        'code': 'F0702',
        'msg': ' street is required'
    }
    ADDRESS_IS_REQUIRED = {
        'code': 'F0703',
        'msg': 'address are required'
    }
    COUNTRY_CAN_NOT_BE_UPDATED ={
        'code': 'F0704',
        'msg': 'you can not edit country'
    }
    COUNTRY_NOT_FOUND = {'code': 'F0705', 'msg': 'country not found.'}
    STATE_NOT_FOUND = {'code': 'F0706', 'msg': 'state not found.'}
    CITY_NOT_FOUND = {'code': 'F0707', 'msg': 'city not found.'}
