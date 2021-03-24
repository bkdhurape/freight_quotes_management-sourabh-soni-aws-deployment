from city.api.v1.city_view import CityView, CityDetailView
from django.urls import path


urlpatterns = [
    path('', CityView.as_view()),
    path('<int:id>/', CityDetailView.as_view()),
]
