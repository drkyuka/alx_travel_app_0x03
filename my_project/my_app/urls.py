"""urls.py for my_app."""

from django.urls import path
from .views import BookListCreateAPIView

urlpatterns = [
    path("api/books/", BookListCreateAPIView.as_view(), name="book-list-create"),
]
