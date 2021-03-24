from company.models.company import Company
from customer.models.customer import Customer
from customer.services.customer_manage_service import CustomerManageService
from datetime import datetime, timedelta
from django.contrib.auth import logout
from django.conf import settings
from django.core import serializers
from exceptions.login_exceptions import LoginError, LoginException
from login.models.jwt_token import JwtToken
from utils.base_models import StatusBase
from utils.helpers import encode_password, generate_token_data
from vendor.models.vendor import Vendor
import copy, json, jwt
from notification.managers.email_manager import EmailNotification

class LoginService:

    def get_user_object(request_data):
        request_data['password'] = encode_password(request_data['password'])
        params = copy.deepcopy(request_data)
        params.pop('account_type')
        if 'customer' == request_data['account_type']:
            user_obj = Customer.objects.get(**params)
        elif 'vendor' == request_data['account_type']:
            user_obj = Vendor.objects.get(**params)
        return user_obj


    def get_jwt_token(request, user_object):
        account_type = request.data['account_type']
        session_expire = int(datetime.timestamp(datetime.now() + timedelta(days=1)))
        user_type = 'customer_type' if account_type == 'customer' else 'vendor_type'
        user_object = json.loads(serializers.serialize('json', [user_object], fields=(
        'id', 'pk', 'name', 'email', 'home_company', 'is_super_admin', user_type)))[0]
        session_data = user_object['fields']
        session_data.update({'user_id': user_object['pk']})
        session_data.update({'account_type': account_type})
        organization_id = list(
            Company.find_by(multi=True, id=session_data['home_company'], status=StatusBase.ACTIVE).values_list(
                'organization', flat=True))[0]
        session_data.update({'organization_id': organization_id})
        if not request.session.exists(request.session.session_key):
            request.session.create()
        session_id = request.session.session_key

        jwt_token_raw_data = {'user_id': user_object['pk'], 'name': session_data['name'],
                              'email': session_data['email'], 'account_type': account_type,
                              'home_company': session_data['home_company'], 'organization_id': organization_id,
                              'is_super_admin': session_data['is_super_admin'], 'user_type': session_data[user_type],
                              'session_id': session_id, 'exp': session_expire}
        jwt_token = jwt.encode(jwt_token_raw_data, settings.JWT_FCT_SECRET, algorithm='HS256')
        jwt_token = jwt_token.decode("utf-8")
        session_data.update({'jwt_token': jwt_token})

        request_jwt_token_data = {
            'entity_id': session_data['user_id'],
            'entity_type': session_data['account_type'],
            'token_key': jwt_token,
            'token_value': session_data,
            'session_id': session_id,
            'expire_timestamp': session_expire
        }

        JwtToken.objects.create(**request_jwt_token_data)
        return jwt_token


    # Logout the user
    def user_logout(request):
        jwt_token_decode = jwt.decode(request.headers['Authorization'], settings.JWT_FCT_SECRET, algorithms=['HS256'])
        result = JwtToken.objects.filter(entity_id=jwt_token_decode['user_id'], entity_type=jwt_token_decode['account_type'], session_id=jwt_token_decode['session_id'])
        if result:
            logout(request)
            result.delete()
            flag = True
        else:
            flag = False
        return flag


    # Change password
    def change_password(request_data, token):
        token = jwt.decode(token, settings.JWT_FCT_SECRET, algorithms=['HS256'], options={'verify_exp': False})

        if 'customer' == token['account_type']:
            # Update Customer with new password
            customer_detail = Customer.find_by(id=token['user_id'], status=StatusBase.ACTIVE)
            customer_detail.password = encode_password(request_data['new_password'])
            customer_detail.save()
            return True

        elif 'vendor' == token['account_type']:
            # Update Vendor with new password
            vendor_detail = Vendor.find_by(id=token['user_id'], status=StatusBase.ACTIVE)
            vendor_detail.password = encode_password(request_data['new_password'])
            vendor_detail.save()
            return True


    # User forgot password
    def forgot_password(request_data):
        if 'customer' == request_data['account_type']:
            customer_object = Customer.find_by(multi=True, email=request_data['email'], status=StatusBase.ACTIVE)
            user_name = list(customer_object.values_list('name', flat=True))[0]
            forgot_password_token = LoginService.update_user_forgot_password_link(customer_object, request_data['email'], 'customer')
            
        elif 'vendor' == request_data['account_type']:
            vendor_object = Vendor.find_by(multi=True, email=request_data['email'], status=StatusBase.ACTIVE)
            user_name = list(vendor_object.values_list('name', flat=True))[0]
            forgot_password_token = LoginService.update_user_forgot_password_link(vendor_object, request_data['email'], 'vendor')

        forgot_password_link = settings.FRONTEND_URL + '/forgot-password/' + forgot_password_token

        email_data = {'user_name':user_name, 'email':request_data['email'], 'link':forgot_password_link}
        EmailNotification.forgot_password(email_data)
        return settings.FRONTEND_URL + '/forgot-password/' + forgot_password_token


    # Update User forgot password link & date
    def update_user_forgot_password_link(user_query_set, email, account_type):
        forgot_password_link, token = generate_token_data(email, account_type)
        params = {
            'forgot_password_link': forgot_password_link,
            'forgot_password_date': datetime.now()
        }
        user_query_set.update(**params)
        return forgot_password_link


# User click on forgot password link
    def forgot_password_link(request_data, link):
        result = False

        # Decode link, Validate link 
        user_email, user_account  = CustomerManageService.get_customer_data_from_url('none', link)

        params = {
            'password': encode_password(request_data['new_password']),
            'forgot_password_link': None,
            'forgot_password_date': None
        }

        if ('customer' == user_account):
            customer_is_update = Customer.objects.filter(email=user_email, status=StatusBase.ACTIVE).update(**params)
            result = True if customer_is_update else False

        elif 'vendor' == user_account:
            vendor_is_update = Vendor.objects.filter(email=user_email, status=StatusBase.ACTIVE).update(**params)
            result = True if vendor_is_update else False

        return result
