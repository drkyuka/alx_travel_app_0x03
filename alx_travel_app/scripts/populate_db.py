#!/usr/bin/env python
"""
Script to populate the database with sample data for testing.
Creates:
- 19 Users
- 12 Listings
- 30 Bookings
- 51 Reviews
"""

import os
import random
import sys
from datetime import timedelta

import django
import faker

# Setup Django environment
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_travel_app.settings")
django.setup()

from django.utils import timezone
from listings.models import Booking, Listing, Review, User

# Initialize faker
fake = faker.Faker()

# Constants
NUM_USERS = 19
NUM_LISTINGS = 12
NUM_BOOKINGS = 30
NUM_REVIEWS = 51

# Listing types
LISTING_TYPES = [
    "APARTMENT",
    "HOUSE",
    "CONDO",
    "VILLA",
    "CABIN",
    "COTTAGE",
    "TOWNHOUSE",
    "HOTEL",
    "RESORT",
    "HOSTEL",
]

# Amenities
AMENITIES = [
    "wifi",
    "tv",
    "kitchen",
    "washer",
    "dryer",
    "air_conditioning",
    "heating",
    "dedicated_workspace",
    "pool",
    "hot_tub",
    "free_parking",
    "gym",
    "bbq_grill",
    "fire_pit",
    "indoor_fireplace",
    "breakfast",
    "smoking_allowed",
    "pets_allowed",
    "security_cameras",
]


def create_users(count):
    """Create and save a specified number of users."""
    print(f"Creating {count} users...")
    users = []
    email = "admin@example.com"

    # Create one admin user
    admin_user = User.objects.create_user(
        email=email,
        username=email,
        password="AdminPass123!",
        first_name="Admin",
        last_name="User",
        is_staff=True,
        is_superuser=True,
    )
    users.append(admin_user)
    print(f"Created admin user: {admin_user.email}")

    # Create regular users
    for i in range(1, count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"

        user = User.objects.create_user(
            email=email,
            username=email,
            password="Password123!",
            first_name=first_name,
            last_name=last_name,
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=80),
        )
        users.append(user)
        print(f"Created user: {user.email}")

    return users


def create_listings(count, users):
    """Create and save a specified number of listings."""
    print(f"\nCreating {count} listings...")
    listings = []

    for i in range(count):
        # Get a random host from users
        host = random.choice(users)

        # Generate a random date in the future
        available_from = timezone.now() + timedelta(days=random.randint(1, 30))

        # Generate random amenities (3-10)
        amenities = random.sample(AMENITIES, random.randint(3, min(10, len(AMENITIES))))

        # Create listing
        listing = Listing.objects.create(
            title=fake.sentence(nb_words=4)[:-1],  # Remove period at end
            description=fake.paragraph(nb_sentences=5),
            listing_type=random.choice(LISTING_TYPES),
            price_per_night=round(random.uniform(50, 500), 2),
            location_address=fake.address(),
            allowable_guests=random.randint(1, 10),
            number_of_bedrooms=random.randint(1, 5),
            number_of_bathrooms=random.randint(1, 4),
            amenities=amenities,
            host=host,
            available_from=available_from,
        )
        listings.append(listing)
        print(f"Created listing: {listing.title}")

    return listings


def create_bookings(count, users, listings):
    """Create and save a specified number of bookings."""
    print(f"\nCreating {count} bookings...")
    bookings = []

    for i in range(count):
        # Get a random guest and listing
        guest = random.choice(users)
        listing = random.choice(listings)

        # Make sure guest is not the host
        while guest == listing.host:
            guest = random.choice(users)

        # Generate random dates
        start_date = listing.available_from + timedelta(days=random.randint(1, 60))
        end_date = start_date + timedelta(days=random.randint(1, 14))

        # Calculate total price
        duration = (end_date - start_date).days
        total_price = listing.price_per_night * duration

        # Create booking
        booking = Booking.objects.create(
            guest=guest,
            listing=listing,
            check_in_date=start_date,
            check_out_date=end_date,
            total_guests=random.randint(1, listing.allowable_guests),
            total_price=total_price,
            booking_status="CONFIRMED" if random.random() > 0.2 else "PENDING",
        )
        bookings.append(booking)
        print(
            f"Created booking: {booking.booking_id} - {guest.email} booked {listing.title}"
        )

    return bookings


def create_reviews(count, users, listings):
    """Create and save a specified number of reviews."""
    print(f"\nCreating {count} reviews...")
    reviews = []

    for i in range(count):
        # Get a random reviewer and listing
        reviewer = random.choice(users)
        listing = random.choice(listings)

        # Make sure reviewer is not the host
        while reviewer == listing.host:
            reviewer = random.choice(users)

        # Generate a rating between 1 and 5
        rating = random.randint(1, 5)

        # Generate appropriate comment based on rating
        if rating >= 4:
            comment = fake.paragraph(nb_sentences=random.randint(1, 3))
        elif rating == 3:
            comment = "It was okay. " + fake.sentence()
        else:
            comment = "Disappointing. " + fake.sentence()

        # Create review
        review = Review.objects.create(
            reviewer=reviewer,
            listing=listing,
            rating=rating,
            comment=comment,
        )
        reviews.append(review)
        print(f"Created review: {reviewer.email} rated {listing.title} {rating}/5")

    return reviews


def main():
    """Main function to populate the database."""
    print("Starting database population script...")

    # Check if data already exists
    if User.objects.count() > 0:
        confirm = input(
            "Database already has data. Do you want to continue and add more? (y/n): "
        )
        if confirm.lower() != "y":
            print("Operation canceled.")
            return

    try:
        # Create users
        users = create_users(NUM_USERS)

        # Create listings
        listings = create_listings(NUM_LISTINGS, users)

        # Create bookings
        bookings = create_bookings(NUM_BOOKINGS, users, listings)

        # Create reviews
        reviews = create_reviews(NUM_REVIEWS, users, listings)

        # Summary
        print("\nDatabase population completed successfully!")
        print(f"Created {len(users)} users")
        print(f"Created {len(listings)} listings")
        print(f"Created {len(bookings)} bookings")
        print(f"Created {len(reviews)} reviews")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
