"""serializers.py"""

from django.db.models import Avg
from rest_framework import serializers
from .models import Listing, User, Booking, Review


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        """Meta class for UserSerializer."""

        model = User
        fields = "__all__"
        read_only_fields = ("user_id", "created_at", "updated_at")


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.
    """

    booked_by = UserSerializer()
    amount_due = serializers.SerializerMethodField(
        method_name="get_amount_due", read_only=True
    )

    class Meta:
        """Meta class for BookingSerializer."""

        model = Booking
        fields = "__all__"
        read_only_fields = ("booking_id", "created_at", "updated_at", "amount_due")

    def validate(self, attrs):
        """
        Validate that the end date is after the start date.
        """

        # check if check_in_date and check_out_date are provided
        if "check_in_date" not in attrs or "check_out_date" not in attrs:
            raise serializers.ValidationError(
                "Both check-in date and check-out date must be provided."
            )

        # Validate that check_in_date is before check_out_date
        if attrs.get("check_in_date") >= attrs.get("check_out_date"):
            raise serializers.ValidationError(
                "Check-out date must be after check-in date."
            )

        # Check if the listing is available for the requested dates
        listing = attrs.get("listing")
        if listing:
            if Booking.objects.filter(
                listing=listing,
                booking_status="CONFIRMED",
                start_date__lt=attrs["check_out_date"],
                end_date__gt=attrs["check_in_date"],
            ).exists():
                raise serializers.ValidationError(
                    "Listing is already booked for the selected dates."
                )

        # check if the number of guests exceeds the listing's capacity
        if attrs.get("number_of_guests") and listing:
            if attrs.get("number_of_guests") > listing.allowable_guests:
                raise serializers.ValidationError(
                    f"Number of guests cannot exceed the listing's maximum capacity of {listing.max_guests}."
                )

        return attrs

    def get_amount_due(self, obj):
        """
        Calculate the amount due for the booking based
        on the listing's price per night
        and the duration of the stay.
        """
        duration = (obj.check_out_date - obj.check_in_date).days
        return duration * float(obj.listing.price_per_night)


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    """

    reviewed_by = UserSerializer(read_only=True)

    class Meta:
        """Meta class for ReviewSerializer."""

        model = Review
        fields = "__all__"
        read_only_fields = ("review_id", "created_at", "updated_at")

    def validate(self, attrs):
        """
        Validate that the rating is between 1 and 5.
        """
        if not (1 <= attrs["rating"] <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return attrs


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Listing model.
    """

    host = UserSerializer()
    reviews = ReviewSerializer(many=True, read_only=True)
    bookings = BookingSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField(method_name="get_average_rating")

    class Meta:
        """Meta class for ListingSerializer."""

        model = Listing
        fields = "__all__"
        read_only_fields = ("listing_id", "created_at", "updated_at")

    def get_average_rating(self, obj):
        """
        Calculate the average rating for the listing.
        """
        avg = obj.reviews.aggregate(avg_rating=Avg("rating"))["avg_rating"]
        return float(avg) if avg else 0.0
