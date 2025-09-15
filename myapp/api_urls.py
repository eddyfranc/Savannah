from django.urls import path
from . import api_views

urlpatterns = [
    path("protected/", api_views.ProtectedHello.as_view(), name="api-protected"),
]
