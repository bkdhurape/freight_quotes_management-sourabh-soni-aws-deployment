from django.urls import path,re_path
from entity.api.v1.entity_view import EntityView, EntityDetailView

urlpatterns = [
    path('', EntityView.as_view()),
    path('<int:id>/', EntityDetailView.as_view())
]
