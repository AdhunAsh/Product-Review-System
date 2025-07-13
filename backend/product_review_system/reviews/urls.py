from django.urls import path
from .views import ReviewListCreateView

urlpatterns = [
    path('<int:product_id>/reviews/', ReviewListCreateView.as_view(), name='product-reviews')
]
