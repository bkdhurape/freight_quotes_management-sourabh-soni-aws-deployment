from django.urls import path
from port.api.v1.port_view import PortView, PortDetailView

urlpatterns = [
    path('', PortView.as_view()),
    path('<int:id>/', PortDetailView.as_view())
]
