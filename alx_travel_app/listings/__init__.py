"""This module initializes the Celery application for the listings app.
It sets up the Celery configuration and makes the Celery app available for import.
"""

from .celery import app as celery_app

__all__ = ["celery_app"]
