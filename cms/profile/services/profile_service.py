from customer.models.customer import Customer
from customer.serializers import CustomerSerializer
from customer.services.customer_service import CustomerService
from datetime import datetime, timedelta
from django.conf import settings
from exceptions import BadRequestException, BadRequestError,CustomerException, CustomerError, VendorException, VendorError
from utils.helpers import generate_token, encode_data, encode_password, decode_data, date_diffs_in_hours, generate_token_data
from vendor.models.vendor import Vendor
from vendor.serializers import VendorSerializer
from vendor.services.vendor_service import VendorService

class ProfileService:

    def __init__(self, data):
        self.data = data
    
    # check user type retrieve user data according to type
    def check_type_and_get_user_data(email, type):
        if type == 'customer':
            user = Customer.find_by(multi=True, email=email)
            user_serializer = CustomerSerializer
            user_model = Customer
            user_service = CustomerService
            user_exception = CustomerException
            user_error = CustomerError

        if type == 'vendor':
            user = Vendor.find_by(multi=True, email=email)
            user_serializer = VendorSerializer
            user_model = Vendor
            user_service = VendorService
            user_exception = VendorException
            user_error = VendorError

        if not user:
            raise user_exception(user_error.INVALID_TOKEN_CONTACT_ADMIN)

        user_serializer = user_serializer(user, many=True)

        user_data = user_serializer.data[0]

        return user_data, user_model, user_service, user_exception, user_error

    # check the status  and retreive user data

    def get_profile_data(self, url_token_hash):
        email, type, token = self.get_user_data_from_url(url_token_hash)
        user_data, user_model, user_service, user_exception, user_error = ProfileService.check_type_and_get_user_data(
            email, type)

        if user_data['status'] == user_model.PENDING:
            if (user_data['registration_token'] != token) or (not token):
                raise user_exception(user_error.INVALID_TOKEN_RESEND_LINK)

            if (user_data['registration_token'] == token):
                response = self.validate_token(user_data, type)
                if response['status'] == 'success':
                    return {'status': 'success', 'data': user_data, 'message': 'user data retrieve successfully.'}
                else:
                    return response

        elif user_data['status'] ==user_model.ACTIVE:
            raise user_exception(user_error.ALREADY_ACTIVATED)

        return {'status': 'success'}

    # set profile and activate user
    def set_profile_data(self, url_token_hash):
        email, type, token = self.get_user_data_from_url(url_token_hash)
        user_data, user_model, user_service, user_exception, user_error = ProfileService.check_type_and_get_user_data(
            email, type)

        if email != self.data['email']:
            raise user_exception(user_error.INVALID_EMAIL)

        if (('contact_no' not in self.data or not self.data['contact_no']) and ('landline_no' not in self.data or not self.data['landline_no'])):
            raise user_exception(user_error.CONTACT_NO_OR_LANDLINE_NO_REQUIRED)

        user_data['registration_token'] = None
        user_data['token_date'] = None
        user_data['status'] = user_model.ACTIVE
        user_data['name'] = self.data['name']
        
        if 'contact_no' in self.data:
            user_data['contact_no'] = self.data['contact_no']

        if 'landline_no' in self.data:
            user_data['landline_no'] = self.data['landline_no']

        if 'landline_no_dial_code' in self.data:
            user_data['landline_no_dial_code'] = self.data['landline_no_dial_code']

        if 'password' not in self.data or self.data['password'] is None or self.data['password'] == "":
            raise user_exception(user_error.PASSWORD_IS_REQUIRED)

        if 'confirm_password' not in self.data or self.data['confirm_password'] is None or self.data['confirm_password'] == "":
            raise user_exception(user_error.CONFIRM_PASSWORD_IS_REQUIRED)

        if self.data['password'] == self.data['confirm_password']:
            self.data['password'] = encode_password(self.data['password'])
            user_data['password'] = self.data['password']
        else:
            raise user_exception(user_error.PASSWORD_DID_NOT_MATCH)
        user_service_object= user_service(data=user_data)
        user_service_object.update(user_data['id'])
        response = {'status': 'success'}

        return response

    #  Get user email and token  and type from url token
    def get_user_data_from_url(self, url_token_hash):
        try:
            decoded_token = decode_data(url_token_hash)
        except Exception as e:
            raise BadRequestException(BadRequestError.INVALID_TOKEN_CONTACT_ADMIN)
        return decoded_token.split("__")

    # Validate if user profile link expired by token date Show appropriate error if token expired and create a new link for reset profile
    def validate_token(self, user_data, type):
        today = datetime.date(datetime.utcnow())
        token_date = user_data['token_date']

        hours = date_diffs_in_hours(token_date, today)

        if hours > int(settings.TOKEN_EXPIRY_LIMIT):
            token = user_data['email'] + '__' + type
            encoded_token = encode_data(token)

            resend_link = settings.API_HOST + '/api/v1/reset_token/' + encoded_token
            response = {'message': 'Your activation link has been expired. Please click here to resend the activation link or Contact admin for any other queries.',
                        'data': resend_link, 'status': 'failure'}
        else:
            response = {'status': 'success'}

        return response

    # Resend user profile link to user by registered email
    def resend_activation_link_for_set_profile(self, token_hash):
        email, type = self.get_user_data_from_url(token_hash)

        user_data, user_model, user_service, user_exception, user_error = ProfileService.check_type_and_get_user_data(
            email, type)

        if user_data['status'] == user_model.ACTIVE:
            raise user_exception(user_error.ALREADY_ACTIVATED)

        token_hash, token = generate_token_data(email, type)
        user_data['registration_token'] = token
        user_data['token_date'] = datetime.now()

        user_service_object = user_service(data=user_data)
        user_service_object.update(user_data['id'])

        link = settings.API_HOST + '/api/v1/profile/' + token_hash
        response = {'status': 'success', 'data': link}

        return response
