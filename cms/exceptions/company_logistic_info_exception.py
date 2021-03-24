from enum import Enum
from exceptions.base_exceptions import BaseException

class CompanyLogisticInfoException(BaseException):

    def getHTTPCode(self):
        return 400

class CompanyLogisticInfoError(Enum):
    COMPANY_LOGISTIC_INFO_CREATION_FAILED = {'code': 'F0083', 'msg': 'Company logistic info not created'}
    COMPANY_REQUIRED = {'code': 'F0082', 'msg': 'Company required '}
    COMPANY_LOGISTIC_INFO_NOT_FOUND={'code': 'F0084', 'msg': 'Company logistic information not found'}
    
