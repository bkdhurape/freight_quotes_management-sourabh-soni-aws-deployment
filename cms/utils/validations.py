from exceptions import BadRequestException, BadRequestError
from utils.dial_code import DialCode
from django.core.exceptions import ValidationError


class ContactNumberValidation:

    @staticmethod
    def validate_contact_no(value):
        """
            Validate contact no. If not valid then it raise Validation error.
        :return: None
        """
        if value and not value.isdigit():
            raise ValidationError('Invalid contact no.')
