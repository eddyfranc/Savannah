from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from .models import Customer

class MyOIDCBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        """
        Create a Customer from OIDC claims.
        claims is a dict returned by the provider (contains email, name, sub, etc).
        """
        user = Customer.objects.create(
            username=claims.get("preferred_username") or claims.get("email").split("@")[0],
            email=claims.get("email", ""),
            first_name=claims.get("given_name", ""),
            last_name=claims.get("family_name", ""),
        )
        # You can store extra claims (e.g., phone) if present
        phone = claims.get("phone_number")
        if phone:
            user.phone = phone
            user.save()
        return user

    def filter_users_by_claims(self, claims):
        """Return existing user(s) matching claims, so we don't create duplicates."""
        email = claims.get("email")
        if not email:
            return Customer.objects.none()
        return Customer.objects.filter(email__iexact=email)
