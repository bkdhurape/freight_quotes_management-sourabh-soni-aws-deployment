from enum import Enum
from exceptions.base_exceptions import BaseException


class QuoteException(BaseException):

    def getHTTPCode(self):
        return 400


class QuoteError(Enum):
    QUOTE_NOT_FOUND = {'code': 'F3001', 'msg': 'Quote not found'}
    PICKUP_LOCATION_REQUIRED = {'code': 'F3002', 'msg': 'pickup_location is required'}
    PICKUP_AIR_PORT_REQUIRED = {'code': 'F3003', 'msg': 'pickup_air_port is required'}
    PICKUP_SEA_PORT_REQUIRED = {'code': 'F3004', 'msg': 'pickup_sea_port is required'}
    DROP_LOCATION_REQUIRED = {'code': 'F3005', 'msg': 'drop_location is required'}
    DROP_AIR_PORT_REQUIRED = {'code': 'F3006', 'msg': 'drop_air_port is required'}
    DROP_SEA_PORT_REQUIRED = {'code': 'F3007', 'msg': 'drop_sea_port is required'}
    COURIER_TYPE_REQUIRED = {'code': 'F3008', 'msg': 'For Air_courier, personal_courier or commercial_courier is required'}
    EXPECTED_ARRIVAL_DATE_REQUIRED = {'code':'F3009', 'msg':'Arrival date is required'}
    EXPECTED_DELIVERY_DATE_REQUIRED = {'code':'F3010', 'msg':'Expected delivery date is required'}
    TRANSPORT_MODE_REQUIRED = {'code':'F3011', 'msg':'Transport mode required'}