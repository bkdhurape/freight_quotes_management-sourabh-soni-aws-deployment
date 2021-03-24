from django.core.exceptions import ObjectDoesNotExist
from exceptions.login_exceptions import LoginError, LoginException
from freight.freight_manager import FreightManager


class JwtTokenManager(FreightManager):
    """JWT Token Data manager used for doing db operation."""

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise LoginException(LoginError.JWT_TOKEN_NOT_FOUND)
