from django.urls import path
from country.api.v1.country_view import CountryView, CountryDetailView

urlpatterns = [
    path('', CountryView.as_view()),
    path('<int:id>/', CountryDetailView.as_view()),
]
