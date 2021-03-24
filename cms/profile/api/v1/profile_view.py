from django.db import transaction
from profile.validation.validation import ProfileValidation
from datetime import datetime
from utils.helpers import encode_password,generate_token_data
from django.conf import settings
from rest_framework import generics
from utils.responses import success_response, error_response
from notification.managers.email_manager import EmailNotification


class Profile(generics.GenericAPIView):

    # token verification and get data
    def get(self, request, token):
        email, user_type, token = ProfileValidation.get_user_data_from_url(token)
        user_model,user_serializer, = ProfileValidation.check_user_type(user_type)
        user = user_model.objects.filter(email=email).first()
        if not user:
            return error_response(data=['invalid User'])
        errors={}
        response = ProfileValidation.validate_token_with_status(user,user_type,user_model,token,errors)
        if response:
            return response
        user_serializer = user_serializer(user,exclude=['password','confirm_password'])
        user_data = user_serializer.data
        return success_response(message='User Details retrieve successfully.', data = user_data)

    @transaction.atomic
    # set profile and activate user
    def put(self, request, token):
        email, user_type, token = ProfileValidation.get_user_data_from_url(token)
        user_model,user_serializer, = ProfileValidation.check_user_type(user_type)

        user_object = user_model.objects.get(email=email)
        serializer = user_serializer(user_object,data=request.data,exclude=['email'])
        if serializer.is_valid():
            data = serializer.validated_data

            data['registration_token'] = None
            data['token_date'] = None
            data['status'] = user_model.ACTIVE
            data['password'] = encode_password(data['password'])
            serializer.save()
            return success_response(message='Your Profile Details saved successfully,please Login to continue', data=None)
        return error_response(data=serializer.errors)


class ReSetProfile(generics.GenericAPIView):

    def get(self, request, token):
        email, user_type = ProfileValidation.get_user_data_from_url(token)
        user_model,user_serializer = ProfileValidation.check_user_type(user_type)

        user_object = user_model.objects.get(email=email)

        if user_object.status == user_model.ACTIVE:
            return success_response(data='you are already activated.please login to continue')
           
        token_hash, token = generate_token_data(email, user_type)
        data = {'registration_token': token, 'token_date': datetime.now()}
        serializer = user_serializer(user_object,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            email_data = {
                'customer_name': user_object.name,
                'customer_email': email,
                'link': settings.FRONTEND_URL + '/set-profile/' + token_hash,
            }
            EmailNotification.set_profile_email(email_data)
            return success_response(message='We have sent you an email to your registered email-id, open it up to set your profile', data=None)
        return error_response(data=serializer.errors)
