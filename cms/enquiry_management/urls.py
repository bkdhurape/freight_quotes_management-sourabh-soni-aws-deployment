from django.urls import path 
from enquiry_management.api.v1.company_expertise_view import  CompanyExpertiseView,CompanyExpertiseDetailView

urlpatterns = [
    path('', CompanyExpertiseView.as_view()),
    path('<int:expertise_id>/', CompanyExpertiseDetailView.as_view()),
]