from . import api_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CategoryViewSet, ProductViewSet, OrderViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    path("protected/", api_views.ProtectedHello.as_view(), name="api-protected"),
    path("", include(router.urls)),
]






