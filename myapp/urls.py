from django.contrib import admin
from django.urls import path, include
from mozilla_django_oidc import views as oidc_views
from myapp import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # OIDC login (redirect to provider)
    path("oidc/login/", oidc_views.OIDCAuthenticationRequestView.as_view(), name="oidc_auth_request"),
    # OIDC callback (provider => your app)
    path("oidc/callback/", oidc_views.OIDCAuthenticationCallbackView.as_view(), name="oidc_auth_callback"),
    # Optional: logout
    path("oidc/logout/", oidc_views.OIDCLogoutView.as_view(), name="oidc_logout"),

    # Local signup for development/testing
    path("accounts/signup/", core_views.signup_view, name="signup"),

    # Simple API example
    path("api/", include("myapp.api_urls")),  # create this file below

    # core/api_urls.py

]
