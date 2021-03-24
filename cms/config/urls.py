"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from customer.api.v1.customer_view import create_customer
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from vendor.api.v1.vendor_view import create_vendor
from quote.api.v1.quote_view import create_duplicate_quote


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('login.urls')),
    path('api/v1/company/', include('company.urls')),
    path('api/v1/organization/', include('company.organization_urls')),
    path('api/v1/company/<int:company_id>/company_logistic_info/',
         include('company.company_logistic_info_urls')),
    path('api/v1/company/<int:company_id>/department/',
         include('department.urls')),
    path('api/v1/company/<int:company_id>/tag/', include('tag.urls')),
    path('api/v1/company/<int:company_id>/branch/', include('branch.urls')),
    path('api/v1/company/<int:company_id>/customer/', include('customer.urls')),
    path('api/v1/company/<int:company_id>/contact_person/', include('contact_person.urls')),
    path('api/v1/customer/', create_customer),
    path('api/v1/company/<int:company_id>/vendor/', include('vendor.urls')),
    path('api/v1/vendor/', create_vendor),
    path('api/v1/vendor/<str:token>', create_vendor),
    path('api/v1/vendor_type/', include('vendor.vendor_type_urls')),
    path('api/v1/', include('profile.urls')),
    path('api/v1/company/<int:company_id>/entity/', include('entity.urls')),
    path('api/v1/port/', include('port.urls')),
    path('api/v1/entity/<int:entity_id>/product/', include('product.urls')),
    path('api/v1/company/<int:company_id>/quote/', include('quote.urls')),
    path('api/v1/company/<int:company_id>/', include('quote.urls')), #working on that
    path('api/v1/company/<int:company_id>/expertise/', include('enquiry_management.urls')),
    path('api/v1/country/', include('country.urls')),
    path('api/v1/country/<int:country_id>/state/', include('state.urls')),
    path('api/v1/country/<int:country_id>/state/<int:state_id>/city/', include('city.urls')),
    path('api/v1/transport/', include('transport.urls')),
    path('api/v1/media/', include('media_management.urls')),
    path('api/v1/media/', include('company.urls')),
    path('api/v1/company/<int:company_id>/quote/<int:quote_id>/duplicate-quote/', create_duplicate_quote),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
