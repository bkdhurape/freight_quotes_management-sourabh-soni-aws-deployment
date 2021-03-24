from django.urls import path,re_path
from vendor.api.v1.vendor_type_view import VendorTypeView, VendorTypeDetailView

urlpatterns = [
    path('', VendorTypeView.as_view()),
    path('<int:id>/', VendorTypeDetailView.as_view())
]
