from django.urls import path
from product.api.v1.product_view import ProductView, ProductDetailView

urlpatterns = [
    path('', ProductView.as_view()),
    path('<int:id>/', ProductDetailView.as_view())
]
