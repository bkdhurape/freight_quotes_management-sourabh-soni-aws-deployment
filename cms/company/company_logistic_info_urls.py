from company.api.v1.company_logistic_info import CompanyLogisticInfoView, CompanyLogisticInfoDetailView
from django.urls import path


urlpatterns = [

    path('', CompanyLogisticInfoView.as_view()),
    path('<int:company_logistic_id>/', CompanyLogisticInfoDetailView.as_view())
]
