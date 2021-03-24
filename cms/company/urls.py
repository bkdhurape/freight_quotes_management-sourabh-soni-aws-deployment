from django.urls import path
from company.api.v1.company import CompanyView, CompanyDetailView
from company.api.v1.company_logo import CompanyLogo

urlpatterns = [
    path('', CompanyView.as_view()),
    path('<int:company_id>/', CompanyDetailView.as_view()),
    path('company/<int:company_id>/company_logo/',CompanyLogo.as_view()),
]
