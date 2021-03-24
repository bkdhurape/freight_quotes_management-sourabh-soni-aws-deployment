from datetime import datetime, timedelta
from django.conf import settings
from customer.models.customer import Customer
from vendor.models.vendor import Vendor
from rest_framework import status
from django.utils import timezone
from notification.managers.email_manager import EmailNotification
from profile.serializers import CustomerSerializer, VendorSerializer
from utils.responses import success_response,error_response
from rest_framework import status
from exceptions import BadRequestException, BadRequestError, CustomerException, CustomerError, VendorException, \
    VendorError
from utils.helpers import generate_token, encode_data, encode_password, decode_data, date_difference_in_hours, \
    generate_token_data


class ProfileValidation:

    #  Get user email and token  and type from url token
    def get_user_data_from_url(url_token_hash):
        try:
            decoded_token = decode_data(url_token_hash)
        except Exception as e:
            raise BadRequestException(
                BadRequestError.INVALID_TOKEN_CONTACT_ADMIN)
        return decoded_token.split("__")

    # Validate if user profile link expired by token date Show appropriate error if token expired and create a new
    # link for reset profile
    def validate_token_expiry(user_data, user_type, errors):
        today = timezone.now()
        token_date = user_data.token_date
        hours = date_difference_in_hours(token_date, today)
        if hours > int(settings.TOKEN_EXPIRY_LIMIT):
            email_data = ProfileValidation.get_user_email_data(user_data, user_type)
            EmailNotification.set_profile_email(email_data)
            return errors.update({settings.REST_FRAMEWORK['NON_FIELD_ERROR_KEY']: "Your link has been expired. A new "
                                                                                  "set profile link has been "
                                                                                  "successfully sent to your "
                                                                                  "registered email id"})
        else:
            return True

    def validate_token_with_status(user, user_type, user_model, token, errors):
        if user.status == user_model.PENDING:
            if str(user.registration_token) != token or not token:
                errors.update(
                    {settings.REST_FRAMEWORK['NON_FIELD_ERROR_KEY']:['invalid token']})

            if (str(user.registration_token == token)):
                ProfileValidation.validate_token_expiry(
                    user, user_type, errors)

        elif user.status == user_model.ACTIVE:
            return success_response(message='you are already activated,please login to continue.',status_code = status.HTTP_201_CREATED)

        if errors:
            return error_response(data=errors)


    def check_user_type(user_type):
        if user_type == 'customer':
            user_serializer = CustomerSerializer
            user_model = Customer

        if user_type == 'vendor':
            user_serializer = VendorSerializer
            user_model = Vendor

        return user_model, user_serializer

    def get_user_email_data(user_data, user_type):

        email_data = {}

        token_hash, token = generate_token_data(user_data.email, user_type)
        user_model, user_serializer = ProfileValidation.check_user_type(user_type)
        user_object = user_model.objects.get(email=user_data.email)

        data = {'registration_token': token, 'token_date': datetime.now()}
        serializer = user_serializer(user_object, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            email_data = {
                'customer_name': user_object.name,
                'customer_email': user_data.email,
                'link': settings.FRONTEND_URL + '/set-profile/' + token_hash,
            }

        return email_data
