from contact_person.api.v1.contact_person_view import ContactPersonView , ContactPersonDetailView
from django.urls import path


urlpatterns = [
    path('', ContactPersonView.as_view()),
    path('<int:contact_person_id>/', ContactPersonDetailView.as_view()) 
    ]