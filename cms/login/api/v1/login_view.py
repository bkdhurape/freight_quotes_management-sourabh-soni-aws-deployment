from django.db import transaction
from login.serializers import LoginSerializer, LogoutSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, ForgotPasswordCheckLinkSerializer, ForgotPasswordLinkSerializer
from login.services.login_service import LoginService
from rest_framework import status
from rest_framework.decorators import api_view
from utils.responses import success_response, error_response


@api_view(['POST'])
@transaction.atomic
def login(request):
    serializer = LoginSerializer(data=request.data, context={'request_object': request})
    if serializer.is_valid():
        user_obj = LoginService.get_user_object(serializer.validated_data)
        token = LoginService.get_jwt_token(request, user_obj)
        result = success_response(status_code=200, status='success', message="Login successfully.", data={'token': token})
    else:
        result = error_response(data=serializer.errors)
    return result


@api_view(['GET'])
@transaction.atomic
def logout(request):
    serializer = LogoutSerializer(data=request.data, context={'request_headers_object': request.headers})
    if serializer.is_valid():
        if LoginService.user_logout(request):
            result = success_response(message="Logout successfully.")
        else:
            result = error_response(message="Logout operation failed.")
    else:
        result = error_response(data=serializer.errors)
    return result


@api_view(['PUT'])
@transaction.atomic
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request_headers_object': request.headers})
    if serializer.is_valid():
        if LoginService.change_password(serializer.validated_data, request.headers['Authorization']):
            result = success_response(message="Password changed successfully.")
        else:
            result = error_response(message="Password change operation failed.")
    else:
        result = error_response(data=serializer.errors)
    return result


@api_view(['PUT'])
@transaction.atomic
def forgot_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        if LoginService.forgot_password(serializer.validated_data):
            result = success_response(message="Password reset link has been successfully sent to your email id, please click on the link to reset your password.")
        else:
            result = error_response(message="Reset password operation has failed.")
    else:
        result = error_response(data=serializer.errors)
    return result


@api_view(['GET'])
@transaction.atomic
def forgot_password_check_link(request, link):
    serializer = ForgotPasswordCheckLinkSerializer(data=request.data, context={'link': link})
    if serializer.is_valid():
        result = success_response(message="Forgot password link is valid.")
    else:
        result = error_response(data=serializer.errors)
    return result


@api_view(['PUT'])
@transaction.atomic
def forgot_password_link(request, link):
    serializer = ForgotPasswordLinkSerializer(data=request.data, context={'link': link})
    if serializer.is_valid():
        if LoginService.forgot_password_link(serializer.validated_data, link):
            result = success_response(message="Your password updated successfully.")
        else:
            result = error_response(message='Your password updation operation failure.')
    else:
        result = error_response(data=serializer.errors)
    return result