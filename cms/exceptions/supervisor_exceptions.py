from enum import Enum
from .base_exceptions import BaseException


class SupervisorException(BaseException):

    def getHTTPCode(self):
        return 400


class SupervisorError(Enum):
    SUPERVISOR_NOT_FOUND = {'code': 'F0121', 'msg': 'Supervisor not found.'}
    SUPERVISOR_EXISTS = {'code': 'F0122', 'msg': 'Supervisor name already exists.'}
    SUPERVISOR_CREATION_FAILED = {'code': 'F0123', 'msg': 'Supervisor not created.'}
    SUPERVISOR_ID_REQUIRED = {'code': 'F0124', 'msg': 'Supervisor ID required.'}
