from django.urls import path
from transport.api.v1.transport_view import TransportView, TransportDetailView

urlpatterns = [
    path('', TransportView.as_view()),
    path('<int:id>/', TransportDetailView.as_view()),
]
