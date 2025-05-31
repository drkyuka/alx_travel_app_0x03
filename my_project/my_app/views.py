"""views.py
Views for the Book model in the Django application.
This module defines API views for listing and creating books using Django REST Framework.
"""

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


class BookListCreateAPIView(generics.ListCreateAPIView):
    """API view to list and create books."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
