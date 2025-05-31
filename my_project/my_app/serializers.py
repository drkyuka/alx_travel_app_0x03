"""serializers.py
This module defines serializers for the Book model in the Django application.
It uses Django REST Framework to convert model instances to JSON format and vice versa.
"""

from datetime import date
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model."""

    def create(self, validated_data):
        """Create a new Book instance."""
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update an existing Book instance."""
        instance.title = validated_data.get("title", instance.title)
        instance.author = validated_data.get("author", instance.author)
        instance.published_date = validated_data.get(
            "published_date", instance.published_date
        )
        instance.save()
        return instance

    class Meta:
        """
        Meta class for BookSerializer.
        """

        model = Book
        fields = "__all__"

    days_since_created = serializers.SerializerMethodField(
        read_only=True, method_name="get_days_since_created"
    )

    def get_days_since_created(self, obj):
        """
        Calculate the number of days since the book was created.
        """
        if obj.published_date:
            return (date.today() - obj.published_date).days
        return 0
