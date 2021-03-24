from django.urls import path
from vendor.api.v1.vendor_view import VendorView, VendorDetailView
from vendor.api.v1.vendor_activation_view import VendorActivationView, VendorActivationResendLinkView
from vendor.api.v1.vendor_client_view import VendorClientView, VendorClientDetailView


urlpatterns = [
    path('activate/<str:token>', VendorActivationView.as_view()),
    path('send_activation_link/<str:email>', VendorActivationResendLinkView.as_view()),
    path('', VendorView.as_view()),
    path('<int:id>/', VendorDetailView.as_view()),
    path('<int:vendor_id>/clients', VendorClientView.as_view()),
    path('<int:vendor_id>/clients/<int:id>/<str:action>', VendorClientDetailView.as_view()),
]
