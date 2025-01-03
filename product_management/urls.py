from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductView, ProductDetailView, DiscountView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
  path('', include(router.urls)),
  path('products/', ProductView.as_view(), name='product-list'),
  path('products/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
  path('discounts/', DiscountView.as_view(), name='discount-create')
]