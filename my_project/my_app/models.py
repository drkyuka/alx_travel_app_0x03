"""models.py
This module defines the Book model for the Django application.
It represents a book in the library with fields for title, author, and published date.
"""

from django.db import models


# Create your models here.
class Book(models.Model):
    """Model representing a book in the library."""

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
