from django.urls import path,re_path
from customer.api.v1.customer_view import CustomerView, CustomerDetailView
from customer.api.v1.customer_activation_view import CustomerActivationView, CustomerActivationResendLinkView
from customer.api.v1.invited_vendor_view import InvitedVendorView, InvitedVendorDetailView


urlpatterns = [
    path('activate/<str:token>', CustomerActivationView.as_view(), name="customer-activate"),
    path('resend/<str:email>', CustomerActivationResendLinkView.as_view()),
    path('', CustomerView.as_view()),
    path('<int:id>/', CustomerDetailView.as_view()),
    path('<int:customer_id>/clients/', InvitedVendorView.as_view()),
    path('<int:customer_id>/clients/<int:id>/', InvitedVendorDetailView.as_view()),
]
