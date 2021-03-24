from enum import Enum
from exceptions.base_exceptions import BaseException


class CargoDetailsException(BaseException):

    def getHTTPCode(self):
        return 400

class CargoDetailsError(Enum):
    QUOTE_TOTAL_WEIGHT_VOLUME_NOT_FOUND = {'code': 'F3151','msg': 'Quote total weight volume not found'}
    TOTAL_WEIGHT_REQUIRED = {'code':'F3152', 'msg':'Total weight is required'}
    TOTAL_WEIGHT_UNIT_REQUIRED = {'code':'F3153', 'msg':'Total weight unit is required'}
    TOTAL_VOLUME_REQUIRED = {'code':'F3154', 'msg':'Total volume is required'}
    TOTAL_VOLUME_UNIT_REQUIRED = {'code':'F3155', 'msg':'Total volume unit is required'}
    VOLUMETRIC_WEIGHT_REQUIRED = {'code':'F3156', 'msg':'Volumetric weight is required'}
    VOLUMETRIC_WEIGHT_UNIT_REQUIRED = {'code':'F3157', 'msg':'Volumetric weight unit is required'}


    QUOTE_ORDER_READY_NOT_FOUND = {'code': 'F3158','msg': 'Quote order ready not found'}
    QUOTE_ORDER_READY_REQUIRED = {'code': 'F3159','msg': 'Quote order ready is required'}
    QUOTE_ORDER_READY_DATE_REQUIRED = {'code': 'F3160','msg': 'Quote order ready date is required'}
    INVALID_DATE = {'code': 'F3160','msg': 'Date cannot be past date'}
    QUOTE_INVOICE_VALUE_REQUIRED = {'code': 'F3161','msg': 'Quote invoice value is required'}
    QUOTE_INVOICE_VALUE_CURRENCY_REQUIRED = {'code': 'F3162','msg': 'Quote invoice value currency is required'}
    QUOTE_HANDOVER_DATE_REQUIRED = {'code': 'F3163','msg': 'Handover date is required'}
    CANNOT_UPDATE_QUOTE_ORDER_READY = {'code': 'F3164','msg': 'Cannot update cargo details with invalid id'}
    QUOTE_ORDER_READY_ID_REQUIRED = {'code': 'F3165','msg': 'Cargo details id is required'}
