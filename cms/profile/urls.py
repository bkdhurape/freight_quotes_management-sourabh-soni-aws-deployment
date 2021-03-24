from django.urls import path,re_path
from profile.api.v1.profile_view import Profile,ReSetProfile

urlpatterns = [
    path('profile/<str:token>',Profile.as_view()),
    path('reset_token/<str:token>',ReSetProfile.as_view()),
]
