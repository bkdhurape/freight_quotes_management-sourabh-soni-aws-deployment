from exceptions import CustomerException, CustomerError
from utils.dial_code import DialCode
import re


class CustomerValidation:
    
    # Validate customer multiple contact no
    def validate_contact_no(contact_no_params):
        dial_codes_values = DialCode.get_dial_code()
        for iteration in contact_no_params:
            if ((not iteration['dial_code']) or (not iteration['contact_no']) or (not iteration['dial_code'] in dial_codes_values) or (not type(iteration['contact_no']) is int)):
                raise CustomerException(CustomerError.CUSTOMER_INVALID_CONTACT_NO)