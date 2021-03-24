from django.urls import path

from tag.api.v1.tag_view import TagView, TagDetailView

urlpatterns = [

    path('', TagView.as_view()),
    path('<int:id>/', TagDetailView.as_view())
]
