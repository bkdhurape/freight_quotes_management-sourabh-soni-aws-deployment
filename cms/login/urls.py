from django.urls import path,re_path
from login.api.v1.login_view import login, logout, change_password, forgot_password, forgot_password_check_link, forgot_password_link

urlpatterns = [
    path('login/', login),
    path('logout/', logout),
    path('change-password/', change_password),
    path('forgot-password/', forgot_password),
    path('forgot-password-check/<str:link>', forgot_password_check_link),
    path('forgot-password/<str:link>', forgot_password_link),
]
