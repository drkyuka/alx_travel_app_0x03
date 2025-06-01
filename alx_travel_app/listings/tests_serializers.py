"""
Tests for serializers in the listings app.
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import Booking, Listing, Review, User
from .serializers import (
    BookingSerializer,
    ListingSerializer,
    ReviewSerializer,
    UserSerializer,
)


class UserSerializerTestCase(TestCase):
    """Tests for the UserSerializer."""

    def setUp(self):
        """Set up test data."""
        self.user_data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "date_of_birth": timezone.now() - timedelta(days=365 * 30),  # 30 years ago
        }
        self.user = User.objects.create(**self.user_data)
        self.serializer = UserSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            [
                "user_id",
                "email",
                "first_name",
                "last_name",
                "date_of_birth",
                "created_at",
                "updated_at",
            ],
        )


class ListingSerializerTestCase(TestCase):
    """Tests for the ListingSerializer."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create(
            email="host@example.com",
            first_name="Host",
            last_name="User",
            date_of_birth=timezone.now() - timedelta(days=365 * 30),
        )
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
        self.serializer = ListingSerializer(instance=self.listing)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            [
                "listing_id",
                "title",
                "description",
                "listing_type",
                "price_per_night",
                "location_address",
                "allowable_guests",
                "number_of_bedrooms",
                "number_of_bathrooms",
                "amenities",
                "host",
                "reviews",
                "bookings",
                "available_from",
                "created_at",
                "updated_at",
                "rating",
            ],
        )


class BookingSerializerTestCase(TestCase):
    """Tests for the BookingSerializer."""

    def setUp(self):
        """Set up test data."""
        self.host = User.objects.create(
            email="host@example.com",
            first_name="Host",
            last_name="User",
            date_of_birth=timezone.now() - timedelta(days=365 * 30),
        )
        self.guest = User.objects.create(
            email="guest@example.com",
            first_name="Guest",
            last_name="User",
            date_of_birth=timezone.now() - timedelta(days=365 * 25),
        )
        self.listing = Listing.objects.create(
            title="Test Listing",
            description="A test listing",
            listing_type="APARTMENT",
            price_per_night=100.00,
            location_address="123 Test St",
            allowable_guests=4,
            number_of_bedrooms=2,
            number_of_bathrooms=1,
            amenities=["wifi", "parking"],
            host=self.host,
            available_from=timezone.now(),
        )
        self.booking_data = {
            "listing": self.listing,
            "booked_by": self.guest,
            "number_of_guests": 2,
            "booking_status": "PENDING",
            "check_in_date": timezone.now() + timedelta(days=5),
            "check_out_date": timezone.now() + timedelta(days=10),
            "amount_due": 500.00,
        }
        self.booking = Booking.objects.create(**self.booking_data)
        self.serializer = BookingSerializer(instance=self.booking)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            [
                "booking_id",
                "listing",
                "booked_by",
                "number_of_guests",
                "booking_status",
                "check_in_date",
                "check_out_date",
                "created_at",
                "updated_at",
                "amount_due",
            ],
        )

    def test_validate_dates(self):
        """Test that check_out_date must be after check_in_date."""
        check_in = timezone.now() + timedelta(days=5)
        check_out = check_in - timedelta(days=1)  # Earlier than check-in
        invalid_data = {
            "listing": self.listing.listing_id,
            "booked_by": self.guest.user_id,
            "number_of_guests": 2,
            "booking_status": "PENDING",
            "check_in_date": check_in,
            "check_out_date": check_out,
        }
        serializer = BookingSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_guests(self):
        """Test that number_of_guests must not exceed allowable_guests."""
        invalid_data = {
            "listing": self.listing.listing_id,
            "booked_by": self.guest.user_id,
            "number_of_guests": self.listing.allowable_guests + 1,  # Too many guests
            "booking_status": "PENDING",
            "check_in_date": timezone.now() + timedelta(days=5),
            "check_out_date": timezone.now() + timedelta(days=10),
        }
        serializer = BookingSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class ReviewSerializerTestCase(TestCase):
    """Tests for the ReviewSerializer."""

    def setUp(self):
        """Set up test data."""
        self.host = User.objects.create(
            email="host@example.com",
            first_name="Host",
            last_name="User",
            date_of_birth=timezone.now() - timedelta(days=365 * 30),
        )
        self.reviewer = User.objects.create(
            email="reviewer@example.com",
            first_name="Reviewer",
            last_name="User",
            date_of_birth=timezone.now() - timedelta(days=365 * 25),
        )
        self.listing = Listing.objects.create(
            title="Test Listing",
            description="A test listing",
            listing_type="APARTMENT",
            price_per_night=100.00,
            location_address="123 Test St",
            allowable_guests=4,
            number_of_bedrooms=2,
            number_of_bathrooms=1,
            amenities=["wifi", "parking"],
            host=self.host,
            available_from=timezone.now(),
        )
        self.review_data = {
            "listing": self.listing,
            "reviewed_by": self.reviewer,
            "rating": 4,
            "comment": "Great place!",
        }
        self.review = Review.objects.create(**self.review_data)
        self.serializer = ReviewSerializer(instance=self.review)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            [
                "review_id",
                "listing",
                "reviewed_by",
                "rating",
                "comment",
                "created_at",
                "updated_at",
            ],
        )

    def test_validate_rating(self):
        """Test that rating must be between 1 and 5."""
        # Test with rating too low
        invalid_data = {
            "listing": self.listing.listing_id,
            "reviewed_by": self.reviewer.user_id,
            "rating": 0,
            "comment": "Bad place!",
        }
        serializer = ReviewSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

        # Test with rating too high
        invalid_data["rating"] = 6
        serializer = ReviewSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class ComprehensiveSerializerTestCase(TestCase):
    """Tests for comprehensive serializer validation including nested relationships."""

    def setUp(self):
        """Set up test data with full relationships."""
        # Create host and guest users
        self.host = User.objects.create(
            email="host@example.com",
            first_name="Host",
            last_name="User",
            date_of_birth=timezone.now() - timedelta(days=365 * 30),
        )
        self.guest = User.objects.create(
            email="guest@example.com",
            first_name="Guest",
            last_name="User",
            date_of_birth=timezone.now() - timedelta(days=365 * 25),
        )

        # Create a listing
        self.listing = Listing.objects.create(
            title="Comprehensive Test Listing",
            description="A test listing for comprehensive testing",
            listing_type="APARTMENT",
            price_per_night=150.00,
            location_address="123 Test St",
            allowable_guests=4,
            number_of_bedrooms=2,
            number_of_bathrooms=1,
            amenities=["wifi", "parking", "pool"],
            host=self.host,
            available_from=timezone.now(),
        )

        # Create a booking
        self.booking = Booking.objects.create(
            listing=self.listing,
            booked_by=self.guest,
            number_of_guests=2,
            booking_status="CONFIRMED",
            check_in_date=timezone.now() + timedelta(days=10),
            check_out_date=timezone.now() + timedelta(days=15),
            amount_due=750.00,
        )

        # Create a review
        self.review = Review.objects.create(
            listing=self.listing,
            reviewed_by=self.guest,
            rating=5,
            comment="Excellent place! Would stay again.",
        )

    def test_full_listing_serialization(self):
        """Test that a listing with related bookings and reviews serializes correctly."""
        serializer = ListingSerializer(instance=self.listing)
        data = serializer.data

        # Check that main listing fields are present
        self.assertEqual(data["title"], self.listing.title)
        self.assertEqual(data["description"], self.listing.description)
        self.assertEqual(data["listing_type"], self.listing.listing_type)
        self.assertEqual(
            float(data["price_per_night"]), float(self.listing.price_per_night)
        )

        # Check that related data is present
        self.assertEqual(data["host"]["email"], self.host.email)
        self.assertEqual(len(data["reviews"]), 1)
        self.assertEqual(data["reviews"][0]["rating"], self.review.rating)
        self.assertEqual(data["reviews"][0]["comment"], self.review.comment)

        # Verify bookings relation is present
        self.assertEqual(len(data["bookings"]), 1)
        self.assertEqual(
            data["bookings"][0]["booking_status"], self.booking.booking_status
        )

        # Check calculated fields
        self.assertEqual(data["rating"], 5.0)

    def test_booking_serialization_with_validation(self):
        """Test booking serialization with validation checks."""
        # Valid booking data
        valid_data = {
            "listing": self.listing.listing_id,
            "user_id": self.guest.user_id,
            "number_of_guests": 3,
            "booking_status": "PENDING",
            "check_in_date": timezone.now() + timedelta(days=20),
            "check_out_date": timezone.now() + timedelta(days=25),
        }

        serializer = BookingSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

        # Invalid booking - too many guests
        invalid_data = valid_data.copy()
        invalid_data["number_of_guests"] = 10  # More than allowable_guests

        serializer = BookingSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Number of guests cannot exceed", str(serializer.errors))

        # Invalid booking - invalid date range
        invalid_data = valid_data.copy()
        invalid_data["check_out_date"] = invalid_data["check_in_date"] - timedelta(
            days=1
        )

        serializer = BookingSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "Check-out date must be after check-in date", str(serializer.errors)
        )
