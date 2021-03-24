from enum import Enum
from exceptions.base_exceptions import BaseException


class CompanyException(BaseException):

    def getHTTPCode(self):
        return 400


class CompanyError(Enum):
    COMPANY_NOT_FOUND = {'code': 'F0001', 'msg': 'Company not found'}
    COMPANY_EXISTS = {'code': 'F0002', 'msg': 'Company name already exists'}
    COMPANY_CREATION_FAILED = {'code': 'F0003', 'msg': 'Company not created'}
    COMPANY_INDUSTRY_IS_REQUIRED = {
        'code': 'F0004', 'msg': 'Company Industry field is required'}
    COMPANY_BUSINNESS_ACTIVITY_IS_REQUIRED = {
        'code': 'F0005', 'msg': 'Business activity field is required'}
    COMPANY_INDUSTRY_OTHER_MUST_BE_EMPTY = {
        'code': 'F0006', 'msg': 'Industry other field must be empty'}
    COMPANY_BUSINNESS_ACTIVITY_OTHER_MUST_BE_EMPTY = {
        'code': 'F0007', 'msg': 'Business activity other field must be empty'}
    GST_IS_REQURIED = {'code': 'F0008', 'msg': 'gst is required'}

    PAN_IS_REQURIED = {'code': 'F0009', 'msg': 'pan is required'}
    CIN_IS_REQURIED = {'code': 'F0010', 'msg': 'cin is required'}
    IEC_IS_REQURIED = {'code': 'F0011', 'msg': 'iec is required'}
    