from company.api.v1.organization import OrganizationView, OrganizationDetailView
from django.urls import path


urlpatterns = [

    path('', OrganizationView.as_view()),
    path('<int:id>/company/', OrganizationDetailView.as_view())
]
