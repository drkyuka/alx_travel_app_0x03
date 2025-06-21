#!/usr/bin/env python
"""
Script to verify that all viewsets work accurately.
This script will test all the CRUD operations for each viewset.
"""

import os
import sys
from datetime import datetime, timedelta

import requests

# Get the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1/"

# Headers for the requests
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def print_success(message):
    """Print a success message."""
    print(f"{GREEN}[SUCCESS] {message}{RESET}")


def print_error(message):
    """Print an error message."""
    print(f"{RED}[ERROR] {message}{RESET}")


def print_info(message):
    """Print an info message."""
    print(f"{YELLOW}[INFO] {message}{RESET}")


def get_token(email, password):
    """Get a JWT token for authentication."""
    url = f"{BASE_URL}token/"
    data = {"email": email, "password": password}

    try:
        response = requests.post(url, json=data, headers=HEADERS)
        response.raise_for_status()
        return response.json()["access"]
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to get token: {e}")
        print_info(
            f"Response: {response.text if 'response' in locals() else 'No response'}"
        )
        return None


def test_user_viewset():
    """Test the UserViewSet."""
    print_info("\n--- Testing UserViewSet ---")

    # Create a new user
    url = f"{BASE_URL}users/"
    email = f"test_{datetime.now().timestamp()}@example.com"
    user_data = {
        "email": email,
        "password": "Password123!",
        "first_name": "Test",
        "last_name": "User",
    }

    try:
        # Create user
        response = requests.post(url, json=user_data, headers=HEADERS)
        response.raise_for_status()
        user_id = response.json()["user_id"]
        print_success(f"Created user with ID: {user_id}")

        # Get user
        response = requests.get(f"{url}{user_id}/", headers=HEADERS)
        response.raise_for_status()
        print_success(f"Retrieved user: {response.json()['email']}")

        # Get all users
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        print_success(f"Retrieved {len(response.json())} users")

        # Update user
        update_data = {"first_name": "Updated", "last_name": "Name"}
        response = requests.patch(f"{url}{user_id}/", json=update_data, headers=HEADERS)
        response.raise_for_status()
        print_success(
            f"Updated user: {response.json()['first_name']} {response.json()['last_name']}"
        )

        # Delete user
        response = requests.delete(f"{url}{user_id}/", headers=HEADERS)
        response.raise_for_status()
        print_success(f"Deleted user with ID: {user_id}")

        return True
    except requests.exceptions.RequestException as e:
        print_error(f"Error testing UserViewSet: {e}")
        print_info(
            f"Response: {response.text if 'response' in locals() else 'No response'}"
        )
        return False


def test_listing_viewset(token):
    """Test the ListingViewSet."""
    print_info("\n--- Testing ListingViewSet ---")

    # Add token to headers
    auth_headers = HEADERS.copy()
    auth_headers["Authorization"] = f"Bearer {token}"

    # Create a new listing
    url = f"{BASE_URL}listings/"
    listing_data = {
        "title": f"Test Listing {datetime.now().timestamp()}",
        "description": "A test listing created by the verification script",
        "listing_type": "APARTMENT",
        "price_per_night": 100.00,
        "location_address": "123 Test St",
        "allowable_guests": 4,
        "number_of_bedrooms": 2,
        "number_of_bathrooms": 1,
        "amenities": ["wifi", "parking"],
        "available_from": (datetime.now() + timedelta(days=1)).isoformat(),
    }

    try:
        # Create listing
        response = requests.post(url, json=listing_data, headers=auth_headers)
        response.raise_for_status()
        listing_id = response.json()["listing_id"]
        print_success(f"Created listing with ID: {listing_id}")

        # Get listing
        response = requests.get(f"{url}{listing_id}/", headers=auth_headers)
        response.raise_for_status()
        print_success(f"Retrieved listing: {response.json()['title']}")

        # Get all listings
        response = requests.get(url, headers=auth_headers)
        response.raise_for_status()
        print_success(f"Retrieved {len(response.json())} listings")

        # Update listing
        update_data = {
            "title": f"Updated Listing {datetime.now().timestamp()}",
            "price_per_night": 120.00,
        }
        response = requests.patch(
            f"{url}{listing_id}/", json=update_data, headers=auth_headers
        )
        response.raise_for_status()
        print_success(f"Updated listing: {response.json()['title']}")

        # Delete listing
        response = requests.delete(f"{url}{listing_id}/", headers=auth_headers)
        response.raise_for_status()
        print_success(f"Deleted listing with ID: {listing_id}")

        return True
    except requests.exceptions.RequestException as e:
        print_error(f"Error testing ListingViewSet: {e}")
        print_info(
            f"Response: {response.text if 'response' in locals() else 'No response'}"
        )
        return False


def test_booking_viewset(token):
    """Test the BookingViewSet."""
    print_info("\n--- Testing BookingViewSet ---")

    # Add token to headers
    auth_headers = HEADERS.copy()
    auth_headers["Authorization"] = f"Bearer {token}"

    # First, we need a listing to book
    url = f"{BASE_URL}listings/"
    listing_data = {
        "title": f"Test Listing for Booking {datetime.now().timestamp()}",
        "description": "A test listing created for booking",
        "listing_type": "APARTMENT",
        "price_per_night": 100.00,
        "location_address": "123 Test St",
        "allowable_guests": 4,
        "number_of_bedrooms": 2,
        "number_of_bathrooms": 1,
        "amenities": ["wifi", "parking"],
        "available_from": (datetime.now() + timedelta(days=1)).isoformat(),
    }

    try:
        # Create listing
        response = requests.post(url, json=listing_data, headers=auth_headers)
        response.raise_for_status()
        listing_id = response.json()["listing_id"]
        print_success(f"Created listing with ID: {listing_id} for booking test")

        # Create a booking
        url = f"{BASE_URL}bookings/"
        booking_data = {
            "listing": listing_id,
            "check_in_date": (datetime.now() + timedelta(days=10)).isoformat(),
            "check_out_date": (datetime.now() + timedelta(days=15)).isoformat(),
            "total_guests": 2,
        }

        # Create booking
        response = requests.post(url, json=booking_data, headers=auth_headers)
        response.raise_for_status()
        booking_id = response.json()["booking_id"]
        print_success(f"Created booking with ID: {booking_id}")

        # Get booking
        response = requests.get(f"{url}{booking_id}/", headers=auth_headers)
        response.raise_for_status()
        print_success(f"Retrieved booking for listing: {response.json()['listing']}")

        # Get all bookings
        response = requests.get(url, headers=auth_headers)
        response.raise_for_status()
        print_success(f"Retrieved {len(response.json())} bookings")

        # Update booking
        update_data = {"total_guests": 3}
        response = requests.patch(
            f"{url}{booking_id}/", json=update_data, headers=auth_headers
        )
        response.raise_for_status()
        print_success(f"Updated booking: {response.json()['total_guests']} guests")

        # Delete booking
        response = requests.delete(f"{url}{booking_id}/", headers=auth_headers)
        response.raise_for_status()
        print_success(f"Deleted booking with ID: {booking_id}")

        # Clean up - delete the listing
        url = f"{BASE_URL}listings/{listing_id}/"
        response = requests.delete(url, headers=auth_headers)
        response.raise_for_status()
        print_success(f"Cleaned up - deleted listing with ID: {listing_id}")

        return True
    except requests.exceptions.RequestException as e:
        print_error(f"Error testing BookingViewSet: {e}")
        print_info(
            f"Response: {response.text if 'response' in locals() else 'No response'}"
        )
        return False


def test_review_viewset(token):
    """Test the ReviewViewSet."""
    print_info("\n--- Testing ReviewViewSet ---")

    # Add token to headers
    auth_headers = HEADERS.copy()
    auth_headers["Authorization"] = f"Bearer {token}"

    # First, we need a listing to review
    url = f"{BASE_URL}listings/"
    listing_data = {
        "title": f"Test Listing for Review {datetime.now().timestamp()}",
        "description": "A test listing created for review",
        "listing_type": "APARTMENT",
        "price_per_night": 100.00,
        "location_address": "123 Test St",
        "allowable_guests": 4,
        "number_of_bedrooms": 2,
        "number_of_bathrooms": 1,
        "amenities": ["wifi", "parking"],
        "available_from": (datetime.now() + timedelta(days=1)).isoformat(),
    }

    try:
        # Create listing
        response = requests.post(url, json=listing_data, headers=auth_headers)
        response.raise_for_status()
        listing_id = response.json()["listing_id"]
        print_success(f"Created listing with ID: {listing_id} for review test")

        # Create a review
        url = f"{BASE_URL}reviews/"
        review_data = {
            "listing": listing_id,
            "rating": 4,
            "comment": "Great place to stay!",
        }

        # Create review
        response = requests.post(url, json=review_data, headers=auth_headers)
        response.raise_for_status()
        review_id = response.json()["review_id"]
        print_success(f"Created review with ID: {review_id}")

        # Get review
        response = requests.get(f"{url}{review_id}/", headers=auth_headers)
        response.raise_for_status()
        print_success(f"Retrieved review with rating: {response.json()['rating']}")

        # Get all reviews
        response = requests.get(url, headers=auth_headers)
        response.raise_for_status()
        print_success(f"Retrieved {len(response.json())} reviews")

        # Update review
        update_data = {"rating": 5, "comment": "Amazing place to stay!"}
        response = requests.patch(
            f"{url}{review_id}/", json=update_data, headers=auth_headers
        )
        response.raise_for_status()
        print_success(
            f"Updated review: {response.json()['rating']} stars - {response.json()['comment']}"
        )

        # Delete review
        response = requests.delete(f"{url}{review_id}/", headers=auth_headers)
        response.raise_for_status()
        print_success(f"Deleted review with ID: {review_id}")

        # Clean up - delete the listing
        url = f"{BASE_URL}listings/{listing_id}/"
        response = requests.delete(url, headers=auth_headers)
        response.raise_for_status()
        print_success(f"Cleaned up - deleted listing with ID: {listing_id}")

        return True
    except requests.exceptions.RequestException as e:
        print_error(f"Error testing ReviewViewSet: {e}")
        print_info(
            f"Response: {response.text if 'response' in locals() else 'No response'}"
        )
        return False


def main():
    """Main function to run all tests."""
    print_info("Starting verification of all viewsets...")

    # Test user creation (this doesn't require a token)
    user_success = test_user_viewset()

    # Create a user to get a token for the other tests
    email = f"admin_{datetime.now().timestamp()}@example.com"
    password = "AdminPassword123!"

    # Create admin user
    url = f"{BASE_URL}users/"
    user_data = {
        "email": email,
        "password": password,
        "first_name": "Admin",
        "last_name": "User",
        "is_staff": True,
        "is_superuser": True,
    }

    try:
        response = requests.post(url, json=user_data, headers=HEADERS)
        response.raise_for_status()
        print_success(f"Created admin user: {email}")

        # Get token
        token = get_token(email, password)
        if not token:
            print_error("Failed to get token, cannot continue with other tests")
            return

        # Test other viewsets
        listing_success = test_listing_viewset(token)
        booking_success = test_booking_viewset(token)
        review_success = test_review_viewset(token)

        # Summary
        print_info("\n--- Test Summary ---")
        print(f"UserViewSet: {'✓' if user_success else '✗'}")
        print(f"ListingViewSet: {'✓' if listing_success else '✗'}")
        print(f"BookingViewSet: {'✓' if booking_success else '✗'}")
        print(f"ReviewViewSet: {'✓' if review_success else '✗'}")

        if user_success and listing_success and booking_success and review_success:
            print_success("\nAll viewsets are working correctly! 🎉")
        else:
            print_error("\nSome viewsets have issues. Please check the logs above.")

    except requests.exceptions.RequestException as e:
        print_error(f"Error creating admin user: {e}")
        print_info(
            f"Response: {response.text if 'response' in locals() else 'No response'}"
        )


if __name__ == "__main__":
    main()
