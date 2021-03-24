from enum import Enum
from exceptions.base_exceptions import BaseException


class LoginException(BaseException):

    def getHTTPCode(self):
        return 400


class LoginError(Enum):
    LOGIN_EMAIL_OR_PASSWORD_REQUIRED = {'code': 'F0501', 'msg': 'Email & password required.'}
    LOGIN_INVALID_ACCOUNT_TYPE = {'code': 'F0502', 'msg': 'Invalid account type.'}
    LOGIN_INVALID_EMAIL_OR_PASSWORD = {'code': 'F0503', 'msg': 'Invalid login credential.'}
    JWT_TOKEN_NOT_FOUND = {'code': 'F0504', 'msg': 'JWT Token not found.'}
    LOGIN_REQUIRED = {'code': 'F0505', 'msg': 'Login required.'}
    USER_ALREADY_LOGIN = {'code': 'F0506', 'msg': 'You are already login.'}
    USER_OLD_NEW_PASSWORD_REQUIRED = {'code': 'F0507', 'msg': 'Old or new password required.'}
    USER_OLD_PASSWORD_INVALID = {'code': 'F0508', 'msg': 'You entered old password is invalid.'}
    USER_FORGOT_PASSWORD_PARAMS_REQUIRED = {'code': 'F0509', 'msg': 'Invalid forgot password request.'}
    USER_INVALID_EMAIL = {'code': 'F0510', 'msg': 'Invalid email in request.'}
    USER_ALREADY_PROCEED_FOR_FORGOT_PASSWORD = {'code': 'F0511', 'msg': 'You already make request for forgot password. Check your email & setup password.'}
    USER_FORGOT_PASSWORD_LINK_EXPIRE = {'code': 'F0512', 'msg': 'Your link has been expire. Processed again for forgot password process.'}
    USER_FORGOT_PASSWORD_LINK_INVALID = {'code': 'F0513', 'msg': 'Invalid forgot password link.'}
    USER_NEW_PASSWORD_INVALID = {'code': 'F0514', 'msg': 'Entered password can\'t be null or empty.'}
    USER_NEW_PASSWORD_UNIQUE = {'code': 'F0515', 'msg': 'Entered new password must be unique, Not same as old password.'}
