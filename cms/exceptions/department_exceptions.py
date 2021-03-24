from enum import Enum
from exceptions.base_exceptions import BaseException


class DepartmentException(BaseException):

    def getHTTPCode(self):
        return 400

class DepartmentError(Enum):
    DEPARTMENT_NOT_FOUND = {'code': 'F0201','msg': 'Department not found'}

    DEPARTMENT_EXISTS = {'code': 'F0202','msg': 'Department name already exists'}
    DEPARTMENT_CREATION_FAILED = {'code': 'F0203', 'msg': 'Department not created'}
    DEPARTMENT_ACTIVATED = {'code': 'F0204', 'msg': 'Department activates successfully'}
