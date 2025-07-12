"""views.py
# Package containing the views for the travel listings application.
# This module defines the API endpoints for managing listings, users, bookings, and reviews.
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Listing, User, Booking, Review, Payment
from .serializers import (
    ListingSerializer,
    UserSerializer,
    BookingSerializer,
    ReviewSerializer,
    PaymentSerializer,
)

# Create your views here.


class ListingViewSet(ModelViewSet):
    """
    A viewset for viewing and editing listing instances.
    """

    # Assuming you have a Listing model and a ListingSerializer
    # queryset = Listing.objects.all()
    # serializer_class = ListingSerializer

    serializer_class = ListingSerializer
    authentication_classes = [JWTAuthentication]
    queryset = Listing.listings.all()


class UserViewSet(ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    # Assuming you have a User model and a UserSerializer
    # queryset = User.objects.all()
    # serializer_class = UserSerializer

    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()


class BookingViewSet(ModelViewSet):
    """
    A viewset for viewing and editing booking instances.
    """

    # Assuming you have a Booking model and a BookingSerializer
    # queryset = Booking.objects.all()
    # serializer_class = BookingSerializer

    serializer_class = BookingSerializer
    authentication_classes = [JWTAuthentication]
    queryset = Booking.bookings.all()


class ReviewViewSet(ModelViewSet):
    """
    A viewset for viewing and editing review instances.
    """

    # Assuming you have a Review model and a ReviewSerializer
    # queryset = Review.objects.all()
    # serializer_class = ReviewSerializer

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = Review.reviews.all()


class PaymentViewSet(ModelViewSet):
    """
    A viewset for viewing and editing payment instances.
    """

    # Assuming you have a Payment model and a PaymentSerializer
    # queryset = Payment.objects.all()
    # serializer_class = PaymentSerializer

    serializer_class = PaymentSerializer
    authentication_classes = [JWTAuthentication]
    queryset = Payment.payments.all()
