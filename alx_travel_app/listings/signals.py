"""signals.py
# Package containing the signals for the travel listings application.
# This module defines the signals that are triggered by various actions in the application,
# such as creating or updating listings, users, bookings, and reviews.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

from rest_framework_simplejwt.tokens import Token


@receiver(post_save, sender=User)
def create_user_jwt_tokens(sender, instance, created, **kwargs):
    """
    Signal to create a user profile when a User instance is created.
    This can be extended to create related models or perform additional actions.
    """
    if created:
        # Here you can create a profile or perform other actions
        print(f"User profile created for {instance.email}")
        token = Token.for_user(instance)
        print(f"JWT Token created for {instance.email}: {token}")
        # You can also save the token to the user model or perform other actions
        # instance.profile.save()  # If you have a profile model related to User
        # instance.jwt_token = token  # If you want to save the token in the user model
        # instance.save()  # Save the user instance if you modified it
        # Note: Ensure you have the necessary imports and configurations for JWT tokens
        # This is just an example; you can customize it as needed
