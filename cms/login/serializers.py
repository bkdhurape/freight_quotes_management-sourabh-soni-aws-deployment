from customer.models.customer import Customer
from customer.services.customer_manage_service import CustomerManageService
from datetime import datetime, timedelta
from django.conf import settings
from django.core import serializers as dj_serializers
from django_restql.mixins import DynamicFieldsMixin
from django.utils import timezone
from login.models.jwt_token import JwtToken
from login.services.login_service import LoginService
from notification.managers.email_manager import EmailNotification
from rest_framework import serializers
from utils.base_models import StatusBase
from utils.helpers import encode_password, generate_token_data, date_difference_in_hours
from vendor.models.vendor import Vendor
import json, jwt

class JwtTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = JwtToken
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=255)
    account_type = serializers.ChoiceField(required=True, choices=['customer', 'vendor'])

    def validate(self, attrs):
        data = dict(attrs)
        error_list = []
        params = {'email': data['email'], 'password': encode_password(data['password']), 'status': StatusBase.ACTIVE}

        if 'customer' == data['account_type']:
            if Customer.objects.filter(**params).exists():
                user_object = Customer.objects.get(**params)
            else:
                error_list.append('Invalid login credential!')

        elif 'vendor' == data['account_type']:
            if Vendor.objects.filter(**params).exists():
                user_object = Vendor.objects.get(**params)
            else:
                error_list.append('Invalid login credential!')

        if not error_list:
            _request = self.context['request_object']
            account_type = _request.data['account_type']
            user_type = 'customer_type' if account_type == 'customer' else 'vendor_type'
            user_object = json.loads(dj_serializers.serialize('json', [user_object], fields=(
                'id', 'pk', 'name', 'email', 'home_company', 'is_super_admin', user_type)))[0]
            session_data = user_object['fields']
            session_data.update({'user_id': user_object['pk']})
            session_data.update({'account_type': account_type})

            if not _request.session.exists(_request.session.session_key):
                _request.session.create()
            session_id = _request.session.session_key

            # Check JWT Token data in database
            token_is_present = JwtToken.find_by(multi=True, entity_id=session_data['user_id'],
                                                entity_type=session_data['account_type'], session_id=session_id)

            if _request.session.exists(_request.session.session_key) and token_is_present:
                error_list.append('You are already login.')

        if error_list:
            raise serializers.ValidationError(error_list)

        return attrs


class LogoutSerializer(serializers.Serializer):
    def validate(self, attrs):
        _request_headers = self.context['request_headers_object']
        jwt_token_decode = jwt.decode(_request_headers['Authorization'], settings.JWT_FCT_SECRET, algorithms=['HS256'])
        result = JwtToken.objects.filter(entity_id=jwt_token_decode['user_id'],
                                         entity_type=jwt_token_decode['account_type'],
                                         session_id=jwt_token_decode['session_id'])
        if not result:
            raise serializers.ValidationError('Login required.')

        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=255)
    new_password = serializers.CharField(required=True, max_length=255)

    def validate(self, attrs):
        _request_headers = self.context['request_headers_object']
        data = dict(attrs)
        error_dict = {}
        error_list = []

        token = jwt.decode(_request_headers['Authorization'], settings.JWT_FCT_SECRET, algorithms=['HS256'],
                           options={'verify_exp': False})

        # New password must be unique
        if (data['old_password'] == data['new_password']):
            error_list.append('Entered new password must be unique, Not same as old password.')

        if 'customer' == token['account_type']:
            # Match old_password with exist password in db & only loggedin user able to change password (validation)
            old_password_is_valid = Customer.find_by(multi=True, id=token['user_id'],
                                                     password=encode_password(data['old_password']),
                                                     status=StatusBase.ACTIVE)
            if (not old_password_is_valid):
                error_dict.update({'old_password': 'You entered old password is invalid.'})

        elif 'vendor' == token['account_type']:
            # Match old_password with exist password in db & only loggedin user able to change password (validation)
            old_password_is_valid = Vendor.find_by(multi=True, id=token['user_id'],
                                                   password=encode_password(data['old_password']),
                                                   status=StatusBase.ACTIVE)
            if (not old_password_is_valid):
                error_dict.update({'old_password': 'You entered old password is invalid.'})

        else:
            error_list.append('Invalid account type.')

        if error_list:
            raise serializers.ValidationError(error_list)
        if error_dict:
            raise serializers.ValidationError(error_dict)

        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)
    account_type = serializers.ChoiceField(required=True, choices=['customer', 'vendor'])

    def validate(self, attrs):
        data = dict(attrs)
        error_list = []

        if 'customer' == data['account_type']:
            # Has valid email
            has_valid_email = Customer.find_by(multi=True, email=data['email'], status=StatusBase.ACTIVE)
            if not has_valid_email:
                error_list.append('Invalid email in request.')

            if not error_list:
                customer_detail = Customer.find_by(email=data['email'], status=StatusBase.ACTIVE)
                if customer_detail.forgot_password_link:
                    today = timezone.now()
                    hours = date_difference_in_hours(customer_detail.forgot_password_date,today)
                    
                    if not (hours > int(settings.TOKEN_EXPIRY_LIMIT)):
                        error_list.append('You already make request for forgot password. Check your email & setup password.')

        elif 'vendor' == data['account_type']:
            # Has valid email
            has_valid_email = Vendor.find_by(multi=True, email=data['email'], status=StatusBase.ACTIVE)
            if not has_valid_email:
                error_list.append('Invalid email in request.')
            if not error_list:
                vendor_detail = Vendor.find_by(email=data['email'], status=StatusBase.ACTIVE)
                if vendor_detail.forgot_password_link:
                    today = timezone.now()
                    hours = date_difference_in_hours(vendor_detail.forgot_password_date,today)
                    if not (hours > int(settings.TOKEN_EXPIRY_LIMIT)):
                        
                        error_list.append('You already make request for forgot password. Check your email & setup password.')

        if error_list:
            raise serializers.ValidationError(error_list)

        return attrs


class ForgotPasswordCheckLinkSerializer(serializers.Serializer):
    def validate(self, attrs):
        _link = self.context['link']
        error_list = []

        # Check link is empty, Validate link
        if not _link.strip():
            error_list.append('Invalid forgot password link.')

        # Decode link, Validate link
        result = CustomerManageService.get_customer_data_from_url_use_in_serializer('none', _link)

        if result['success']:
            user_email, user_account = result['data']['email'], result['data']['account_type']

            if 'customer' == user_account:
                # Validate token exist in DB
                token_is_exist = Customer.find_by(multi=True, forgot_password_link=_link, status=StatusBase.ACTIVE)
                if not token_is_exist:
                    error_list.append('Invalid forgot password link.')

                if not error_list:
                    customer_detail = Customer.find_by(multi=True, email=user_email, status=StatusBase.ACTIVE)
                    user_name = list(customer_detail.values_list('name', flat=True))[0]
                    customer_forgot_password_link = list(customer_detail.values_list('forgot_password_link', flat=True))[0]
                    customer_forgot_password_date = \
                    list(customer_detail.values_list('forgot_password_date', flat=True))[0]
                    if (not customer_forgot_password_link):
                        error_list.append('Your link has been expired.A new password reset link has been successfully sent to your email id, please click on the link to reset your password')
                    else:
                        today = timezone.now()
                        hours = date_difference_in_hours(customer_forgot_password_date,today)
                        if hours > int(settings.TOKEN_EXPIRY_LIMIT):
                            forgot_password_token = LoginService.update_user_forgot_password_link(customer_detail,
                                                                                                  user_email,
                                                                                                  'customer')
                            forgot_password_link = settings.FRONTEND_URL + '/forgot-password/' + forgot_password_token
                            email_data = {'user_name': user_name, 'email': user_email,
                                          'link': forgot_password_link}
                            EmailNotification.forgot_password(email_data)

                            error_list.append('Your link has been expired.A new password reset link has been successfully sent to your email id, please click on the link to reset your password')

            elif 'vendor' == user_account:
                vendor_detail = Vendor.find_by(multi=True,email=user_email, status=StatusBase.ACTIVE)
                user_name = list(vendor_detail.values_list('name', flat=True))[0]
                vendor_forgot_password_link = list(vendor_detail.values_list('forgot_password_link', flat=True))[0]
                vendor_forgot_password_date = list(vendor_detail.values_list('forgot_password_date', flat=True))[0]
                # Validate token exist in DB
                token_is_exist = Vendor.find_by(multi=True, forgot_password_link=_link, status=StatusBase.ACTIVE)
                if not token_is_exist:
                    error_list.append('Invalid forgot password link.')

                if not error_list:
                    if (not vendor_forgot_password_link):
                        error_list.append('Your link has been expired.A new password reset link has been successfully sent to your email id, please click on the link to reset your password')
                    else:
                        today = timezone.now()
                        hours = date_difference_in_hours(vendor_forgot_password_date,today)
                        if hours > int(settings.TOKEN_EXPIRY_LIMIT):
                            forgot_password_token = LoginService.update_user_forgot_password_link(vendor_detail,
                                                                                                  user_email,
                                                                                                  'vendor')
                            forgot_password_link = settings.FRONTEND_URL + '/forgot-password/' + forgot_password_token
                            email_data = {'user_name': user_name, 'email': user_email,
                                          'link': forgot_password_link}
                            EmailNotification.forgot_password(email_data)

                            error_list.append('Your link has been expired.A new Password reset link has been successfully sent to your email id, please click on the link to reset your password')

            else:
                error_list.append('Invalid account type.')
        else:
            error_list.append(result['data'])

        if error_list:
            raise serializers.ValidationError(error_list)

        return attrs


class ForgotPasswordLinkSerializer(ForgotPasswordCheckLinkSerializer):
    new_password = serializers.CharField(required=True, max_length=255)
