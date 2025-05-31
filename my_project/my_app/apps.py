"""apps.py
This module defines the configuration for the MyApp application in a Django project.
It specifies the default auto field type and the name of the application.
"""

from django.apps import AppConfig


class MyAppConfig(AppConfig):
    """Configuration for the MyApp application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "my_app"
