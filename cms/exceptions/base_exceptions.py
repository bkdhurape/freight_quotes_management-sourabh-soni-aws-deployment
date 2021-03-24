from enum import Enum

class BaseException(Exception):
    DEFAULTCODE = 99999

    def getHTTPCode():
        return 400


    def __init__(self, code='', message='', *args, **kwargs):
        if isinstance(code, Enum):
            self.error_msg = message or code.value.get('msg', '')
            self.error_code = code.value.get('code', self.DEFAULTCODE)

            try:
                self.error_msg = self.error_msg.format(*args, **kwargs)
            except (IndexError, KeyError):
                pass
        else:
            self.error_code = code or self.DEFAULTCODE
            self.error_msg = message

        try:
            msg = '[{0}] {1}'.format(
                self.error_code, self.error_msg.format(*args, **kwargs))
        except (IndexError, KeyError):
            msg = '[{0}] {1}'.format(self.error_code, self.error_msg)

        super().__init__(msg)

    def to_dict(self):
        return {'code': self.error_code, 'message': self.error_msg, 'data': {}, 'status': 'error'}
