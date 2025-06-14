"""models.py
Package containing the models for the travel listings application.
This module defines the data structures used in the application, including
listings, users, bookings, and reviews.
"""

import os
from enum import Enum
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from dotenv import load_dotenv

# Create your models here.
load_dotenv()


class User(AbstractUser):
    """
    Model representing a user profile.
    """

    user_id = models.UUIDField(
        primary_key=True, unique=True, null=False, editable=False, default=uuid4
    )
    email = models.EmailField(unique=True)

    # Add related_name to avoid conflicts with default User model
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="listings_user_set",
        related_query_name="listings_user",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="listings_user_set",
        related_query_name="listings_user",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Remove username from required fields since email is the username field

    @property
    def name(self):
        """
        Returns the full name of the user.
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.user_id} - {self.name}, Email: {self.email}"

    def clean(self):
        """
        Custom clean method to ensure password meets complexity requirements.
        """
        if not self.password:
            self.set_password(os.getenv("DEFAULT_PASSWORD"))

    class Meta:
        """
        Meta class for the User model.
        This class defines the database table name and verbose names.
        """

        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]


class Listing(models.Model):
    """
    Model representing a travel listing.
    """

    class ListingType(Enum):
        """Enum representing the type of listing.
        This enum defines the different types of properties that can be listed."""

    listings = models.Manager()

    listing_id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField()
    listing_type = models.CharField(
        max_length=50,
        choices=[
            ("HOUSE", "House"),
            ("VILLA", "Villa"),
            ("TOWNHOUSE", "Townhouse"),
            ("LOFT", "Loft"),
            ("STUDIO", "Studio"),
            ("MANSION", "Mansion"),
            ("CASTLE", "Castle"),
            ("FARMHOUSE", "Farmhouse"),
            ("RESORT", "Resort"),
            ("CHALET", "Chalet"),
            ("APARTMENT", "Apartment"),
            ("TENT", "Tent"),
            ("TREEHOUSE", "Treehouse"),
            ("YURT", "Yurt"),
            ("BOAT", "Boat"),
            ("CARAVAN", "Caravan"),
            ("TRAILER", "Trailer"),
            ("SHACK", "Shack"),
            ("HUT", "Hut"),
            ("COTTAGE", "Cottage"),
            ("BUNGALOW", "Bungalow"),
            ("PENTHOUSE", "Penthouse"),
        ],
        default="APARTMENT",
        help_text="Type of the listing, e.g., House, Villa, Apartment, etc.",
    )
    price_per_night = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    location_address = models.CharField(max_length=255, blank=False, null=False)
    allowable_guests = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    number_of_bedrooms = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    number_of_bathrooms = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    amenities = models.JSONField(default=list, blank=True, null=True)
    host = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings_host"
    )
    available_from = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for the Listing model.
        This class defines the ordering and verbose name for the model.
        """

        ordering = ["-created_at"]
        verbose_name = "Travel Listing"
        verbose_name_plural = "Travel Listings"
        db_table = "travel_listings"

    def __str__(self):
        """
        String representation of the Listing model.
        Returns a string containing the title, price per night, and creation date.
        """

        return (
            f"{self.title} - {self.price_per_night} USD, Created at: {self.created_at}"
        )


class Booking(models.Model):
    """
    Model representing a booking for a travel listing.
    """

    bookings = models.Manager()

    booking_id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="booking_listing"
    )
    booked_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookings_person"
    )
    number_of_guests = models.PositiveIntegerField(
        default=0,
        help_text="Number of guests for the booking.",
    )
    booking_status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("CONFIRMED", "Confirmed"),
            ("CANCELLED", "Cancelled"),
        ],
        default="PENDING",
    )
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount_due = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )

    class Meta:
        """
        Meta class for the Booking model.
        This class defines the ordering and verbose name for the model.
        """

        ordering = ["-created_at"]
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        db_table = "travel_bookings"

    def clean(self):
        """
        Populate amount due.
        """
        self.amount_due = self.calculate_amount_due()

    def calculate_amount_due(self):
        """
        Calculate the amount due for the booking based on the listing's price per night
        and the duration of the stay.
        """
        if self.listing and self.check_in_date and self.check_out_date:
            duration = (self.check_out_date - self.check_in_date).days

            if duration > 0:
                return duration * float(self.listing.price_per_night)
            raise ValueError("End date must be after start date.")

        raise ValueError("Listing, start date, and end date must be set.")

    def __str__(self):
        return f"Booking for {self.listing.title} by {self.booked_by.name} from {self.check_in_date} to {self.check_out_date}"


class Review(models.Model):
    """
    Model representing a review for a travel listing.
    """

    reviews = models.Manager()
    review_id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="reviews_listing"
    )
    reviewed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews_person"
    )
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.listing.title} by {self.reviewed_by.name}"
