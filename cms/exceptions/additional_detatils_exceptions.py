from enum import Enum
from exceptions.base_exceptions import BaseException


class AdditionalDetailsException(BaseException):

    def getHTTPCode(self):
        return 400

class AdditionalDetailsError(Enum):
    NO_OF_SUPPLIERS_REQUIRED = {'code': 'F3101','msg': 'No of suppliers required'}
    MAXIMUM_PREFERENCE_VALIDATION={'code':'F3102','msg':'You can select only five airlines'}
    MAXIMUM_DEPREFERENCE_VALIDATION={'code':'F3103','msg':'You can depreference only five airlines'}
    ONLY_ONE_CAN_BE_SELECTED ={'code':'F3104','msg':'You can select either preference or depreference not both at the same time'}
    ONE_SHOULD_BE_SELECTED ={'code':'F3105','msg':'One should be selected either preference or depreference'}