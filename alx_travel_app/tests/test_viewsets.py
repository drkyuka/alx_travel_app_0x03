"""
Tests for viewsets in the listings app.
"""

import os
import sys
from datetime import timedelta

import django


from django.urls import reverse
from django.utils import timezone

# from listings.models import Booking, Listing, Review, User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


# Setup Django environment
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_travel_app.settings")
django.setup()


from listings.models import Booking, Listing, Review, User  # noqa: E402
# Ensure the Django environment is set up correctly


class ViewsetTestCase(APITestCase):
    """Base test case for all viewset tests."""

    def setUp(self):
        """Set up test data."""
        # Create a test user
        self.user_data = {
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        }
        self.user = User.objects.create_user(**self.user_data)

        # Create a test listing
        self.listing_data = {
            "title": "Test Listing",
            "description": "A test listing",
            "listing_type": "APARTMENT",
            "price_per_night": 100.00,
            "location_address": "123 Test St",
            "allowable_guests": 4,
            "number_of_bedrooms": 2,
            "number_of_bathrooms": 1,
            "amenities": ["wifi", "parking"],
            "host": self.user,
            "available_from": timezone.now(),
        }
        self.listing = Listing.objects.create(**self.listing_data)

        # Create a test booking
        self.booking_data = {
            "guest": self.user,
            "listing": self.listing,
            "check_in_date": timezone.now() + timedelta(days=10),
            "check_out_date": timezone.now() + timedelta(days=15),
            "total_guests": 2,
        }
        self.booking = Booking.objects.create(**self.booking_data)

        # Create a test review
        self.review_data = {
            "reviewer": self.user,
            "listing": self.listing,
            "rating": 4,
            "comment": "Great place!",
        }
        self.review = Review.objects.create(**self.review_data)

        # Setup API client with authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


class UserViewsetTest(ViewsetTestCase):
    """Tests for the UserViewSet."""

    def test_list_users(self):
        """Test that users can be listed."""
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_user(self):
        """Test that a user can be created."""
        url = reverse("user-list")
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            User.objects.filter(email="newuser@example.com").exists(), True
        )

    def test_retrieve_user(self):
        """Test that a user can be retrieved."""
        url = reverse("user-detail", args=[self.user.user_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)


class ListingViewsetTest(ViewsetTestCase):
    """Tests for the ListingViewSet."""

    def test_list_listings(self):
        """Test that listings can be listed."""
        url = reverse("listing-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_listing(self):
        """Test that a listing can be created."""
        url = reverse("listing-list")
        data = {
            "title": "New Listing",
            "description": "A new test listing",
            "listing_type": "HOUSE",
            "price_per_night": 150.00,
            "location_address": "456 Test Ave",
            "allowable_guests": 6,
            "number_of_bedrooms": 3,
            "number_of_bathrooms": 2,
            "amenities": ["wifi", "pool"],
            "host": str(self.user.user_id),
            "available_from": timezone.now().isoformat(),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Listing.objects.filter(title="New Listing").exists(), True)

    def test_retrieve_listing(self):
        """Test that a listing can be retrieved."""
        url = reverse("listing-detail", args=[self.listing.listing_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.listing.title)


class BookingViewsetTest(ViewsetTestCase):
    """Tests for the BookingViewSet."""

    def test_list_bookings(self):
        """Test that bookings can be listed."""
        url = reverse("booking-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_booking(self):
        """Test that a booking can be created."""
        url = reverse("booking-list")
        data = {
            "guest": str(self.user.user_id),
            "listing": str(self.listing.listing_id),
            "check_in_date": (timezone.now() + timedelta(days=20)).isoformat(),
            "check_out_date": (timezone.now() + timedelta(days=25)).isoformat(),
            "total_guests": 3,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.filter(total_guests=3).exists(), True)

    def test_retrieve_booking(self):
        """Test that a booking can be retrieved."""
        url = reverse("booking-detail", args=[self.booking.booking_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_guests"], self.booking.total_guests)


class ReviewViewsetTest(ViewsetTestCase):
    """Tests for the ReviewViewSet."""

    def test_list_reviews(self):
        """Test that reviews can be listed."""
        url = reverse("review-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_review(self):
        """Test that a review can be created."""
        url = reverse("review-list")
        data = {
            "reviewer": str(self.user.user_id),
            "listing": str(self.listing.listing_id),
            "rating": 5,
            "comment": "Excellent stay!",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.filter(rating=5).exists(), True)

    def test_retrieve_review(self):
        """Test that a review can be retrieved."""
        url = reverse("review-detail", args=[self.review.review_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rating"], self.review.rating)


# This allows the tests to be run directly with python tests/test_viewsets.py
if __name__ == "__main__":
    from django.test.runner import DiscoverRunner

    test_runner = DiscoverRunner(verbosity=1)
    failures = test_runner.run_tests(["tests.test_viewsets"])
    sys.exit(bool(failures))
