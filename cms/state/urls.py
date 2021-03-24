from django.urls import path
from state.api.v1.state_view import StateView, StateDetailView

urlpatterns = [
    path('', StateView.as_view()),
    path('<int:id>/', StateDetailView.as_view()),
]
