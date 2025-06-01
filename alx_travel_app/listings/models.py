"""models.py
Package containing the models for the travel listings application.
This module defines the data structures used in the application, including
listings, users, bookings, and reviews.
"""

import datetime
from enum import Enum
from uuid import uuid4

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class User(models.Model):
    """
    Model representing a user profile.
    """

    user_id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    date_of_birth = models.DateTimeField(default=datetime.datetime(1900, 1, 1))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        """
        Returns the full name of the user.
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.user_id} - {self.name}, Email: {self.email}"


class Listing(models.Model):
    """
    Model representing a travel listing.
    """

    class ListingType(Enum):
        """Enum representing the type of listing.
        This enum defines the different types of properties that can be listed."""

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
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    available_from = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.title} - {self.price_per_night} USD, Created at: {self.created_at}"
        )


class Booking(models.Model):
    """
    Model representing a booking for a travel listing.
    """

    booking_id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bookings"
    )
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE)
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

    review_id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="reviews"
    )
    reviewed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.listing.title} by {self.reviewed_by.name}"
