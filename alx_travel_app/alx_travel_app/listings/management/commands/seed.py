"""
Management command to seed the database with sample data.

This script creates sample users, listings, bookings, and reviews
for the ALX Travel App. It provides realistic data for each model,
including different property types, booking statuses, and reviews
with varied ratings.
"""

import datetime
import random

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

try:
    from faker import Faker

    fake = Faker()
except ImportError:
    raise ImportError(
        "The Faker package is required. Install it with 'pip install faker'"
    )

from alx_travel_app.listings.models import Booking, Listing, Review, User


class Command(BaseCommand):
    """Command to seed the database with sample data."""

    help = "Seeds the database with sample data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        """
        Handle the command to seed the database.
        This creates users, listings, bookings, and reviews.
        """
        self.stdout.write("Seeding database...")

        # Delete all existing data to avoid duplicates
        self.stdout.write("Deleting existing data...")
        Booking.objects.all().delete()
        Review.objects.all().delete()
        Listing.objects.all().delete()
        User.objects.all().delete()

        # Create sample users
        self.stdout.write("Creating sample users...")
        users = self._create_users(20)  # Create 20 users

        # Create sample listings
        self.stdout.write("Creating sample listings...")
        listings = self._create_listings(users, 50)  # Create 50 listings

        # Create sample bookings
        self.stdout.write("Creating sample bookings...")
        bookings = self._create_bookings(users, listings, 100)  # Create 100 bookings

        # Create sample reviews
        self.stdout.write("Creating sample reviews...")
        self._create_reviews(users, listings, 150)  # Create 150 reviews

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded database with:\n"
                f"- {len(users)} users\n"
                f"- {len(listings)} listings\n"
                f"- {len(bookings)} bookings\n"
                f"- {Review.objects.count()} reviews"
            )
        )

    def _create_users(self, count):
        """Create sample users."""
        users = []
        for _ in range(count):
            dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
            dob_datetime = datetime.datetime.combine(
                dob, datetime.time.min, tzinfo=timezone.get_current_timezone()
            )

            user = User.objects.create(
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                date_of_birth=dob_datetime,
            )
            users.append(user)
        return users

    def _create_listings(self, users, count):
        """Create sample listings of various property types."""
        listings = []
        property_types = [
            "HOUSE",
            "VILLA",
            "TOWNHOUSE",
            "LOFT",
            "STUDIO",
            "MANSION",
            "CASTLE",
            "FARMHOUSE",
            "RESORT",
            "CHALET",
            "APARTMENT",
            "TENT",
            "TREEHOUSE",
            "YURT",
            "BOAT",
            "CARAVAN",
            "TRAILER",
            "SHACK",
            "HUT",
            "COTTAGE",
            "BUNGALOW",
            "PENTHOUSE",
        ]

        amenities_options = [
            "Wi-Fi",
            "Air conditioning",
            "Kitchen",
            "Washer",
            "Dryer",
            "TV",
            "Pool",
            "Hot tub",
            "Free parking",
            "Gym",
            "Breakfast",
            "Elevator",
            "Heating",
            "Laptop-friendly workspace",
            "Iron",
            "Hair dryer",
            "BBQ grill",
            "Fire pit",
            "Beach access",
            "Mountain view",
            "Security cameras",
            "Smoke alarm",
            "Carbon monoxide alarm",
        ]

        # Ensure we create at least one listing of each property type
        for property_type in property_types:
            host = random.choice(users)
            amenities = random.sample(amenities_options, k=random.randint(3, 10))

            # Set available date to a random date in the future (up to 1 year)
            available_from = timezone.now() + datetime.timedelta(
                days=random.randint(1, 30)
            )

            listing = Listing.objects.create(
                title=f"{fake.catch_phrase()} {property_type.capitalize()}",
                description=fake.paragraph(nb_sentences=5),
                listing_type=property_type,
                price_per_night=round(random.uniform(50, 1000), 2),
                location_address=fake.address(),
                allowable_guests=random.randint(1, 12),
                number_of_bedrooms=random.randint(1, 6),
                number_of_bathrooms=random.randint(1, 6),
                amenities=amenities,
                host=host,
                available_from=available_from,
            )
            listings.append(listing)

        # Create remaining random listings to reach the desired count
        for _ in range(count - len(property_types)):
            host = random.choice(users)
            property_type = random.choice(property_types)
            amenities = random.sample(amenities_options, k=random.randint(3, 10))

            # Set available date to a random date in the future (up to 1 year)
            available_from = timezone.now() + datetime.timedelta(
                days=random.randint(1, 30)
            )

            listing = Listing.objects.create(
                title=f"{fake.catch_phrase()} {property_type.capitalize()}",
                description=fake.paragraph(nb_sentences=5),
                listing_type=property_type,
                price_per_night=round(random.uniform(50, 1000), 2),
                location_address=fake.address(),
                allowable_guests=random.randint(1, 12),
                number_of_bedrooms=random.randint(1, 6),
                number_of_bathrooms=random.randint(1, 6),
                amenities=amenities,
                host=host,
                available_from=available_from,
            )
            listings.append(listing)

        return listings

    def _create_bookings(self, users, listings, count):
        """Create sample bookings with different confirmation statuses."""
        bookings = []
        statuses = ["PENDING", "CONFIRMED", "CANCELLED"]

        # Ensure at least one booking of each status type
        for status in statuses:
            user = random.choice(users)
            listing = random.choice(listings)

            # Ensure the user is not the host
            while user == listing.host:
                user = random.choice(users)

            # Set dates in the future, starting from the listing's available date
            check_in = listing.available_from + datetime.timedelta(
                days=random.randint(1, 90)
            )
            check_out = check_in + datetime.timedelta(days=random.randint(1, 14))

            guests = random.randint(1, min(listing.allowable_guests, 10))

            # Calculate amount due based on dates and price
            duration = (check_out - check_in).days
            amount_due = float(listing.price_per_night) * duration

            booking = Booking.objects.create(
                listing=listing,
                booked_by=user,
                number_of_guests=guests,
                booking_status=status,
                check_in_date=check_in,
                check_out_date=check_out,
                amount_due=amount_due,
            )
            bookings.append(booking)

        # Create remaining random bookings
        for _ in range(count - len(statuses)):
            user = random.choice(users)
            listing = random.choice(listings)

            # Ensure the user is not the host
            while user == listing.host:
                user = random.choice(users)

            # Set dates in the future, starting from the listing's available date
            check_in = listing.available_from + datetime.timedelta(
                days=random.randint(1, 90)
            )
            check_out = check_in + datetime.timedelta(days=random.randint(1, 14))

            guests = random.randint(1, min(listing.allowable_guests, 10))
            status = random.choice(statuses)

            # Calculate amount due based on dates and price
            duration = (check_out - check_in).days
            amount_due = float(listing.price_per_night) * duration

            booking = Booking.objects.create(
                listing=listing,
                booked_by=user,
                number_of_guests=guests,
                booking_status=status,
                check_in_date=check_in,
                check_out_date=check_out,
                amount_due=amount_due,
            )
            bookings.append(booking)

        return bookings

    def _create_reviews(self, users, listings, count):
        """Create sample reviews with varied ratings."""
        reviews = []

        # Create at least one review with each rating (1-5)
        for rating in range(1, 6):
            user = random.choice(users)
            listing = random.choice(listings)

            # Ensure the user is not the host
            while user == listing.host:
                user = random.choice(users)

            review = Review.objects.create(
                listing=listing,
                reviewed_by=user,
                rating=rating,
                comment=fake.paragraph(nb_sentences=3),
            )
            reviews.append(review)

        # Create remaining random reviews
        for _ in range(count - 5):
            user = random.choice(users)
            listing = random.choice(listings)

            # Ensure the user is not the host
            while user == listing.host:
                user = random.choice(users)

            rating = random.randint(1, 5)

            review = Review.objects.create(
                listing=listing,
                reviewed_by=user,
                rating=rating,
                comment=fake.paragraph(nb_sentences=3),
            )
            reviews.append(review)

        return reviews
