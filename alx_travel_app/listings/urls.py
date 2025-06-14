"""urls.py
# This file defines the URL patterns for the listings application.
# It maps URLs to their corresponding viewsets for listings, bookings, users, and reviews.
"""

from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .routers import router

urlpatterns = [
    path("", include(router.urls)),
    # JWT Token endpoints
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
