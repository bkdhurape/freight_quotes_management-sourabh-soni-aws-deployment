from branch.models.branch import Branch
from branch.models.branch_transport_mode import BranchTransportMode
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from exceptions.branch_exceptions import BranchException, BranchError
from exceptions.branch_transport_mode_exceptions import BranchTransportModeException, BranchTransportModeError
from functools import wraps
from utils.base_models import StatusBase


def validate_branch_info(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not Branch.objects.filter(company=kwargs['company_id'], id=kwargs['branch_id'], status=StatusBase.ACTIVE).exists():
            # raise ValidationError('Id does not exists')
            raise BranchException(
                BranchError.BRANCH_NOT_FOUND)
        return function(*args, **kwargs)
    return wrapper


def validate_transport_mode_id(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not BranchTransportMode.objects.filter(branch=kwargs['branch_id'], id=kwargs['id'], status=StatusBase.ACTIVE).exists():
            raise BranchTransportModeException(
                BranchTransportModeError.BRANCH_TRANSPORT_MODE_NOT_FOUND)
        return function(*args, **kwargs)
    return wrapper



