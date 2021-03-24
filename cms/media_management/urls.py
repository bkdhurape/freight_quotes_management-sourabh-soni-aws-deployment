from django.urls import path,re_path
from media_management.api.v1.media_management_view import MediaManagementView

urlpatterns = [
    path('customer-vendor/<int:user_id>/profile_pic_upload/', MediaManagementView.as_view())
  
]